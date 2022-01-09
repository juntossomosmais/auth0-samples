import logging

from functools import wraps
from typing import List
from typing import TypedDict

from auth0.v3.authentication import GetToken
from auth0.v3.exceptions import Auth0Error
from auth0.v3.management import Auth0

from product_a_regular_web_app import settings

_logger = logging.getLogger(__name__)

_domain = settings.SOCIAL_AUTH_AUTH0_DOMAIN
_non_interactive_client_id = settings.SOCIAL_AUTH_AUTH0_KEY
_non_interactive_client_secret = settings.SOCIAL_AUTH_AUTH0_SECRET
_endpoint = f"https://{_domain}/api/v2/"

_get_token = GetToken(_domain)


def retrieve_access_token():
    token = _get_token.client_credentials(_non_interactive_client_id, _non_interactive_client_secret, _endpoint)
    return token["access_token"]


class User(TypedDict):
    created_at: str
    email: str
    email_verified: bool
    given_name: str
    family_name: str
    identities: dict
    video_upload_limits: dict
    locale: str
    name: str
    nickname: str
    picture: str
    updated_at: str
    user_id: str
    last_login: str
    last_ip: str
    logins_count: str
    install_type: str
    installed: str
    # Sample value: "{first} {last}"
    name_format: str
    picture: str
    picture_large: str
    short_name: str


class UserList(TypedDict):
    start: int
    limit: int
    length: int
    total: int
    users: List[User]


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


management_api = _ManagementAPI()
