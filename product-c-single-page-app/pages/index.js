import React from "react"
import { useAuth0 } from "@auth0/auth0-react"
import Layout from "./components/Layout"

export default function Home() {
  const { user, isAuthenticated } = useAuth0()

  return (
    <Layout>
      {isAuthenticated && (
        <div className="pricing-header p-3 pb-md-4 mx-auto text-center">
          <h1 className="display-4 fw-normal">Agora sabemos 😋</h1>
          <p className="fs-5 text-muted">
            <strong>
              {user.name} / {user.email}
            </strong>
          </p>
        </div>
      )}
      {!isAuthenticated && (
        <div className="pricing-header p-3 pb-md-4 mx-auto text-center">
          <h1 className="display-4 fw-normal">Não sabemos quem é você 🥲</h1>
          <p className="fs-5 text-muted">Se autentique e veja o se perfil!</p>
        </div>
      )}
    </Layout>
  )
}
