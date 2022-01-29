import logging

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.request import Request
from rest_framework.response import Response

from django_api.apps.core.api.authentication.authentications import JWTAccessTokenAuthentication
from django_api.apps.core.api.permissions import IsSameUser
from django_api.apps.core.api.v1.serializers import UserAttributesSerializer
from django_api.apps.core.providers.auth0_provider import management_api
from django_api.apps.core.services import profile_manager

_logger = logging.getLogger(__name__)


@api_view(["POST"])
@authentication_classes([JWTAccessTokenAuthentication])
@permission_classes([IsSameUser])
def refresh_user_attributes(request: Request) -> Response:
    _logger.debug("The following user is trying to refresh his attributes: %s", request.user.id)
    serializer = UserAttributesSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    profile_manager.save_new_properties(serializer.validated_data)

    return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([JWTAccessTokenAuthentication])
@permission_classes([IsSameUser])
def retrieve_user_attributes(request: Request, user_id: str) -> Response:
    _logger.debug("The following user is trying to retrieve his attributes: %s", request.user.id)
    user_details = management_api.retrieve_user(user_id)
    body = {
        "full_name": user_details.get("full_name"),
        "given_name": user_details.get("given_name"),
        "family_name": user_details.get("family_name"),
        "user_metadata": user_details.get("user_metadata"),
    }
    return Response(body, status=status.HTTP_200_OK)
