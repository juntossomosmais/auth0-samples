import Layout from "./components/Layout"
import UniversalLogin from "./components/UniversalLogin"
import { useEffect } from "react"

export function App() {
  useEffect(() => {
    const bodyElement = document.querySelector("body")
    bodyElement.style.backgroundColor = "#ff0000"
  })

  return (
    <Layout>
      <UniversalLogin />
    </Layout>
  )
}
