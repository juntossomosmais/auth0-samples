import pytest

from jwt import PyJWKClient
from jwt import PyJWKSet
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.test import APIRequestFactory

from django_api.apps.core.api.authentication.authentications import JWTAccessTokenAuthentication
from django_api.apps.core.api.authentication.models import TokenUser


@pytest.fixture
def jwt_access_token_authentication_scenario(mocker):
    factory = APIRequestFactory()
    fake_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVRUGdscDc2cWt2c1NLazZsaFR6byJ9.eyJpc3MiOiJodHRwczovL2pzbS1zYW5kYm94LWRldjEudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYxZTQ2NmMwYWUyOWIzMDA3NjQ2OGIzMCIsImF1ZCI6WyJodHRwczovL3VzZXItbWFuYWdlbWVudC9kamFuZ28tYXBpLyIsImh0dHBzOi8vanNtLXNhbmRib3gtZGV2MS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjQzNTcyNTk0LCJleHAiOjE2NDM2NTg5OTQsImF6cCI6Imx0MlppT3ZENTJuNFkzenpRNDM0MGZJQUU0SkdSblU4Iiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCJ9.jMSoSkPn7Ihn3PDYg3Q4QRCbkHuKT6Igh3eoqw1tMiNHkg0_CuRcsUxvFouJkA85YnWCEqMMuNPNkdX8QuftAoj0I2eXq8p1fxHfeclyPB3n02tj4_r5_o_zqMspMTD3l2oE6JiiLdMvx3TH0fdbX3IGW2F-IEaVVVTHpnkOI9fhw-25DAI_aHXI1dB7Hc4zD6Ug51WNL77-Rtm_TH7sBPLJFkqLl_g0kEgHch8otazOO3c1PJutmoBGEuTgRysPEVW-wyRLVktl5EVL8nzsTEtZZYGpgD-sy7YEw1ivhpv8hM8bCxF-GQhIfTQU0HZrpL0Cclvf20dKWzc1YDnr8A"
    fake_jwks = {
        "keys": [
            {
                "alg": "RS256",
                "kty": "RSA",
                "use": "sig",
                "n": "ptoBeC2lYCefxlmk8JfTZz5QnYkmhfubD5xmHPfsevD6d6Bs9544HEkWC6AbS90awwSuz_wDRL6Qz6f4DppkLW5NFK6Vq2yCVy19A4wqZ_SqylstXJAZd8iZUIZW2GbhUm2P-mevciFJGWucMm08n7QDO8pcKETWMkktOqPMJfODIImH1OO9eX7L9Wc5yVwQqOL-4Ey6-1Ejd3VoT-ssaYrmIshplrgP1qURdT4rvwyJsyiMmUI9yL3IlUiHDOot07Qf1kvShaE4X2X46w9VOUepqXtg26JUDLs-q_iTHZQJSo0QPoeqMvJUtjSEsfuih0wtTfOY4HHD5sKwSYo4kQ",
                "e": "AQAB",
                "kid": "uQPglp76qkvsSKk6lhTzo",
                "x5t": "44uB4xIL3dzyQzPULQ8UyslMvy0",
                "x5c": [
                    "MIIDFTCCAf2gAwIBAgIJMnZx2QzTfSrSMA0GCSqGSIb3DQEBCwUAMCgxJjAkBgNVBAMTHWpzbS1zYW5kYm94LWRldjEudXMuYXV0aDAuY29tMB4XDTIyMDEwNTIxNTAzNFoXDTM1MDkxNDIxNTAzNFowKDEmMCQGA1UEAxMdanNtLXNhbmRib3gtZGV2MS51cy5hdXRoMC5jb20wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCm2gF4LaVgJ5/GWaTwl9NnPlCdiSaF+5sPnGYc9+x68Pp3oGz3njgcSRYLoBtL3RrDBK7P/ANEvpDPp/gOmmQtbk0UrpWrbIJXLX0DjCpn9KrKWy1ckBl3yJlQhlbYZuFSbY/6Z69yIUkZa5wybTyftAM7ylwoRNYySS06o8wl84MgiYfU4715fsv1ZznJXBCo4v7gTLr7USN3dWhP6yxpiuYiyGmWuA/WpRF1Piu/DImzKIyZQj3IvciVSIcM6i3TtB/WS9KFoThfZfjrD1U5R6mpe2DbolQMuz6r+JMdlAlKjRA+h6oy8lS2NISx+6KHTC1N85jgccPmwrBJijiRAgMBAAGjQjBAMA8GA1UdEwEB/wQFMAMBAf8wHQYDVR0OBBYEFP7B9Ju9NnrRj02P0bp4fny77jQLMA4GA1UdDwEB/wQEAwIChDANBgkqhkiG9w0BAQsFAAOCAQEACh2TpSwC/B7Uz7zbt7dzJaAM9F+GTzBVfwG8vC6/suBAU9uNbWaz3Bb+eByJ+wiWoR1boATtFU27ykALu1HbM/G9SIua783F/nkkzVUUwSHPYRdlxgHtfyrZHNiROxDJ4wqrbUEbjhcStFPxVUDNu+q5QW6+/FYaI2OR9fbJbK6rivGEZ+qKEfPKAd86T1Emkgp9exCgl3rWsl/2VCj5Zl55hkTxuTmHQmyrSV5STrIQhzq/o7FPT3EA1ukWx0dtl/73+rKy67Gb93TP0oeOZmETAsP6fbD1SPpYF9aFp/GJnll+TDPmGaRXdhszWMohqYVLOx6L+VcMCU9DFghesQ=="
                ],
            },
            {
                "alg": "RS256",
                "kty": "RSA",
                "use": "sig",
                "n": "2_nzPyykse3xOJLRlnRKynhgruqTNFva5fUhv7mazzpFDFAb71ojCi3YlpLJOQpaX9LpKq9OSerCX2qLgnRQL_auRNjlZw8AHJOAdPQTIQEmHrjqLNz8QK28vxZOQzJORYN7cfClsMevJ21rWWnalqsP4sCZUTnTpDfzrdKUN9IAD86Wonkw-JM_LipK2P_vkHUtpEawO0GuXl28tI-cbAoijqN0Qfzwa-nZJwLiufKtMD7I7hxPCRPA6dAcZyE4Lyb4hb8guTaLrApKLr8e0n2u0qurAhGD6uR_AX3j5D7TsL5CsI609GCesE25wV2oInt5k63dUT7IuTFj2D8Iow",
                "e": "AQAB",
                "kid": "JoCS-tDuDkNx7260zjx9z",
                "x5t": "N9Z24tD_JeaWsZuPZ5qlt9nYOqc",
                "x5c": [
                    "MIIDFTCCAf2gAwIBAgIJE9wUerX84GmPMA0GCSqGSIb3DQEBCwUAMCgxJjAkBgNVBAMTHWpzbS1zYW5kYm94LWRldjEudXMuYXV0aDAuY29tMB4XDTIyMDEwNTIxNTAzNFoXDTM1MDkxNDIxNTAzNFowKDEmMCQGA1UEAxMdanNtLXNhbmRib3gtZGV2MS51cy5hdXRoMC5jb20wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDb+fM/LKSx7fE4ktGWdErKeGCu6pM0W9rl9SG/uZrPOkUMUBvvWiMKLdiWksk5Clpf0ukqr05J6sJfaouCdFAv9q5E2OVnDwAck4B09BMhASYeuOos3PxArby/Fk5DMk5Fg3tx8KWwx68nbWtZadqWqw/iwJlROdOkN/Ot0pQ30gAPzpaieTD4kz8uKkrY/++QdS2kRrA7Qa5eXby0j5xsCiKOo3RB/PBr6dknAuK58q0wPsjuHE8JE8Dp0BxnITgvJviFvyC5NousCkouvx7Sfa7Sq6sCEYPq5H8BfePkPtOwvkKwjrT0YJ6wTbnBXagie3mTrd1RPsi5MWPYPwijAgMBAAGjQjBAMA8GA1UdEwEB/wQFMAMBAf8wHQYDVR0OBBYEFGJ6wvMKPkN1JVyvTnTQ00XvU5rrMA4GA1UdDwEB/wQEAwIChDANBgkqhkiG9w0BAQsFAAOCAQEAhHpQYjxRSwTxhcNKX7OjlC6vGp/UCUWSezsHO3Rq0dSopbqrsoOqbEuG6RA1cPNmAO4Cry0oPdIaJY7SuYSfDlqegxp+DRbpYMhFVz2L2DDTe/zaicQg5RjQoSd9O4edA68a0qcKuJ1qTuqoN0gw+c12M6LbYpzwP1ABn+5t/xd9A4gPuNXovLPlZ/TaoARY7cjFhePbp62OOHudZ86RlkC1BFV9GykKw1gK9B6d/Hk+WuVidc7ppAZe3Q14dANmmGPcotjsafhEwNH9ZwhUIUwh/001otNh5i+ck2oW4iun7xiMFrArvhdQQe3mFKuJxy+obnPjadbnBAgGHZv2PQ=="
                ],
            },
        ]
    }
    mocked_jwks_client = PyJWKClient("https://agrabah/.well-known/jwks.json")
    mocker.patch.object(mocked_jwks_client, "get_jwk_set", lambda: PyJWKSet.from_dict(fake_jwks))
    extra_internal_options = {
        "internal_extra_jwt_decode_options": {"verify_exp": False},
        "internal_jwks_client": mocked_jwks_client,
    }
    backend = JWTAccessTokenAuthentication(**extra_internal_options)
    return factory, backend, fake_token


