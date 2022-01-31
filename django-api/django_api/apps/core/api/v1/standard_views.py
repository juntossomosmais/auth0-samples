import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django_api.apps.core.api.authentication.authentications import JWTAccessTokenAuthentication
from django_api.apps.core.api.permissions import IsSameUser
from django_api.apps.core.api.v1.serializers import UserAttributesSerializer
from django_api.apps.core.providers.auth0_provider import management_api
from django_api.apps.core.services import profile_manager

_logger = logging.getLogger(__name__)


class UserManagementAttributesAPIView(APIView):
    authentication_classes = [JWTAccessTokenAuthentication]

    def post(self, request):
        user_id = request.user.id
        _logger.debug("The following user is trying to refresh his attributes: %s", user_id)
        serializer = UserAttributesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        profile_manager.save_new_properties(user_id, serializer.validated_data)

        return Response(status=status.HTTP_200_OK)

    def get(self, request):
        user_id = request.user.id
        _logger.debug("The following user is trying to retrieve his attributes: %s", user_id)
        user_details = management_api.retrieve_user(user_id)
        body = {
            "full_name": user_details.get("name"),
            "given_name": user_details.get("given_name"),
            "family_name": user_details.get("family_name"),
            "user_metadata": user_details.get("user_metadata"),
        }
        return Response(body, status=status.HTTP_200_OK)
