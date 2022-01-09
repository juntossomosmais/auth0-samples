from unittest import TestCase

from product_a_regular_web_app.apps.core.services.auth0_handler import management_api


class ManagementAPITests(TestCase):
    def test_should_retrieve_users(self):
        # Arrange
        user_id = "auth0|61ccbb14a0f603006a20e2de"
        email = "willian.lima.antunes@gmail.com"
        # Act
        result = management_api.retrieve_users_with_same_verified_email(user_id, email)
        # Assert
        assert len(result["users"]) == 2

    def test_should_retrieve_user_details(self):
        # Arrange
        user_id = "auth0|61ccbb14a0f603006a20e2de"
        # Act
        result = management_api.retrieve_user_details(user_id)
        # Assert
        assert result == {
            "created_at": "2021-12-29T19:46:28.640Z",
            "email": "willian.lima.antunes@gmail.com",
            "email_verified": True,
            "identities": [
                {
                    "connection": "Username-Password-Authentication",
                    "user_id": "61ccbb14a0f603006a20e2de",
                    "provider": "auth0",
                    "isSocial": False,
                }
            ],
            "name": "willian.lima.antunes@gmail.com",
            "nickname": "willian.lima.antunes",
            "picture": "https://s.gravatar.com/avatar/38ecfbc56718536ca51fcaae7d7da9b3?s=480&r=pg&d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2Fwi.png",
            "updated_at": "2021-12-29T19:46:44.231Z",
            "user_id": "auth0|61ccbb14a0f603006a20e2de",
            "user_metadata": {},
            "username": "53164915055",
        }
