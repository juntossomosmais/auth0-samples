import logging

from functools import wraps
from typing import List
from typing import Optional

from auth0.v3.authentication import GetToken
from auth0.v3.exceptions import Auth0Error
from auth0.v3.management import Auth0

from django_api import settings
from django_api.apps.core.providers.auth0_models import AppType
from django_api.apps.core.providers.auth0_models import User
from django_api.apps.core.providers.auth0_models import UserList
from django_api.support.dict_utils import clean_dict_with_falsy_or_strange_values

_logger = logging.getLogger(__name__)

_domain = settings.AUTH0_DOMAIN
_non_interactive_client_id = settings.AUTH0_MY_APPLICATION_KEY
_non_interactive_client_secret = settings.AUTH0_MY_APPLICATION_SECRET
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

    def retrieve_user(self, user_id):
        return self.auth0.users.get(user_id)

    def retrieve_users_with_same_verified_email(self, user_id, email) -> UserList:
        setup = {
            "search_engine": "v3",
            "q": f'email: "{email}" AND email_verified:true -user_id:"{user_id}"',
        }
        # https://auth0-python.readthedocs.io/en/latest/v3.management.html#auth0.v3.management.users.Users.list
        return self.auth0.users.list(**setup)

    def create_user_email_one_time_password(self, email):
        body = {
            "email": email,
            "email_verified": True,
            "connection": "email",
        }
        return self.auth0.users.create(body)

    def update_user(
        self,
        user_id,
        full_name=None,
        family_name=None,
        given_name=None,
        user_metadata=None,
        app_metadata=None,
        email=None,
    ):
        body = {
            "name": full_name,
            "family_name": family_name,
            "given_name": given_name,
            "user_metadata": user_metadata,
            "app_metadata": app_metadata,
            "email": email,
        }
        if email:
            body["email_verified"] = False
            body["verify_email"] = True
        body = clean_dict_with_falsy_or_strange_values(body)
        # TODO: Ensure that at least one of the optional parameters is provided
        # https://auth0-python.readthedocs.io/en/latest/v3.management.html#auth0.v3.management.users.Users.update
        return self.auth0.users.update(user_id, body)

    def retrieve_user_details(self, user_id: str) -> User:
        # https://auth0-python.readthedocs.io/en/latest/v3.management.html#auth0.v3.management.users.Users.get
        return self.auth0.users.get(user_id)

    def link_accounts_through_access_token(self, primary_user_id, target_user_id_access_token):
        body = {
            "link_with": target_user_id_access_token,
        }
        # https://auth0-python.readthedocs.io/en/latest/v3.management.html#auth0.v3.management.users.Users.link_user_account
        return self.auth0.users.link_user_account(primary_user_id, body)

    def link_accounts_through_secondary_accounts_details(self, primary_user_id: str, provider: str, user_id: str):
        body = {
            "provider": provider,
            "user_id": user_id,
        }
        # https://auth0-python.readthedocs.io/en/latest/v3.management.html#auth0.v3.management.users.Users.link_user_account
        return self.auth0.users.link_user_account(primary_user_id, body)

    def unlink_accounts(self, primary_user_id, target_provider, target_user_id):
        # https://auth0-python.readthedocs.io/en/latest/v3.management.html#auth0.v3.management.users.Users.unlink_user_account
        return self.auth0.users.unlink_user_account(primary_user_id, target_provider, target_user_id)


class ShouldHaveFoundAllApplicationsClientException(Exception):
    pass


class InvalidProvidedArgumentException(Exception):
    pass


def resource_owner(username_or_email, password):
    other_params = {"scope": None, "realm": None, "grant_type": "password", "audience": None}
    try:
        return _get_token.login(
            _non_interactive_client_id, _non_interactive_client_secret, username_or_email, password, **other_params
        )
    except Auth0Error as e:
        _logger.warning("We received %s because of the following: %s", e.status_code, e.message)
        if e.status_code == 403 and "wrong" in e.message.lower():
            return
        else:
            raise e


management_api = _ManagementAPI()
