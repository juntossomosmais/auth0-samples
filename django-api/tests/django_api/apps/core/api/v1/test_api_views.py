import pytest

from pytest_mock import MockFixture

from django_api.apps.core.api.authentication.authentications import JWTAccessTokenAuthentication
from django_api.apps.core.models import AuditAction


@pytest.fixture
def accept_fake_access_token(mocker: MockFixture):
    mocker.patch.object(JWTAccessTokenAuthentication, "_provide_jwks_client", mocker.MagicMock)
    mocked_jwt = mocker.patch("django_api.apps.core.api.authentication.authentications.jwt")
    fake_data = {
        "iss": "https://jsm-sandbox-dev1.us.auth0.com/",
        "sub": "auth0|61e466c0ae29b30076468b30",
        "aud": ["https://user-management/django-api/", "https://jsm-sandbox-dev1.us.auth0.com/userinfo"],
        "iat": 1643572594,
        "exp": 1643658994,
        "azp": "lt2ZiOvD52n4Y3zzQ4340fIAE4JGRnU8",
        "scope": "openid profile email",
    }
    mocked_jwt.decode.return_value = fake_data
    return fake_data


def test_should_return_400_as_no_property_has_been_sent(accept_fake_access_token, client):
    # Arrange
    fake_data = {}
    header = {
        "HTTP_AUTHORIZATION": "Bearer fake-token",
    }
    # Act
    response = client.post("/api/v1/users/attributes", content_type="application/json", data=fake_data, **header)
    # Assert
    result = response.json()
    assert response.status_code == 400
    assert result == {"non_field_errors": ["At least one property should be set!"]}


@pytest.mark.django_db
def test_should_return_200_with_new_full_name(accept_fake_access_token, client):
    # Arrange
    fake_user_data = accept_fake_access_token
    fake_data = {
        "full_name": "Jafar Iago",
        "user_metadata": {"birthday": "1985-06-23"},
    }
    header = {
        "HTTP_AUTHORIZATION": "Bearer fake-token",
    }
    # Act
    response = client.post("/api/v1/users/attributes", content_type="application/json", data=fake_data, **header)
    # Assert
    assert response.status_code == 200
    assert AuditAction.objects.count() == 1
    created_audit_action: AuditAction = AuditAction.objects.first()
    assert created_audit_action.ip_address == None
    assert created_audit_action.user_id == fake_user_data["sub"]
    assert created_audit_action.action == "save_new_properties"
    assert created_audit_action.success


def test_should_return_200_with_user_attributes(accept_fake_access_token, client):
    # Arrange
    header = {
        "HTTP_AUTHORIZATION": "Bearer fake-token",
    }
    # Act
    response = client.get("/api/v1/users/attributes", content_type="application/json", **header)
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert result == {
        "full_name": None,
        "given_name": "Curt",
        "family_name": "Smith",
        "user_metadata": {"birthday": "1985-06-23", "city": "São Paulo", "gender": "masculine", "state": "SP"},
    }
