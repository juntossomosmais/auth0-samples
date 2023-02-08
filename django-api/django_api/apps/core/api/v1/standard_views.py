import logging

from apps.core.api.api_exception import InvalidContractException
from apps.core.api.api_exception import UnauthorizedException
from apps.core.providers.auth0_provider import resource_owner
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django_api.apps.core.api.authentication.authentications import JWTAccessTokenAuthentication
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

        data = serializer.validated_data
        email = data.get("email")
        # TODO: Compare if the provided email is different than the current one
        if email:
            password = data.get("password")
            current_email = data.get("current_email")
            if not password and not current_email:
                raise InvalidContractException
            if not resource_owner(current_email, password):
                raise UnauthorizedException
            del data["password"]
            del data["current_email"]
        profile_manager.save_new_properties(user_id, data)

        # TODO: Return current user settings
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
            "email": user_details.get("email"),
        }
        return Response(body, status=status.HTTP_200_OK)
