import logging

from functools import wraps

from auth0.v3.authentication import GetToken
from auth0.v3.exceptions import Auth0Error
from auth0.v3.management import Auth0

from scripts.commands import settings

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

    def retrieve_client_id_all_apps(self):
        clients = self.auth0.clients.all(fields=["global", "name", "client_id"])
        for client in clients:
            if client["global"] and client["name"].lower() == "all applications":
                return client["client_id"]
        raise ShouldHaveFoundAllApplicationsClientException


class ShouldHaveFoundAllApplicationsClientException(Exception):
    pass


management_api = _ManagementAPI()