def test_should_return_none_if_no_authorization_header(jwt_access_token_authentication_scenario):
    # Arrange
    factory, backend, _ = jwt_access_token_authentication_scenario
    request = factory.get("/test-url/")
    # Act
    with pytest.raises(AuthenticationFailed) as authentication_failed_exception:
        backend.authenticate(request)
    # Assert
    assert authentication_failed_exception.value.status_code == 401
    assert authentication_failed_exception.value.detail == "Authorization header is not present"


def test_should_pull_correct_header_off_request(jwt_access_token_authentication_scenario):
    # Arrange
    factory, backend, _ = jwt_access_token_authentication_scenario
    headers = {
        "HTTP_AUTHORIZATION": "Salt addicted",
    }
    request = factory.get("/test-url/", **headers)
    # Act
    with pytest.raises(AuthenticationFailed) as authentication_failed_exception:
        backend.authenticate(request)
    # Assert
    assert authentication_failed_exception.value.status_code == 401
    assert (
        authentication_failed_exception.value.detail
        == "Authorization header must start with Bearer followed by its token"
    )


def test_should_return_jwt_user(jwt_access_token_authentication_scenario):
    # Arrange
    factory, backend, token = jwt_access_token_authentication_scenario
    headers = {
        "HTTP_AUTHORIZATION": f"Bearer {token}",
    }
    request = factory.get("/test-url/", **headers)
    expected_token = {
        "iss": "https://jsm-sandbox-dev1.us.auth0.com/",
        "sub": "auth0|61e466c0ae29b30076468b30",
        "aud": ["https://user-management/django-api/", "https://jsm-sandbox-dev1.us.auth0.com/userinfo"],
        "iat": 1643572594,
        "exp": 1643658994,
        "azp": "lt2ZiOvD52n4Y3zzQ4340fIAE4JGRnU8",
        "scope": "openid profile email",
    }
    # Act
    result = backend.authenticate(request)
    # Assert
    assert result == (TokenUser(expected_token), expected_token)
