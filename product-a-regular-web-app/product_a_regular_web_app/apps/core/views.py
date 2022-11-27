import logging
import uuid

from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from product_a_regular_web_app.apps.core.services.auth0_handler import management_api
from product_a_regular_web_app.apps.core.services.oidc_provider import OIDCProvider

logger = logging.getLogger(__name__)


def index(request):
    logged_user = request.session.get("user")
    context = {}

    if logged_user:
        logout_request_path = _build_uri(request, "logout")
        final_logout_uri = OIDCProvider.build_logout_url(logout_request_path)
        # Enriching output
        context["logout_uri"] = final_logout_uri
        user_id, email = logged_user["sub"], logged_user["email"]
        email_verified = logged_user.get("email_verified")
        should_retrieve_other_accounts_with_same_email = email_verified and email_verified is True
        user_details = management_api.retrieve_user_details(user_id)
        suggested_users = None
        if should_retrieve_other_accounts_with_same_email:
            result = management_api.retrieve_users_with_same_verified_email(user_id, email)
            suggested_users = result["users"]
        context = {
            "logout_uri": final_logout_uri,
            "user_details": user_details,
            "suggested_users": suggested_users,
        }

    return render(request, "core/pages/home.html", context)


def logout(request):
    request.session.flush()
    redirect_uri = _build_uri(request, "index")
    return redirect(redirect_uri)


def initiate_login_flow(request):
    redirect_uri = _build_uri(request, "v1/response-oidc")
    logger.info("Building flow session details...")
    some_state = str(uuid.uuid4())
    # So we can retrieve it later
    request.session["authorization-code"] = {"state": some_state, "redirect_uri": redirect_uri}
    # Then we redirect the user
    auth_uri = OIDCProvider.build_authorization_url(redirect_uri, some_state)
    return redirect(auth_uri)


def link_account(request):
    logger.info("Initializing linking account...")
    if request.method == "POST":
        # Essential parameters
        user_id = request.POST["userId"]
        email = request.POST["email"]
        connection = request.POST["connection"]
        params = {
            # https://auth0.com/docs/connections/pass-parameters-to-idps#field-list
            # https://community.auth0.com/t/does-login-hint-work-for-new-universal-login/44390/4
            # Let's say, it is used to fill an input with the provided value
            "login_hint": email,
            # It means "Maximum Authentication Age".
            # Specifies the allowable elapsed time in seconds since the last time the End-User was actively authenticated by the OP
            # https://openid.net/specs/openid-connect-core-1_0.html#ServerMTI
            "max_age": 0,
            # https://community.auth0.com/t/passing-data-to-the-hosted-login-page-with-solution/28243
            # This one will work like "allowed connections to be accepted" on the Identity Provider side
            "connection": connection,
        }
        # Stuff required to build the final URL
        redirect_uri = _build_uri(request, "v1/response-oidc")
        some_state = str(uuid.uuid4())
        # So we can retrieve it later
        request.session["authorization-code"] = {"state": some_state, "redirect_uri": redirect_uri, "user_id": user_id}

        auth_uri = OIDCProvider.build_authorization_url(redirect_uri, some_state, params)
        return redirect(auth_uri)
    else:
        redirect_uri = _build_uri(request, "index")
        return redirect(redirect_uri)


def unlink_account(request):
    logger.info("Initializing unlinking account...")
    redirect_uri = _build_uri(request, "index")

    if request.method == "POST":
        logged_user = request.session["user"]
        primary_user_id = logged_user["sub"]
        # Essential parameters
        target_provider = request.POST["targetProvider"]
        target_user_id = request.POST["targetUserId"]
        result = management_api.unlink_accounts(primary_user_id, target_provider, target_user_id)
        logger.debug("Accounts have been unlinked! Details: %s", result)

    return redirect(redirect_uri)


def _build_uri(request, view_name):
    location_redirect = reverse(view_name)
    return request.build_absolute_uri(location_redirect)
