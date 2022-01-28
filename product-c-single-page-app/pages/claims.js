import React from "react"
import { useAuth0, withAuthenticationRequired } from "@auth0/auth0-react"
import Layout from "./components/Layout"
import { useCallback, useEffect, useState } from "react"
import Table from "./components/Table"
import { useRouter } from "next/router"
import NotAuthenticated from "./components/NotAuthenticated"

const Claims = () => {
  const { getIdTokenClaims } = useAuth0()
  const [claims, setClaims] = useState(null)
  // Hooks
  const fetchMyAPI = useCallback(async () => {
    const claims = await getIdTokenClaims()
    setClaims(claims)
  }, [])

  useEffect(() => {
    fetchMyAPI()
  }, [fetchMyAPI])

  return (
    <Layout>
      <div className="row">
        <div className="col-md-12">
          <h1 className="display-9 fw-normal text-center">Veja o que está associado com o seu usuário.</h1>
          <Table keyValueObject={claims} />
          <p>
            Em termos técnicos, essa página mostra as claims associadas ao seu usuário. É útil para debugar quais claims estão
            populando seu ID Token.
          </p>
        </div>
      </div>
    </Layout>
  )
}

// https://auth0.github.io/auth0-react/modules/with_authentication_required.html
// https://auth0.github.io/auth0-react/interfaces/with_authentication_required.withauthenticationrequiredoptions.html
export default withAuthenticationRequired(Claims, {
  onRedirecting: () => <NotAuthenticated />,
  returnTo: () => window.location.href,
})
