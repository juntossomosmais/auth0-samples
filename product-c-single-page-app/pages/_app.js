import React, { useEffect } from "react"
import "bootstrap/dist/css/bootstrap.css"
import Router from "next/router"
import { Auth0Provider } from "@auth0/auth0-react"

const onRedirectCallback = appState => {
  Router.replace(appState?.returnTo || "/")
}

function MyApp({ Component, pageProps }) {
  useEffect(() => {
    import("bootstrap/dist/js/bootstrap")
  }, [])

  useEffect(() => {
    typeof document !== undefined ? require("bootstrap/dist/js/bootstrap") : null
  }, [])

  const auth0Props = {
    domain: process.env.NEXT_PUBLIC_SOCIAL_AUTH_AUTH0_DOMAIN,
    clientId: process.env.NEXT_PUBLIC_SOCIAL_AUTH_AUTH0_KEY,
    redirectUri: process.env.NEXT_PUBLIC_SOCIAL_AUTH_AUTH0_REDIRECT_URI,
    onRedirectCallback: onRedirectCallback,
  }

  return (
    <Auth0Provider {...auth0Props}>
      <Component {...pageProps} />
    </Auth0Provider>
  )
}

export default MyApp
