import logging

from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from product_a_regular_web_app.apps.core.api.api_exception import ContractNotRespectedException
from product_a_regular_web_app.apps.core.services.auth0_handler import management_api
from product_a_regular_web_app.apps.core.services.oidc_provider import OIDCProvider

logger = logging.getLogger(__name__)


@api_view(["GET"])
def handle_response_oidc(request: Request) -> Response:
    current_referer = request.headers.get("referer")
    logger.info("Handling callback! It came from %s", current_referer)

    auth_flow_details: dict = request.session.pop("authorization-code", {})
    code = request.query_params.get("code")
    state = request.query_params.get("state")

    if not code or not state or not auth_flow_details:
        raise ContractNotRespectedException
    if auth_flow_details["state"] != state:
        raise ContractNotRespectedException

    logger.info("We have everything to contact token endpoint!")
    tokens, claims = OIDCProvider.acquire_token_by_auth_code_flow(code, auth_flow_details["redirect_uri"])

    # If this is true, then it came from linking account flow
    user_id = auth_flow_details.get("user_id")
    if user_id:
        authenticated_target_user_id = claims["sub"]
        skip_accounting_linking = user_id != authenticated_target_user_id
        if skip_accounting_linking:
            logger.warning("Skipping account linking as the authenticated user is different than target linking user")
        else:
            target_id_token = tokens["id_token"]
            primary_user_id = request.session["user"]["sub"]
            result = management_api.link_accounts(primary_user_id, target_id_token)
            logger.debug("Accounts have been linked! Details: %s", result)
    else:
        request.session["user"] = claims
        request.session["tokens"] = tokens
    location_index = reverse("index")

    return redirect(location_index)


@api_view(["GET"])
def retrieve_user_info(request: Request) -> Response:
    tokens = request.session.get("tokens")
    result = OIDCProvider.get_user_info(tokens["access_token"])

    return Response(data=result)
