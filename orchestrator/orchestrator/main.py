import pathlib

from dataclasses import dataclass

from orchestrator import settings
from orchestrator.auth0_handler import management_api
from orchestrator.models import AppType
from orchestrator.settings_handler import refresh_settings

auth0_api_audience = f"https://{settings.AUTH0_DOMAIN}/api/v2/"
django_api_audience = "https://user-management/django-api/api/v1"


class UnexpectedBehaviorException(Exception):
    pass


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
            "NEXT_PUBLIC_SOCIAL_AUTH_AUTH0_KEY": client_details.client_id,
            "Auth0__ClientId": client_details.client_id,
            "SOCIAL_AUTH_AUTH0_SECRET": client_details.client_secret,
            "NEXT_PUBLIC_SOCIAL_AUTH_AUTH0_SECRET": client_details.client_secret,
            "Auth0__ClientSecret": client_details.client_secret,
            "SOCIAL_AUTH_AUTH0_DOMAIN": f"{client_details.tenant}.us.auth0.com",
            "NEXT_PUBLIC_SOCIAL_AUTH_AUTH0_DOMAIN": f"{client_details.tenant}.us.auth0.com",
            "Auth0__Domain": f"{client_details.tenant}.us.auth0.com",
            "AUTH0_USER_MANAGEMENT_AUDIENCE": django_api_audience,
            "NEXT_PUBLIC_AUTH0_USER_MANAGEMENT_AUDIENCE": django_api_audience,
            # APIs
            "AUTH0_DOMAIN": f"{client_details.tenant}.us.auth0.com",
            "AUTH0_MY_APPLICATION_AUDIENCE": django_api_audience,
            "AUTH0_MY_APPLICATION_KEY": client_details.client_id,
            "AUTH0_MY_APPLICATION_SECRET": client_details.client_secret,
        }
        refresh_settings(file_location_path, find_key_and_replace_for_value)
    else:
        print(f"The following file does not exist to update setting: {file_location_path}")


def retrieve_id_by_connection_name(connections, name):
    for connection in connections:
        if connection["name"] == name:
            return connection["id"]
    raise UnexpectedBehaviorException


