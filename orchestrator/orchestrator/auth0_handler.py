import logging

from functools import wraps
from typing import List
from typing import Optional

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
        jwt_configuration=None,
    ):
        body = {
            "name": name,
            "cross_origin_auth": cross_origin_auth,
            "app_type": app_type.name.lower(),
            "jwt_configuration": {"alg": "RS256", "lifetime_in_seconds": 36000, "secret_encoded": False},
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
        if jwt_configuration:
            body["jwt_configuration"] = jwt_configuration
        if app_type == AppType.SPA:
            body["token_endpoint_auth_method"] = "none"

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

    def configure_email_provider(self, default_from_address, smtp_host, smtp_port, smtp_user, smtp_pass):
        body = {
            "name": "smtp",
            "enabled": True,
            "default_from_address": default_from_address,
            "credentials": {
                "smtp_host": smtp_host,
                "smtp_port": smtp_port,
                "smtp_user": smtp_user,
                "smtp_pass": smtp_pass,
            },
        }
        return self.auth0.emails.config(body)

    def current_email_provider(self) -> Optional[dict]:
        fields = ["credentials", "default_from_address", "settings", "enabled"]
        try:
            return self.auth0.emails.get(fields, include_fields=True)
        except Auth0Error as e:
            if e.status_code == 404 and e.message == "There is not a configured email provider":
                return None
            else:
                raise e

    def delete_email_provider(self):
        return self.auth0.emails.delete()

    def retrieve_all_connection(self, connection_name=None, fields=None):
        return self.auth0.connections.all(fields=fields, strategy=connection_name)

    def create_connection(self, name, strategy, enabled_clients=None):
        valid_strategy_names = ["facebook", "google-oauth2", "email"]

        if strategy not in valid_strategy_names:
            raise InvalidProvidedArgumentException

        if strategy == valid_strategy_names[0]:
            options = {"email": True, "scope": "email,public_profile", "public_profile": True}
        elif strategy == valid_strategy_names[1]:
            options = {"email": True, "scope": ["email", "profile"], "profile": True}
        else:
            options = {
                "name": "email",
                "totp": {"length": 6, "time_step": 180},
                "email": {
                    "body": '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml">\n  <head>\n    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n    <style type="text/css">.ExternalClass,.ExternalClass div,.ExternalClass font,.ExternalClass p,.ExternalClass span,.ExternalClass td,img{line-height:100%}#outlook a{padding:0}.ExternalClass,.ReadMsgBody{width:100%}a,blockquote,body,li,p,table,td{-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%}table,td{mso-table-lspace:0;mso-table-rspace:0}img{-ms-interpolation-mode:bicubic;border:0;height:auto;outline:0;text-decoration:none}table{border-collapse:collapse!important}#bodyCell,#bodyTable,body{height:100%!important;margin:0;padding:0;font-family:ProximaNova,sans-serif}#bodyCell{padding:20px}#bodyTable{width:600px}@font-face{font-family:ProximaNova;src:url(https://cdn.auth0.com/fonts/proxima-nova/proximanova-regular-webfont-webfont.eot);src:url(https://cdn.auth0.com/fonts/proxima-nova/proximanova-regular-webfont-webfont.eot?#iefix) format(\'embedded-opentype\'),url(https://cdn.auth0.com/fonts/proxima-nova/proximanova-regular-webfont-webfont.woff) format(\'woff\');font-weight:400;font-style:normal}@font-face{font-family:ProximaNova;src:url(https://cdn.auth0.com/fonts/proxima-nova/proximanova-semibold-webfont-webfont.eot);src:url(https://cdn.auth0.com/fonts/proxima-nova/proximanova-semibold-webfont-webfont.eot?#iefix) format(\'embedded-opentype\'),url(https://cdn.auth0.com/fonts/proxima-nova/proximanova-semibold-webfont-webfont.woff) format(\'woff\');font-weight:600;font-style:normal}@media only screen and (max-width:480px){#bodyTable,body{width:100%!important}a,blockquote,body,li,p,table,td{-webkit-text-size-adjust:none!important}body{min-width:100%!important}#bodyTable{max-width:600px!important}#signIn{max-width:280px!important}}\n</style>\n  </head>\n  <body leftmargin="0" marginwidth="0" topmargin="0" marginheight="0" offset="0" style="-webkit-text-size-adjust: 100%;-ms-text-size-adjust: 100%;margin: 0;padding: 0;font-family: &quot;ProximaNova&quot;, sans-serif;height: 100% !important;"><center>\n  <table style="width: 600px;-webkit-text-size-adjust: 100%;-ms-text-size-adjust: 100%;mso-table-lspace: 0pt;mso-table-rspace: 0pt;margin: 0;padding: 0;font-family: &quot;ProximaNova&quot;, sans-serif;border-collapse: collapse !important;height: 100% !important;" align="center" border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" id="bodyTable">\n    <tr>\n      <td align="center" valign="top" id="bodyCell" style="-webkit-text-size-adjust: 100%;-ms-text-size-adjust: 100%;mso-table-lspace: 0pt;mso-table-rspace: 0pt;margin: 0;padding: 20px;font-family: &quot;ProximaNova&quot;, sans-serif;height: 100% !important;">\n      <div class="main">\n        <p style="text-align: center;-webkit-text-size-adjust: 100%;-ms-text-size-adjust: 100%; margin-bottom: 30px;">\n          <img src="https://cdn.auth0.com/styleguide/2.0.9/lib/logos/img/badge.png" width="50" alt="Your logo goes here" style="-ms-interpolation-mode: bicubic;border: 0;height: auto;line-height: 100%;outline: none;text-decoration: none;">\n        </p>\n\n        <!-- Email change content -->\n        {% if operation == \'change_email\' %}\n\n          <p style="font-size: 1.2em;line-height: 1.3;-webkit-text-size-adjust: 100%;-ms-text-size-adjust: 100%;">Your email address has been updated.</p>\n\n        {% else %}\n\n          <!-- Signup email content -->\n          {% if send == \'link\' or send == \'link_ios\' or send == \'link_android\' %}\n\n            <p style="font-size: 1.2em;line-height: 1.3;-webkit-text-size-adjust: 100%;-ms-text-size-adjust: 100%;">Click and confirm that you want to sign in to {{ application.name }}. This link will expire in three minutes.</p>\n\n            <div style="text-align:center">\n            <a id="signIn" style="text-transform: uppercase;letter-spacing: 1px;color: #ffffff;text-decoration: none;display: inline-block;min-height: 48px;line-height: 48px;padding-top: 0;padding-right: 26px;padding-bottom: 0;margin: 20px 0;padding-left: 26px;border: 0;outline: 0;background: #eb5424;font-size: 14px;font-style: normal;font-weight: 400;text-align: center;white-space: nowrap;border-radius: 3px;text-overflow: ellipsis;max-width: 280px;overflow: hidden;-webkit-text-size-adjust: 100%;-ms-text-size-adjust: 100%;" href="{{ link }}">Sign in to {{ application.name }}</a>\n            </div>\n\n            <p style="-webkit-text-size-adjust: 100%;-ms-text-size-adjust: 100%;">Or sign in using this link:</p>\n            <p style="-webkit-text-size-adjust: 100%;-ms-text-size-adjust: 100%;"><a style="font-size: 12px; color: #A9B3BC; text-decoration: none;word-break: break-all;-webkit-text-size-adjust: 100%;-ms-text-size-adjust: 100%;" href="{{ link }}">{{ link }}</a></p>\n\n            {% elsif send == \'code\' %}\n\n            <p style="font-size: 1.4em; line-height: 1.3;">Your verification code is: <b>{{ code }}</b></p>\n\n          {% endif %}\n\n        {% endif %}\n\n        <p style="-webkit-text-size-adjust: 100%;-ms-text-size-adjust: 100%;">If you are having any issues with your account, please don\'t hesitate to contact us by replying to this mail.</p>\n\n        <br>\n        Thanks!\n        <br>\n\n        <strong>{{ application.name }}</strong>\n\n        <br><br>\n        <hr style="border: 2px solid #EAEEF3; border-bottom: 0; margin: 20px 0;">\n        <p style="text-align: center;color: #A9B3BC;-webkit-text-size-adjust: 100%;-ms-text-size-adjust: 100%;">\n          If you did not make this request, please contact us by replying to this mail.\n        </p>\n      </div>\n      </td>\n    </tr>\n  </table>\n</center>\n</body>\n</html>',
                    "from": "{{ application.name }} <root@auth0.com>",
                    "syntax": "liquid",
                    "subject": "Welcome to {{ application.name }}",
                },
                "disable_signup": False,
                "brute_force_protection": True,
            }

        body = {
            "name": name,
            "strategy": strategy,
            "options": options,
        }

        if enabled_clients:
            body["enabled_clients"] = enabled_clients

        return self.auth0.connections.create(body)

    def delete_connection(self, connection_id):
        return self.auth0.connections.delete(connection_id)

    def update_connection_with_clients(self, connection_id: str, enabled_clients: List[str]):
        body = {"enabled_clients": enabled_clients}
        return self.auth0.connections.update(connection_id, body)

    def update_connection_to_enable_username(self, connection_id: str, strategy: str):
        # Finding all options
        connections = self.retrieve_all_connection(connection_name=strategy, fields=["options", "id"])
        connection_options = None
        for connection in connections:
            if connection["id"] == connection_id:
                connection_options = connection["options"]
        if not connection_options:
            raise InvalidProvidedArgumentException
        # Updating properties
        connection_options["validation"] = {"username": {"max": 11, "min": 11}}
        connection_options["requires_username"] = True
        # Final object
        body = {"options": connection_options}
        return self.auth0.connections.update(connection_id, body)

    def retrieve_all_client_grants(self):
        return self.auth0.client_grants.all()

    def create_client_grant(self, client_id, audience, scope: List[str]):
        body = {
            "client_id": client_id,
            "audience": audience,
            "scope": scope,
        }
        return self.auth0.client_grants.create(body)


class ShouldHaveFoundAllApplicationsClientException(Exception):
    pass


class InvalidProvidedArgumentException(Exception):
    pass


management_api = _ManagementAPI()
