# Auth0 Samples

In this project, you'll find:

- **custom-universal-login**: A project that has a custom universal login using [Auth0.js](https://github.com/auth0/auth0.js), React and [Parcel](https://parceljs.org/). You can easily change it to [Lock.js](https://github.com/auth0/lock) if required. This has nothing to do with New Universal Login, which uses Liquid as template engine. [Know the differences](https://auth0.com/docs/login/universal-login/new-universal-login-vs-classic-universal-login).
- **product-a-regular-web-app**: A sample application that represents some sort of product written in Python using [Django as template engine](https://docs.djangoproject.com/en/4.0/topics/templates/).
- **product-b-regular-web-app**: A sample application that represents some sort of product written in C# using [ASP.NET Core MVC](https://docs.microsoft.com/en-us/aspnet/core/mvc/overview?view=aspnetcore-6.0).
- **product-c-single-page-app**: A sample application that represents some sort of product written in JavaScript using [Next.js](https://nextjs.org/).

[The Authorization Code grant type](https://auth0.com/docs/authorization/flows/authorization-code-flow) is used by the products to authenticate the user.

## Why 3 products?

So you can see how SSO (single sign-on) works. In addition, you can check out the code and understand the logic behind the curtain.

## Seeing them in action

First you must update the universal login that represents the sandbox tenant. To do that you must issue the following:

    docker-compose up apply-classic-page

Now you can fire up the products! Let's say you'd like to see in action only products A and B:

    docker-compose up product-a product-b

Then you can access them through the following addresses:

- Product A: http://app.local:8000
- Product B: http://app.local:8001

## Why app.local instead of localhost?

[To skip user consent](https://community.auth0.com/t/skip-user-consent-when-using-social-connection/18061) when doing authorization code grant type. You can test it using `localhost`, but you should understand it upfront from us.

## Important notice

You may not see all the projects here as this is still work in progress.