def main():
    # Control variables
    product_a_client, product_b_client, product_c_client, django_api_client = None, None, None, None

    print("Retrieving configuration from clients A, B, C, and Django API, if available")
    clients = management_api.retrieve_all_clients(fields=["client_secret", "client_id", "tenant", "name"])
    for client in clients:
        if client["name"].lower() == settings.PRODUCT_A_NAME.lower():
            product_a_client = ClientDetails.build_from_raw_client(client)
            continue
        if client["name"].lower() == settings.PRODUCT_B_NAME.lower():
            product_b_client = ClientDetails.build_from_raw_client(client)
            continue
        if client["name"].lower() == settings.PRODUCT_C_NAME.lower():
            product_c_client = ClientDetails.build_from_raw_client(client)
            continue
        if client["name"].lower() == settings.DJANGO_API_NAME.lower():
            django_api_client = ClientDetails.build_from_raw_client(client)
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
        # Only product A will use M2M communication
        scope = ["read:users", "update:users"]
        management_api.create_client_grant(product_a_client.client_id, auth0_api_audience, scope)
    if not product_b_client:
        print("Creating product B!")
        my_service_address = "app.local:8001"
        allowed_logout_urls = [f"https://{my_service_address}/"]
        callbacks = [f"https://{my_service_address}/Account/Callback"]
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
            "web_origins": configuration_for_all,
        }
        created_client = management_api.create_client(settings.PRODUCT_C_NAME, AppType.SPA, **extra_options)
        product_c_client = ClientDetails.build_from_raw_client(created_client)
    if not django_api_client:
        print("Creating Django API client!")
        created_client = management_api.create_client(settings.DJANGO_API_NAME, AppType.NON_INTERACTIVE)
        django_api_client = ClientDetails.build_from_raw_client(created_client)
        # So the custom API can invoke Auth0 Management API!
        scope = [
            "read:users",
            "update:users",
            "delete:users",
            "create:users",
            "read:users_app_metadata",
            "update:users_app_metadata",
            "delete:users_app_metadata",
            "create:users_app_metadata",
            "read:user_custom_blocks",
            "create:user_custom_blocks",
            "delete:user_custom_blocks",
        ]
        management_api.create_client_grant(django_api_client.client_id, auth0_api_audience, scope)

    # Custom resource server for DJANGO API
    name = "Management - Orchestrate - Django API"
    identifier = django_api_audience
    resource_servers = management_api.all_resource_servers()
    has_resource_server_registered = False
    for rs in resource_servers:
        if rs["identifier"] == identifier:
            print(f"No need for creating resource server: {identifier}")
            has_resource_server_registered = True
    if not has_resource_server_registered:
        print(f"Creating resource server with identifier: {identifier}")
        management_api.create_resource_server(name, identifier)
        scope = ["read:users", "update:users"]

    # Updating application settings
    where_settings_is_product_a = settings.PRODUCT_A_ENV_FILE
    update_settings(where_settings_is_product_a, product_a_client)

    where_settings_is_product_b = settings.PRODUCT_B_ENV_FILE
    update_settings(where_settings_is_product_b, product_b_client)

    where_settings_is_product_c = settings.PRODUCT_C_ENV_FILE
    update_settings(where_settings_is_product_c, product_c_client)

    where_settings_is_django_api = settings.DJANGO_API_ENV_FILE
    update_settings(where_settings_is_django_api, django_api_client)

    # Apply custom email provider
    email_provider = management_api.current_email_provider()
    if not email_provider:
        arguments = {
            "default_from_address": settings.AUTH0_EMAIL_PROVIDER_FROM,
            "smtp_host": settings.AUTH0_EMAIL_SMTP_HOST,
            "smtp_port": settings.AUTH0_EMAIL_SMTP_PORT,
            "smtp_user": settings.AUTH0_EMAIL_SMTP_USER,
            "smtp_pass": settings.AUTH0_EMAIL_SMTP_PASSWORD,
        }
        management_api.configure_email_provider(**arguments)

    # Control variables
    database_connection = "Username-Password-Authentication"
    google_connection = "google-oauth2"
    facebook_connection = "facebook"
    passwordless_email_connection = "email"
    enabled_clients = [product_a_client.client_id, product_b_client.client_id, product_c_client.client_id]
    # Create connections to enable social login
    connections = management_api.retrieve_all_connection()
    connections_number = len(connections)
    only_auth0_strategy_available = connections_number == 1
    if only_auth0_strategy_available:
        print("Creating connections for facebook, google and passwordless")
        management_api.create_connection(google_connection, google_connection, enabled_clients)
        management_api.create_connection(facebook_connection, facebook_connection, enabled_clients)
        management_api.create_connection(passwordless_email_connection, passwordless_email_connection, enabled_clients)
    else:
        print(f"Updating connections with the enabled clients. Current number: {connections_number}")
        fields = ["id", "strategy", "name"]
        connections = management_api.retrieve_all_connection(fields=fields)
        google_connection_id = retrieve_id_by_connection_name(connections, google_connection)
        facebook_connection_id = retrieve_id_by_connection_name(connections, facebook_connection)
        passwordless_email_connection_id = retrieve_id_by_connection_name(connections, passwordless_email_connection)
        management_api.update_connection_with_clients(google_connection_id, enabled_clients)
        management_api.update_connection_with_clients(facebook_connection_id, enabled_clients)
        management_api.update_connection_with_clients(passwordless_email_connection_id, enabled_clients)

    # Update main connection if required to allow username usage
    fields = ["id", "name", "strategy"]
    connections = management_api.retrieve_all_connection(fields=fields, connection_name="auth0")
    database_connection_id = retrieve_id_by_connection_name(connections, database_connection)
    print(f"Allowing usage of username in {database_connection}...")
    try:
        management_api.update_connection_to_enable_username(database_connection_id, "auth0")
    except Exception:
        print("Could not configure database to allow username!")
