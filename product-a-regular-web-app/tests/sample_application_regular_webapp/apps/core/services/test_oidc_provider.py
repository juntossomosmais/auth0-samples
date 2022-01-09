from unittest import TestCase

from product_a_regular_web_app import settings
from product_a_regular_web_app.apps.core.services.oidc_provider import OIDCConfigurationDocument
from product_a_regular_web_app.apps.core.services.oidc_provider import OIDCProvider


class OIDCProviderTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        OIDCProvider.configure_class_properties(
            settings.SOCIAL_AUTH_AUTH0_DOMAIN,
            settings.SOCIAL_AUTH_AUTH0_KEY,
            settings.SOCIAL_AUTH_AUTH0_SECRET,
            settings.SOCIAL_AUTH_AUTH0_SCOPE,
        )

    def test_should_setup_oidc_configuration(self):
        # Act
        OIDCProvider.configure_oidc_configuration_document()
        # Assert
        document = OIDCProvider.oidc_configuration_document
        public_keys = OIDCProvider.jwt_public_keys
        assert document == OIDCConfigurationDocument(
            authorization_endpoint="https://antunes.us.auth0.com/authorize",
            token_endpoint="https://antunes.us.auth0.com/oauth/token",
            device_authorization_endpoint="https://antunes.us.auth0.com/oauth/device/code",
            userinfo_endpoint="https://antunes.us.auth0.com/userinfo",
            mfa_challenge_endpoint="https://antunes.us.auth0.com/mfa/challenge",
            jwks_uri="https://antunes.us.auth0.com/.well-known/jwks.json",
            registration_endpoint="https://antunes.us.auth0.com/oidc/register",
            revocation_endpoint="https://antunes.us.auth0.com/oauth/revoke",
            issuer="https://antunes.us.auth0.com/",
            scopes_supported=[
                "openid",
                "profile",
                "offline_access",
                "name",
                "given_name",
                "family_name",
                "nickname",
                "email",
                "email_verified",
                "picture",
                "created_at",
                "identities",
                "phone",
                "address",
            ],
            response_types_supported=[
                "code",
                "token",
                "id_token",
                "code token",
                "code id_token",
                "token id_token",
                "code token id_token",
            ],
            code_challenge_methods_supported=["S256", "plain"],
            response_modes_supported=["query", "fragment", "form_post"],
            subject_types_supported=["public"],
            id_token_signing_alg_values_supported=["HS256", "RS256"],
            token_endpoint_auth_methods_supported=["client_secret_basic", "client_secret_post"],
            claims_supported=[
                "aud",
                "auth_time",
                "created_at",
                "email",
                "email_verified",
                "exp",
                "family_name",
                "given_name",
                "iat",
                "identities",
                "iss",
                "name",
                "nickname",
                "phone_number",
                "picture",
                "sub",
            ],
            request_uri_parameter_supported=False,
        )
        assert len(public_keys) == 1
