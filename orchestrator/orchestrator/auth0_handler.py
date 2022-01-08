import logging

from functools import wraps
from typing import List

from auth0.v3.authentication import GetToken
from auth0.v3.exceptions import Auth0Error
from auth0.v3.management import Auth0

from orchestrator import settings
from orchestrator.models import AppType
from orchestrator.models import User
from orchestrator.models import UserList

_logger = logging.getLogger(__name__)

_domain = settings.AUTH0_DOMAIN
_non_interactive_client_id = settings.AUTH0_M2M_CLIENT_ID
_non_interactive_client_secret = settings.AUTH0_M2M_CLIENT_SECRET
_endpoint = f"https://{_domain}/api/v2/"

_get_token = GetToken(_domain)


def retrieve_access_token():
    token = _get_token.client_credentials(_non_interactive_client_id, _non_interactive_client_secret, _endpoint)
    return token["access_token"]


class _BaseManagementAPIMetaClass(type):
    def __new__(cls, subclass_name, bases, dictionary):
        for attribute in dictionary:
            value = dictionary[attribute]
            must_wrap_function = not attribute.startswith("__") and not attribute.startswith("_") and callable(value)
            if must_wrap_function:
                dictionary[attribute] = reauthenticate()(value)
        return type.__new__(cls, subclass_name, bases, dictionary)


def reauthenticate():
    def reauthentication_logic(func, self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Auth0Error as e:
            _logger.warning("We received %s because of the following: %s", e.status_code, e.message)
            if e.status_code == 401:
                self.auth0 = Auth0(_domain, retrieve_access_token())
                return func(self, *args, **kwargs)
            else:
                raise e

    def main_wrapper(func):
        @wraps(func)
        def wrapped(self, *args, **kwargs):
            try:
                return reauthentication_logic(func, self, *args, **kwargs)
            except AttributeError as e:
                create_auth0 = e.args[0].endswith("object has no attribute 'auth0'")
                if create_auth0:
                    self.auth0 = Auth0(_domain, retrieve_access_token())
                    return reauthentication_logic(func, self, *args, **kwargs)
                else:
                    raise e

        return wrapped

    return main_wrapper


class _ManagementAPI(object, metaclass=_BaseManagementAPIMetaClass):
    auth0: Auth0

    def update_login_page_classic(self, page: str):
        all_applications_client_id = self.retrieve_client_id_all_apps()
        body = {"custom_login_page": page}
        return self.auth0.clients.update(all_applications_client_id, body)

    def retrieve_all_clients(self, fields=None):
        return self.auth0.clients.all(fields=fields)

    def create_client(
        self,
        name,
        app_type: AppType,
        callbacks: List[str] = None,
        cross_origin_auth=False,
        allowed_origins: List[str] = None,
        web_origins: List[str] = None,
        allowed_logout_urls: List[str] = None,
        grant_types: List[str] = None,
    ):
        body = {
            "name": name,
            "cross_origin_auth": cross_origin_auth,
            "app_type": app_type.name.lower(),
        }
        if callbacks:
            body["callbacks"] = callbacks
        if allowed_origins:
            body["allowed_origins"] = allowed_origins
        if web_origins:
            body["web_origins"] = web_origins
        if allowed_logout_urls:
            body["allowed_logout_urls"] = allowed_logout_urls
        if grant_types:
            body["grant_types"] = grant_types

        # https://auth0-python.readthedocs.io/en/latest/v3.management.html#auth0.v3.management.clients.Clients.create
        return self.auth0.clients.create(body)

    def delete_client(self, client_id):
        return self.auth0.clients.delete(client_id)

    def retrieve_client_id_all_apps(self):
        clients = self.auth0.clients.all(fields=["global", "name", "client_id"])
        for client in clients:
            if client["global"] and client["name"].lower() == "all applications":
                return client["client_id"]
        raise ShouldHaveFoundAllApplicationsClientException

    def retrieve_users_with_same_verified_email(self, user_id, email) -> UserList:
        setup = {
            "search_engine": "v3",
            "q": f'email: "{email}" AND email_verified:true -user_id:"{user_id}"',
        }
        # https://auth0-python.readthedocs.io/en/latest/v3.management.html#auth0.v3.management.users.Users.list
        return self.auth0.users.list(**setup)

    def retrieve_user_details(self, user_id: str) -> User:
        # https://auth0-python.readthedocs.io/en/latest/v3.management.html#auth0.v3.management.users.Users.get
        return self.auth0.users.get(user_id)

    def link_accounts(self, primary_user_id, target_user_id_access_token):
        body = {
            "link_with": target_user_id_access_token,
        }
        # https://auth0-python.readthedocs.io/en/latest/v3.management.html#auth0.v3.management.users.Users.link_user_account
        return self.auth0.users.link_user_account(primary_user_id, body)

    def unlink_accounts(self, primary_user_id, target_provider, target_user_id):
        # https://auth0-python.readthedocs.io/en/latest/v3.management.html#auth0.v3.management.users.Users.unlink_user_account
        return self.auth0.users.unlink_user_account(primary_user_id, target_provider, target_user_id)


class ShouldHaveFoundAllApplicationsClientException(Exception):
    pass


management_api = _ManagementAPI()
