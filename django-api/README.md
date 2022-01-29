# Django API

How do you create an API that can only be accessed with a valid access token? Check out this project and understand how it works behind the curtain.

## Notes

1. The authentication process method was copied from [jazzband/djangorestframework-simplejwt](https://github.com/jazzband/djangorestframework-simplejwt), but heavily changed to meet our criteria. [JWTTokenUserAuthentication backend](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/experimental_features.html) is indeed a great idea.

## Interesting links

Auth0 community:

- [How to allow the end-user to update their own profile information?](https://community.auth0.com/t/how-to-allow-the-end-user-to-update-their-own-profile-information/6228?u=willianantunes)
- [End Users Ability to update Profile](https://community.auth0.com/t/end-users-ability-to-update-profile/47022?u=willianantunes)
- [Understanding how the “audience” concept actually works](https://community.auth0.com/t/understanding-how-the-audience-concept-actually-works/34011?u=willianantunes)

Auth0 documentation:

- [Understanding user profiles](https://auth0.com/docs/manage-users/user-accounts/user-profiles)
- [Understand How Metadata Works in User Profiles](https://auth0.com/docs/manage-users/user-accounts/metadata)
- [Update Root Attributes for Users](https://auth0.com/docs/manage-users/user-accounts/user-profiles/root-attributes/update-root-attributes-for-users)

Auth0 blog:

- [Working with Auth0 User Profile Information and Metadata in Android Apps](https://auth0.com/blog/working-auth0-user-profile-information-metadata-android-apps/)

GitHub issues:

- [Caching of key set in PyJWKClient](https://github.com/jpadilla/pyjwt/issues/615)

Others:

- [Retrieve RSA signing keys from a JWKS endpoint](https://pyjwt.readthedocs.io/en/latest/usage.html?highlight=PyJWKClient#retrieve-rsa-signing-keys-from-a-jwks-endpoint)
