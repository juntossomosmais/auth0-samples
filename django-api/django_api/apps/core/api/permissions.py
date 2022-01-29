import logging

from rest_framework import permissions
from rest_framework.request import Request

_logger = logging.getLogger(__name__)


def _is_same_user(source_id, target_id):
    if source_id != target_id:
        _logger.warning("%s is trying to access resources from a different user: %s", source_id, target_id)
        return False
    return True


class IsSameUser(permissions.BasePermission):
    message = "You are not authorized 😬"

    def has_permission(self, request: Request, view):
        defined_user_id_attribute = "user_id"
        user_id_from_query_params = request.query_params.get(defined_user_id_attribute)
        user_id_from_body = request.data.get(defined_user_id_attribute)
        source_user = request.user.id

        if not user_id_from_query_params and not user_id_from_body:
            return False

        if user_id_from_query_params:
            if not _is_same_user(source_user, user_id_from_query_params):
                return False

        if user_id_from_body:
            if not _is_same_user(source_user, user_id_from_body):
                return False

        return True
