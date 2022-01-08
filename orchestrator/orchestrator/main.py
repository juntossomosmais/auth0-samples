import pathlib

from dataclasses import dataclass
from typing import Optional

from orchestrator import settings
from orchestrator.auth0_handler import management_api
from orchestrator.models import AppType
from orchestrator.settings_handler import refresh_settings


@dataclass(frozen=True)
class ClientDetails:
    client_id: str
    client_secret: str
    tenant: str

    @staticmethod
    def build_from_raw_client(client):
        return ClientDetails(client["client_id"], client["client_secret"], client["tenant"])


def update_settings(file_location, client_details: ClientDetails):
    file_location_path = pathlib.Path(file_location).resolve()
    if file_location_path.exists():
        print(f"Updating settings for the following file: {file_location_path}")
        find_key_and_replace_for_value = {
            "SOCIAL_AUTH_AUTH0_KEY": client_details.client_id,
            "SOCIAL_AUTH_AUTH0_SECRET": client_details.client_secret,
            "SOCIAL_AUTH_AUTH0_DOMAIN": f"{client_details.tenant}.us.auth0.com",
        }
        refresh_settings(file_location_path, find_key_and_replace_for_value)
    else:
        print(f"The following file does not exist to update setting: {file_location_path}")


def main():
    # Control variables
    product_a_client, product_b_client, product_c_client = None, None, None

    print("Retrieving configuration from clients A, B and C, if available")
    clients = management_api.retrieve_all_clients()
    for client in clients:
        if client["name"].lower() == settings.PRODUCT_A_NAME:
            product_a_client = ClientDetails.build_from_raw_client(client)
            continue
        if client["name"].lower() == settings.PRODUCT_B_NAME:
            product_b_client = ClientDetails.build_from_raw_client(client)
            continue
        if client["name"].lower() == settings.PRODUCT_C_NAME:
            product_c_client = ClientDetails.build_from_raw_client(client)
            continue

    # Create clients only if this is required
    if not product_a_client:
        print("Creating product A!")
        my_service_address = "app.local:8000"
        allowed_logout_urls = [f"http://{my_service_address}/logout"]
        callbacks = [f"http://{my_service_address}/api/v1/response-oidc"]
        extra_options = {"allowed_logout_urls": allowed_logout_urls, "callbacks": callbacks}
        created_client = management_api.create_client(settings.PRODUCT_A_NAME, AppType.REGULAR_WEB, **extra_options)
        product_a_client = ClientDetails.build_from_raw_client(created_client)
    if not product_b_client:
        print("Creating product B!")
        my_service_address = "app.local:8001"
        allowed_logout_urls = [f"https://{my_service_address}/"]
        callbacks = [f"https://{my_service_address}/v1/auth/response-oidc"]
        extra_options = {"allowed_logout_urls": allowed_logout_urls, "callbacks": callbacks}
        created_client = management_api.create_client(settings.PRODUCT_B_NAME, AppType.REGULAR_WEB, **extra_options)
        product_b_client = ClientDetails.build_from_raw_client(created_client)
    if not product_c_client:
        print("Creating product C!")
        my_service_address = "app.local:8002"
        configuration_for_all = [f"https://{my_service_address}/"]
        extra_options = {
            "allowed_logout_urls": configuration_for_all,
            "callbacks": configuration_for_all,
            "allowed_origins": configuration_for_all,
        }
        created_client = management_api.create_client(settings.PRODUCT_C_NAME, AppType.SPA, **extra_options)
        product_c_client = ClientDetails.build_from_raw_client(created_client)

    # Updating application settings
    where_settings_is_product_a = settings.PRODUCT_A_ENV_FILE
    update_settings(where_settings_is_product_a, product_a_client)

    where_settings_is_product_b = settings.PRODUCT_B_ENV_FILE
    update_settings(where_settings_is_product_b, product_b_client)

    where_settings_is_product_c = settings.PRODUCT_C_ENV_FILE
    update_settings(where_settings_is_product_c, product_c_client)
