# Product C SPA

This represents a sample product from a company that uses the authorization code grant type to authenticate a user against an identity provider.

It uses the [Auth0 SDK for React Single Page Applications (SPA)](https://github.com/auth0/auth0-react), **handling everything client-side**. In addition, you can use another library dedicated to Next.js known as [auth0/nextjs-auth0](https://github.com/auth0/nextjs-auth0). **This dedicated library would allow you to redirect the user on the server side**. Look at [this architecture](https://github.com/auth0/nextjs-auth0/blob/70f59193b637ba5c5525359282b3c78b555b286b/ARCHITECTURE.md) as a reference.

## Running the project

You should just execute the following:

    npm run dev-ssl

Why HTTPS? Because of [this](https://github.com/auth0/auth0-spa-js/blob/1390ff8c00790894978eb713a38deaac5ecfe235/FAQ.md#why-do-i-get-auth0-spa-js-must-run-on-a-secure-origin).

You can access your server through https://app.local:8002/.

## Interesting links

- [Next.js with HTTPS](https://github.com/vercel/next.js/discussions/10935#discussioncomment-1540436)
- [The Ultimate Guide to Next.js Authentication with Auth0](https://auth0.com/blog/ultimate-guide-nextjs-authentication-auth0/)

## Notes

1. To do silent authentication, you need to register your service address as a valid one in the **Allowed Web Origins** property.
