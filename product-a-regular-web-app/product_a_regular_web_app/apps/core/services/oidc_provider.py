import inspect
import logging

from dataclasses import dataclass
from typing import List
from typing import Optional
from typing import Set
from typing import TypedDict

import requests

from jose import jwt
from requests.auth import HTTPBasicAuth

from product_a_regular_web_app.support.http_utils import build_url_with_query_strings

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class OIDCConfigurationDocument:
    # Endpoints
    authorization_endpoint: str
    token_endpoint: str
    device_authorization_endpoint: str
    userinfo_endpoint: str
    mfa_challenge_endpoint: str
    jwks_uri: str
    registration_endpoint: str
    revocation_endpoint: str
    # Metadata
    issuer: str
    scopes_supported: List[str]
    response_types_supported: List[str]
    code_challenge_methods_supported: List[str]
    response_modes_supported: List[str]
    subject_types_supported: List[str]
    id_token_signing_alg_values_supported: List[str]
    token_endpoint_auth_methods_supported: List[str]
    claims_supported: List[str]
    request_uri_parameter_supported: bool
    request_parameter_supported: bool

    @classmethod
    def from_dict(cls, env):
        return cls(**{k: v for k, v in env.items() if k in inspect.signature(cls).parameters})


class JWTPublicKey(TypedDict):
    alg: str
    e: str
    kid: str
    kty: str
    n: str
    use: str
    x5t: Optional[str]
    x5c: Optional[str]


class JWTPublicKeys(TypedDict):
    keys: List[JWTPublicKey]


