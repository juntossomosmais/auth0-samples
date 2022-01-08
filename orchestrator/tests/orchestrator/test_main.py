import unittest

from pathlib import Path

from orchestrator.file_helper import load_content_as_string
from orchestrator.main import ClientDetails
from orchestrator.main import update_settings


class MainTests(unittest.TestCase):
    def test_should_refresh_file_with_provided_settings(self):
        # Arrange
        file_location = "../../../product-a-regular-web-app/.env.development"
        fake_client_details = ClientDetails("fake_client_id", "fake_client_secret", "fake_tenant")
        # Act
        update_settings(file_location, fake_client_details)
        # Assert
        file_location_path = Path(file_location)
        content = load_content_as_string(file_location_path, break_lines=True)
        assert (
            content
            == """##################
#### Auth0
SOCIAL_AUTH_AUTH0_KEY=fake_client_id
SOCIAL_AUTH_AUTH0_SECRET=fake_client_secret
SOCIAL_AUTH_AUTH0_DOMAIN=fake_tenant.us.auth0.com
SOCIAL_AUTH_AUTH0_SCOPE=openid,profile,email
"""
        )
