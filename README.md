# Auth0 Samples

In this project, you'll find:

- **custom-universal-login**: A project that has a custom universal login using [Auth0.js](https://github.com/auth0/auth0.js), React and [Parcel](https://parceljs.org/). You can easily change it to [Lock.js](https://github.com/auth0/lock) if required. This has nothing to do with New Universal Login, which uses Liquid as template engine. [Know the differences](https://auth0.com/docs/login/universal-login/new-universal-login-vs-classic-universal-login).
- **product-a-regular-web-app**: A sample application that represents some sort of product written in Python using [Django as template engine](https://docs.djangoproject.com/en/4.0/topics/templates/).
- **product-b-regular-web-app**: A sample application that represents some sort of product written in C# using [ASP.NET Core MVC](https://docs.microsoft.com/en-us/aspnet/core/mvc/overview?view=aspnetcore-6.0).
- **product-c-single-page-app**: A sample application that represents some sort of product written in JavaScript using [Next.js](https://nextjs.org/).
- **django-api**: API responsible for manage user properties. It's written in Python using Django and [DRF](https://www.django-rest-framework.org/).

[The Authorization Code grant type](https://auth0.com/docs/authorization/flows/authorization-code-flow) is used by the products to authenticate the user.

## Why 3 products?

So you can see how SSO (single sign-on) works. In addition, you can check out the code and understand the logic behind the curtain.

## Seeing them in action

To start, please configure the file [.env](./.env).

> ⚠ You are not required to configure all properties in case you don't want the custom universa login.

Now you should update the universal login that represents the sandbox tenant. To do that you can issue the following:

> ⚠ It's worth mentioning that a build is required in case you have changed any project. That is why the commands below have the build flag.

    docker-compose build apply-classic-page && docker-compose up apply-classic-page

Then you should access your Auth0 tenant to configure 1 manual steps:

- In `Branding > Universal Login > Advanced Options` go to the `Login` tab and click on `Customize Login Page` button.

Then update all the `env.development` files in the products by executing the following command:

    docker-compose build update-settings && docker-compose up update-settings

Now you can run the products including the API:

    docker-compose build product-a product-b product-c django-api && docker-compose up product-a product-b product-c django-api 

You can access them through the following addresses:

- Product A: http://app.local:8000
- Product B: http://app.local:8001
- Product C: https://app.local:8002
- Django API: https://app.local:8010/admin

Use `admin:admin` to access Django ADMIN!

## Why app.local instead of localhost?

[To skip user consent](https://community.auth0.com/t/skip-user-consent-when-using-social-connection/18061) when doing authorization code grant type. You can test it using `localhost`, but you should understand it upfront from us.

## FAQ

1. I want to use this project. The S3 part seems OK, but what do I need to do on Auth0?

First you must create an application of type M2M and then grant access to certain scopes to the audience `YOUR_TENANT_NAME.us.auth0.com/api/v2/`. If you consult the endpoint [_Get client grants_](https://auth0.com/docs/api/management/v2#!/Client_Grants/get_client_grants) you should receive something like the following:

```json
{
    "id": "cgr_99YBl1KhuQ2aI5He",
    "client_id": "CAR3cmoBtcNUbHYSHKEmPEUEUBSMs0RI",
    "audience": "https://YOUR_TENANT_NAME.us.auth0.com/api/v2/",
    "scope": [
        "read:client_grants",
        "create:client_grants",
        "delete:client_grants",
        "update:client_grants",
        "read:users",
        "update:users",
        "read:clients",
        "update:clients",
        "delete:clients",
        "create:clients",
        "read:client_keys",
        "read:connections",
        "update:connections",
        "delete:connections",
        "create:connections",
        "read:email_provider",
        "update:email_provider",
        "delete:email_provider",
        "create:email_provider",
        "read:grants",
        "delete:grants",
        "read:resource_servers",
        "update:resource_servers",
        "delete:resource_servers",
        "create:resource_servers"
    ]
}
```

Then you should update the following env files:

- [custom-universal-login/env.development](./custom-universal-login/.env.development)
- [orchestrator/env.development](./orchestrator/.env.development)

Look at them very carefully, otherwise something may no work as expected.

2. I'm receiving error from S3. How do I configure the policy?

It can be many things. If you want something that's been tested and has proof of work, then use [this project](https://github.com/willianantunes/tutorials/blob/27f8ad444b21008c2b960ce922d75cf649225b5e/XXXX/universal-login-s3-terraform/README.md).

If the issue concerns policy, given the bucket name is `juntosid-idp-s3-sandbox`, you can use the one below:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:GetBucketTagging",
                "s3:DeleteObjectVersion",
                "s3:GetObjectVersionTagging",
                "s3:ListBucketVersions",
                "s3:GetBucketLogging",
                "s3:RestoreObject",
                "s3:ListBucket",
                "s3:GetBucketPolicy",
                "s3:ReplicateObject",
                "s3:GetObjectVersionTorrent",
                "s3:GetObjectAcl",
                "s3:GetBucketObjectLockConfiguration",
                "s3:PutBucketTagging",
                "s3:GetBucketRequestPayment",
                "s3:GetObjectVersionAcl",
                "s3:GetObjectTagging",
                "s3:GetBucketOwnershipControls",
                "s3:PutObjectTagging",
                "s3:DeleteObject",
                "s3:PutObjectAcl",
                "s3:GetBucketPublicAccessBlock",
                "s3:GetBucketPolicyStatus",
                "s3:ListBucketMultipartUploads",
                "s3:GetObjectRetention",
                "s3:GetBucketWebsite",
                "s3:PutObjectLegalHold",
                "s3:GetBucketVersioning",
                "s3:PutBucketCORS",
                "s3:GetBucketAcl",
                "s3:GetObjectLegalHold",
                "s3:GetBucketNotification",
                "s3:PutObject",
                "s3:GetObject",
                "s3:ObjectOwnerOverrideToBucketOwner",
                "s3:GetObjectTorrent",
                "s3:PutObjectRetention",
                "s3:PutObjectVersionAcl",
                "s3:GetBucketCORS",
                "s3:PutBucketObjectLockConfiguration",
                "s3:GetObjectVersionForReplication",
                "s3:GetBucketLocation",
                "s3:GetObjectVersion"
            ],
            "Resource": [
                "arn:aws:s3:::juntosid-idp-s3-sandbox/*",
                "arn:aws:s3:::juntosid-idp-s3-sandbox"
            ]
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": "s3:ListAllMyBuckets",
            "Resource": "*"
        }
    ]
}
```

3. An env file is present in all sample product projects. Do I need to touch them for something?

This is not required. [They will be automatically updated by the orchestrator](https://github.com/juntossomosmais/auth0-samples/blob/5e42b109ba23460bf55c457f581a2df041955c4e/orchestrator/orchestrator/main.py#L149-L160).

4. I'm using an Apple M1 chip and receiving weird errors such as `gyp ERR!` from `product-a`. What do I do?

Sadly we're using images that don't support M1 architecture. So for this particular case, we recommend you run other products and leave the one that doesn't work aside.
