import logging

from datetime import date
from typing import TypedDict
from typing import Union

from auth0.v3.exceptions import Auth0Error

from django_api.apps.core.models import AuditAction
from django_api.apps.core.providers.auth0_provider import management_api

_logger = logging.getLogger(__name__)


class UserMetadata(TypedDict):
    city: str
    state: str
    birthday: Union[date, str]
    gender: str


class UserAttributes(TypedDict):
    user_id: str
    user_metadata: UserMetadata
    full_name: str
    given_name: str
    family_name: str


def save_new_properties(user_id: str, user_attributes: UserAttributes):
    _logger.debug("Saving properties for the user %s", user_id)
    user_metadata = user_attributes.get("user_metadata")
    if user_metadata:
        birthday = user_metadata.get("birthday")
        if birthday:
            user_metadata["birthday"] = birthday.isoformat()
    try:
        result = management_api.update_user(user_id, **user_attributes)
        _logger.debug("Result from Auth0: %s", result)
        AuditAction(user_id=user_id, action=save_new_properties.__name__, success=True).save()
    except Auth0Error as e:
        # TODO: When an existing email is provided, you'll receive the error 400 followed by the message "The specified new email already exists"
        _logger.exception("%s could not save his attributes")
        extra_values = {"success": False, "motive": f"{e.status_code}: {e.message}"}
        AuditAction(user_id=user_id, action=save_new_properties.__name__, **extra_values).save()
