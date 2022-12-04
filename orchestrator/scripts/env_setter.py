import fileinput
import json
import os
import pathlib

from dataclasses import dataclass
from pathlib import Path

from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
auth0_endpoint = f"https://{AUTH0_DOMAIN}/api/v2/"
get_token = GetToken(AUTH0_DOMAIN)


def _yielding_all_matching_files_from_directory(folder, glob_pattern) -> list[Path]:
    return list(pathlib.Path(folder).glob(glob_pattern))


def _refresh_settings(settings_location, key_value_to_replace: dict[str, str]):
    for line in fileinput.input(settings_location, inplace=True):
        replaced = False
        for key_to_be_found in key_value_to_replace:
            if line.startswith(key_to_be_found):
                value = key_value_to_replace[key_to_be_found]
                replaced = True
                print(f"""{key_to_be_found}={value}\n""", end="")
                break
        if not replaced:
            print(line, end="")


def _load_content_as_string(file_name) -> str:
    with open(file_name, mode="r") as file:
        return "".join(line.rstrip() for line in file)


def _load_content_from_json_file_as_dict(file_path: str):
    file_path = pathlib.Path(file_path)

    with open(file_path, "r") as file:
        return json.load(file)


class UnexpectedBehaviorException(Exception):
    pass


@dataclass(frozen=True)
class ClientDetails:
    client_id: str
    client_secret: str
    name: str
    tenant: str


if __name__ == "__main__":
    print("Getting all env files")
    files = _yielding_all_matching_files_from_directory("./envs", "**/*.env.development")
    assert len(files) == 4, "Four environment files should have been found!"
    print("Creating Auth0 Management API Client")
    token = get_token.client_credentials(AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, auth0_endpoint)
    auth0 = Auth0(AUTH0_DOMAIN, token["access_token"])
    print("Gathering needed data")
    django_api, product_a, product_b, product_c = None, None, None, None
    clients = auth0.clients.all(fields=["client_secret", "client_id", "tenant", "name"])
    for client in clients:
        client_name = client["name"].lower()
        if client_name == "Management - Orchestrate - Django API".lower():
            django_api = ClientDetails(**client)
        elif client_name == "Product A".lower():
            product_a = ClientDetails(**client)
        elif client_name == "Product B".lower():
            product_b = ClientDetails(**client)
        elif client_name == "Product C".lower():
            product_c = ClientDetails(**client)
    if None in [django_api, product_a, product_b, product_c]:
        raise UnexpectedBehaviorException("Couldn't retrieve Django API or some of the products")
    print("Creating templates to apply configuration")
    django_api_audience = "https://user-management/django-api/api/v1"
    django_api_env_variables = {
        "AUTH0_DOMAIN": AUTH0_DOMAIN,
        "AUTH0_MY_APPLICATION_AUDIENCE": django_api_audience,
        "AUTH0_MY_APPLICATION_KEY": django_api.client_id,
        "AUTH0_MY_APPLICATION_SECRET": django_api.client_secret,
    }
    product_a_env_variables = {
        "SOCIAL_AUTH_AUTH0_DOMAIN": AUTH0_DOMAIN,
        "SOCIAL_AUTH_AUTH0_KEY": product_a.client_id,
        "SOCIAL_AUTH_AUTH0_SECRET": product_a.client_secret,
    }
    product_b_env_variables = {
        "Auth0__Domain": AUTH0_DOMAIN,
        "Auth0__ClientId": product_b.client_id,
        "Auth0__ClientSecret": product_b.client_secret,
    }
    product_c_env_variables = {
        "SOCIAL_AUTH_AUTH0_DOMAIN": AUTH0_DOMAIN,
        "NEXT_PUBLIC_SOCIAL_AUTH_AUTH0_DOMAIN": AUTH0_DOMAIN,
        "SOCIAL_AUTH_AUTH0_KEY": product_c.client_id,
        "NEXT_PUBLIC_SOCIAL_AUTH_AUTH0_KEY": product_c.client_id,
        "AUTH0_USER_MANAGEMENT_AUDIENCE": django_api_audience,
        "NEXT_PUBLIC_AUTH0_USER_MANAGEMENT_AUDIENCE": django_api_audience,
    }
    print("Applying configuration")
    number_of_updates = 0
    for file in files:
        file_name = str(file)
        if "django-api" in file_name:
            _refresh_settings(file, django_api_env_variables)
            number_of_updates += 1
        if "product-a" in file_name:
            _refresh_settings(file, product_a_env_variables)
            number_of_updates += 1
        if "product-b" in file_name:
            _refresh_settings(file, product_b_env_variables)
            number_of_updates += 1
        if "product-c" in file_name:
            _refresh_settings(file, product_c_env_variables)
            number_of_updates += 1
    assert number_of_updates == 4, "I should have updated 4 files. Did I do something wrong? 🤨"
    print("Done 🥳")