class OIDCProvider:
    oidc_configuration_document: OIDCConfigurationDocument
    jwt_public_keys: JWTPublicKeys
    jwt_public_keys_algorithms: Set[str]

    domain = str
    app_client_key = str
    app_client_secret = str
    scopes = str

    @classmethod
    def configure_class_properties(cls, domain, app_key, app_secret, scopes: List[str]):
        cls.domain = domain
        cls.app_client_key = app_key
        cls.app_client_secret = app_secret
        cls.scopes = scopes

    @classmethod
    def configure_oidc_configuration_document(cls):
        document = requests.get(f"https://{cls.domain}/.well-known/openid-configuration").json()

        # Sample document that is returned by openid-configuration endpoint:
        # {
        #     "issuer": "https://antunes.us.auth0.com/",
        #     "authorization_endpoint": "https://antunes.us.auth0.com/authorize",
        #     "token_endpoint": "https://antunes.us.auth0.com/oauth/token",
        #     "device_authorization_endpoint": "https://antunes.us.auth0.com/oauth/device/code",
        #     "userinfo_endpoint": "https://antunes.us.auth0.com/userinfo",
        #     "mfa_challenge_endpoint": "https://antunes.us.auth0.com/mfa/challenge",
        #     "jwks_uri": "https://antunes.us.auth0.com/.well-known/jwks.json",
        #     "registration_endpoint": "https://antunes.us.auth0.com/oidc/register",
        #     "revocation_endpoint": "https://antunes.us.auth0.com/oauth/revoke",
        #     "scopes_supported": [
        #         "openid",
        #         "profile",
        #         "offline_access",
        #         "name",
        #         "given_name",
        #         "family_name",
        #         "nickname",
        #         "email",
        #         "email_verified",
        #         "picture",
        #         "created_at",
        #         "identities",
        #         "phone",
        #         "address",
        #     ],
        #     "response_types_supported": [
        #         "code",
        #         "token",
        #         "id_token",
        #         "code token",
        #         "code id_token",
        #         "token id_token",
        #         "code token id_token",
        #     ],
        #     "code_challenge_methods_supported": ["S256", "plain"],
        #     "response_modes_supported": ["query", "fragment", "form_post"],
        #     "subject_types_supported": ["public"],
        #     "id_token_signing_alg_values_supported": ["HS256", "RS256"],
        #     "token_endpoint_auth_methods_supported": ["client_secret_basic", "client_secret_post"],
        #     "claims_supported": [
        #         "aud",
        #         "auth_time",
        #         "created_at",
        #         "email",
        #         "email_verified",
        #         "exp",
        #         "family_name",
        #         "given_name",
        #         "iat",
        #         "identities",
        #         "iss",
        #         "name",
        #         "nickname",
        #         "phone_number",
        #         "picture",
        #         "sub",
        #     ],
        #     "request_uri_parameter_supported": False,
        # }

        # First let's configure the OIDC configuration document
        cls.oidc_configuration_document = OIDCConfigurationDocument.from_dict(document)

        # Now the public keys to verify the JWT created by Auth0
        public_keys = requests.get(cls.oidc_configuration_document.jwks_uri).json()

        # Sample public keys that is returned by jwks_uri endpoint:
        # {
        #     "keys": [
        #         {
        #             "alg": "RS256",
        #             "kty": "RSA",
        #             "use": "sig",
        #             "n": "01EW-npmkOYEpwM6LLKpr6OJ1s_gQQz3biUzBY5QdH3JwWS37h6WFUdyv-CJEBWBetbzHLBYx_58HbGcGwmhht7bXJ8WDlRroxvt7MoYhINMaG8aXo3Giw0_st-VaEC8BuNEemfhJHBlcpJR8-ZdSLx5Q-rFojePOdnVrbcGIviVu9b6pOPHI1jnW_WmyBfG5XmXPHy2aL3OxjLFa8uVkxyHIu1mN3hWEdzZqewUqrFe91egCwT7u4MOkLgfmym_meXjXgIJZSp-GvNGJzk8Iyr0EszlrimP8eBgLg4AjEmwQzRkcRSXYsGCjO8-Dy4ecch-YNhOXpzWSf4bC22XYw",
        #             "e": "AQAB",
        #             "kid": "faYZw_CEI0IRz-SaG9bhi",
        #             "x5t": "ovFav4LfCHs4qZaOImYWpxoXdzA",
        #             "x5c": [
        #                 "MIIDAzCCAeugAwIBAgIJbqiVa0rLk9wpMA0GCSqGSIb3DQEBCwUAMB8xHTAbBgNVBAMTFGFudHVuZXMudXMuYXV0aDAuY29tMB4XDTIxMTAwNjE1MDIwNVoXDTM1MDYxNTE1MDIwNVowHzEdMBsGA1UEAxMUYW50dW5lcy51cy5hdXRoMC5jb20wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDTURb6emaQ5gSnAzossqmvo4nWz+BBDPduJTMFjlB0fcnBZLfuHpYVR3K/4IkQFYF61vMcsFjH/nwdsZwbCaGG3ttcnxYOVGujG+3syhiEg0xobxpejcaLDT+y35VoQLwG40R6Z+EkcGVyklHz5l1IvHlD6sWiN4852dWttwYi+JW71vqk48cjWOdb9abIF8bleZc8fLZovc7GMsVry5WTHIci7WY3eFYR3Nmp7BSqsV73V6ALBPu7gw6QuB+bKb+Z5eNeAgllKn4a80YnOTwjKvQSzOWuKY/x4GAuDgCMSbBDNGRxFJdiwYKM7z4PLh5xyH5g2E5enNZJ/hsLbZdjAgMBAAGjQjBAMA8GA1UdEwEB/wQFMAMBAf8wHQYDVR0OBBYEFC21wXqeOFczGIEjlB+FCDVuaqleMA4GA1UdDwEB/wQEAwIChDANBgkqhkiG9w0BAQsFAAOCAQEAl1I7bmq6ihafH9Zts+Fc9/Pe6kQ6C8yUMTJheNpiX6FTBfEWPuX/KWDz2WcC2/1S8tsQZPD3GJEF899LDa8F+mHY2adWMgFep5e5AejcwdmnZlCZoKmVAZ2HZHMgQr7RM0c0HZ2laBbzv4XcZPiDBP8YCuJlmL4zQFMeuWlA4ShCPB8Vk0VhDIJ/GBHvKYgy2pSa7mfZpoC4JcUc5XV4q6fZahEL27eqC3l4ffXaEcBK1axy769SaJpxHgpEeniMkfGcbuAYamInO64lhqKLf0hq9kQ6WId17hOt9nMa2q2ct88s5ZJirDzkE9uEKr0m9tqqaTgupN/xgq0xHVXkww=="
        #             ],
        #         },
        #         {
        #             "alg": "RS256",
        #             "kty": "RSA",
        #             "use": "sig",
        #             "n": "uPw-p0UpUVWd54qkPEfxt6GRqt1kJFDmzWmwVBfJxtRLp4m7jixzX9KNQrRWhBNJ1rlAxqpookqeB6cm74aEJ_UAJ-uPHnGKqYdA41VBOMrCgMl-DH86peK-HtGg_0vg6D0qMkcmXZJBGeKdK6UAhw0uwALEqN_twlBwdvtVocS30fvYdt_JqTnSb8uimRnoaA5GoAet5fAG7cph5ZnZuIAYdVf4T3RiPBdRNtHJbP9cuCZatJWb7CabjuIN9wmztAsex8n9wuSp06_wuVWJQQiCDGQF8tT11yn4TlFnzdlwxpQ8ngrvsoAt0KPfA_1rrFBL9vhGIGFkkRvfC3WFUw",
        #             "e": "AQAB",
        #             "kid": "1Yjr6qd1riVeCrHC-DuhH",
        #             "x5t": "oLlrWY6HThi71U-AJZwN4Jn24IU",
        #             "x5c": [
        #                 "MIIDAzCCAeugAwIBAgIJU21sCpl+udZDMA0GCSqGSIb3DQEBCwUAMB8xHTAbBgNVBAMTFGFudHVuZXMudXMuYXV0aDAuY29tMB4XDTIxMTAwNjE1MDIwNloXDTM1MDYxNTE1MDIwNlowHzEdMBsGA1UEAxMUYW50dW5lcy51cy5hdXRoMC5jb20wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC4/D6nRSlRVZ3niqQ8R/G3oZGq3WQkUObNabBUF8nG1EunibuOLHNf0o1CtFaEE0nWuUDGqmiiSp4HpybvhoQn9QAn648ecYqph0DjVUE4ysKAyX4Mfzql4r4e0aD/S+DoPSoyRyZdkkEZ4p0rpQCHDS7AAsSo3+3CUHB2+1WhxLfR+9h238mpOdJvy6KZGehoDkagB63l8AbtymHlmdm4gBh1V/hPdGI8F1E20cls/1y4Jlq0lZvsJpuO4g33CbO0Cx7Hyf3C5KnTr/C5VYlBCIIMZAXy1PXXKfhOUWfN2XDGlDyeCu+ygC3Qo98D/WusUEv2+EYgYWSRG98LdYVTAgMBAAGjQjBAMA8GA1UdEwEB/wQFMAMBAf8wHQYDVR0OBBYEFG1wVasCVyhsSQnaDuAxSj0AF3/qMA4GA1UdDwEB/wQEAwIChDANBgkqhkiG9w0BAQsFAAOCAQEArfE7/0Khu6Dupfyy9dy5FdL9HUxBF1YgFeOWPBZg8VilRkldjq+S8axYUdbhpyCuEcnnInqO17t+KJ5/oRdEb1Ma4Lj4XD2GdyN1wTniUoq2P/r5aGRqToISAEtwpvVgYmQZflDC9xYq+d5ddZ43LfouWKSkE01OfL7YQJM+yNWm4dwQAT0gXNchnBGRtlajhStYLDb6Sci/AizEIMcqZnkXoBJQXwaEBYZCsXCkWgUoiQFVPzZr07m4iQF4FtoyPsjlbxbhQ2ymEbVCS986zmApkTfv9GcTSpIonoom7fMjkww+7s5/CoKgPCvYeEu+phmW8nzY8o0FsSeNUfI6nw=="
        #             ],
        #         },
        #     ]
        # }

        jwt_public_keys_algorithms = set()
        for public_key in public_keys["keys"]:
            algorithm = public_key.get("alg")
            if algorithm:
                jwt_public_keys_algorithms.add(algorithm)

        cls.jwt_public_keys = public_keys
        cls.jwt_public_keys_algorithms = jwt_public_keys_algorithms

    @classmethod
    def build_authorization_url(cls, redirect_uri: str, state: str, params: Optional[dict] = None):
        # https://auth0.com/docs/api/authentication#authorization-code-flow
        # https://auth0.com/docs/login/authentication/add-login-auth-code-flow#authorize-user
        auth_url = cls.oidc_configuration_document.authorization_endpoint
        provided_params = {
            "state": state,
            "client_id": cls.app_client_key,
            "response_type": "code",
            "redirect_uri": redirect_uri,
            "scope": " ".join(cls.scopes),
            # https://auth0.com/docs/brand-and-customize/i18n/universal-login-internationalization
            # Instead of passing the parameter below, I changed the tenant itself!
            # "ui_locales": "pt-BR",
        }
        if params:
            provided_params = provided_params | params

        logger.debug("Building authorization URL...")
        return build_url_with_query_strings(auth_url, provided_params)

    @classmethod
    def acquire_token_by_auth_code_flow(cls, code: str, redirect_uri: str):
        # https://auth0.com/docs/api/authentication#authenticate-user
        # https://auth0.com/docs/authorization/flows/call-your-api-using-the-authorization-code-flow#request-tokens
        token_endpoint = cls.oidc_configuration_document.token_endpoint
        app_credentials = HTTPBasicAuth(cls.app_client_key, cls.app_client_secret)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        body = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": cls.app_client_key,
            "redirect_uri": redirect_uri,
            "scope": " ".join(cls.scopes),
        }
        response = requests.post(token_endpoint, headers=headers, data=body, auth=app_credentials)
        content = response.json()
        id_token = content["id_token"]
        access_token = content["access_token"]
        claims = cls._retrieve_claims(id_token, access_token)
        return content, claims

    @classmethod
    def _retrieve_claims(cls, id_token: str, access_token: str) -> dict:
        issuer = cls.oidc_configuration_document.issuer
        algorithms = list(cls.jwt_public_keys_algorithms)
        if not algorithms:
            algorithms.append(jwt.get_unverified_headers(id_token)["alg"])
        audience = cls.app_client_key
        public_keys = cls.jwt_public_keys

        # return jwt.decode(
        #     id_token, public_keys, algorithms=algorithms, audience=audience, issuer=issuer, access_token=access_token
        # )
        return jwt.decode(id_token, public_keys, algorithms=algorithms, audience=audience, access_token=access_token)

    @classmethod
    def build_logout_url(cls, return_to):
        # https://auth0.com/docs/api/authentication#logout
        logout_endpoint = f"https://{cls.domain}/v2/logout"

        params = {
            "returnTo": return_to,
            "client_id": cls.app_client_key,
        }
        logger.debug("Building logout URL...")
        return build_url_with_query_strings(logout_endpoint, params)

    @classmethod
    def get_user_info(cls, access_token: str):
        # https://auth0.com/docs/api/authentication#user-profile
        userinfo_endpoint = cls.oidc_configuration_document.userinfo_endpoint
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        result = requests.get(userinfo_endpoint, headers=headers)
        # Sample result
        # {
        #     "sub": "bbf338b6-fa67-4b91-baaf-24886a31b3d6",
        #     "email_verified": "true",
        #     "email": "willianlimaantunes@gmail.com",
        #     "username": "willian",
        # }
        body = result.json()

        return body
