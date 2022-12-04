# Auth0 Samples: Demystify all your doubts about how to integrate with Auth0 

In this repository, you'll find:

- **custom-universal-login**: A project that has a custom universal login using [Auth0.js](https://github.com/auth0/auth0.js), React and [Parcel](https://parceljs.org/). You can easily change it to [Lock.js](https://github.com/auth0/lock) if required. This has nothing to do with New Universal Login, which uses Liquid as template engine. [Know the differences](https://auth0.com/docs/login/universal-login/new-universal-login-vs-classic-universal-login).
- **product-a-regular-web-app**: A sample application that represents some sort of product written in Python using [Django as template engine](https://docs.djangoproject.com/en/4.0/topics/templates/).
- **product-b-regular-web-app**: A sample application that represents some sort of product written in C# using [ASP.NET Core MVC](https://docs.microsoft.com/en-us/aspnet/core/mvc/overview?view=aspnetcore-6.0).
- **product-c-single-page-app**: A sample application that represents some sort of product written in JavaScript using [Next.js](https://nextjs.org/).
- **django-api**: API responsible for manage user properties. It's written in Python using Django and [DRF](https://www.django-rest-framework.org/).

[The Authorization Code grant type](https://auth0.com/docs/authorization/flows/authorization-code-flow) is used by the products to authenticate the user.

## Why 3 products?

So you can see how SSO (single sign-on) works. In addition, you can check out the code and understand the logic behind the curtain.

## Configuring the environment

To run all the products, you are not required to configure the custom universal login, as the new universal login enables everything. The following section explains how to configure the custom universal login, which is optional, and then how to run the products.

### Optional: Custom Universal Login

The Custom Universal Login requires storage to upload its static files. However, only the HTTP files are uploaded to Auth0, and they reference the static files stored on AWS S3. 

#### Creating the S3 bucket

To create a properly configured S3 bucket, access the folder [custom-universal-login-s3-iac](./custom-universal-login-s3-iac) and set everything that starts with `YOUR_`. Then, execute the command:

    terraform init

Then you can apply it:

    terraform apply

You'll see this message when it ends:

```
Apply complete! Resources: 7 added, 0 changed, 0 destroyed.
```

#### Uploading the custom universal login

Please configure all the variables available in[.env](./.env) file. To build and upload the front-end project, you can issue the following command:

> ⚠ It's worth mentioning that a build is required in case you have changed any project. That is why the commands below have the build flag.

    docker-compose build apply-classic-page && docker-compose up apply-classic-page

Then you should access your Auth0 tenant to configure 1 manual steps:

- In `Branding > Universal Login > Advanced Options` go to the `Login` tab and click on `Customize Login Page` button.

### Required: Running the products A, B, C, and the API

Please configure all the variables in the section `Auth0 Management API stuff` in the [.env](./.env) file. To configure all `env.development` files, execute the command:

    docker-compose build update-settings && docker-compose up update-settings

Now you can run the products including the API:

    docker-compose build product-a product-b product-c django-api && docker-compose up product-a product-b product-c django-api 

You can access them through the following addresses:

- Product A: http://app.local:8000
- Product B: http://app.local:8001
- Product C: https://app.local:8002
- Django API: https://app.local:8010/admin

Use `admin:admin` to access the Django ADMIN!

## FAQ

1. Why `app.local` instead of `localhost`?

[To skip user consent](https://community.auth0.com/t/skip-user-consent-when-using-social-connection/18061) when doing authorization code grant type. You can test it using `localhost`, but you should understand it upfront from us.

2. I want to use this project. How do I configure the application required by Auth0 Deploy CLI?

You must create an application of type M2M and then grant access to certain scopes to the audience `YOUR_TENANT_NAME.us.auth0.com/api/v2/`. If you consult the endpoint [_Get client grants_](https://auth0.com/docs/api/management/v2#!/Client_Grants/get_client_grants) you should see something like the following:

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

3. An env file is present in all sample product projects. Do I need to touch them for something?

This is not required. [They will be automatically updated by the orchestrator](./orchestrator/scripts/env_setter.py).

4. I'm using an Apple M1 chip and receiving weird errors such as `gyp ERR!` from `product-a`. What do I do?

Sadly we're using images that don't support M1 architecture. So for this particular case, we recommend you run other products and leave the one that doesn't work aside.
