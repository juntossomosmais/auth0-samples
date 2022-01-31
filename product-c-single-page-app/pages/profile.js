import React, { useEffect, useState } from "react"
import { useAuth0, withAuthenticationRequired } from "@auth0/auth0-react"
import Layout from "./components/Layout"
import NotAuthenticated from "./components/NotAuthenticated"
import { retrieveUserAttributes, updateUserAttributes } from "./providers/user-management"
import { Alert, Button, Form } from "react-bootstrap"
import { removeEmptyKeys } from "./utils/objects"

const Claims = () => {
  const audience = process.env.NEXT_PUBLIC_AUTH0_USER_MANAGEMENT_AUDIENCE
  // States
  const { getAccessTokenSilently } = useAuth0()
  const [accessToken, setAccessToken] = useState(null)
  const initialFormState = {
    full_name: "",
    given_name: "",
    family_name: "",
    user_metadata: null,
    // Messages that we can show
    saveButtonValue: "Salvar alterações",
    sending: false,
    errorMessage: "",
    loadingMessage: "",
    showError: false,
  }
  const [formState, setFormState] = useState(initialFormState)
  // Events
  const handleChange = e => {
    const { name, value } = e.target
    setFormState(prevState => ({ ...prevState, [name]: value }))
  }
  const submitUpdateAttributesHandler = async e => {
    e.preventDefault()
    setFormState(prevState => ({
      ...prevState,
      sending: true,
      saveButtonValue: "Salvando alterações ⏳",
      showError: false,
      errorMessage: "",
    }))
    const attributes = {
      full_name: formState.full_name,
      given_name: formState.given_name,
      family_name: formState.family_name,
    }
    const cleanedAttributes = removeEmptyKeys(attributes)
    try {
      await updateUserAttributes(accessToken, cleanedAttributes)
      setFormState(prevState => ({
        ...prevState,
        sending: false,
        saveButtonValue: initialFormState.saveButtonValue,
        showError: false,
        errorMessage: "",
      }))
    } catch (e) {
      console.log(e)
      setFormState(prevState => ({
        ...prevState,
        sending: false,
        saveButtonValue: initialFormState.saveButtonValue,
        showError: true,
        errorMessage: `You get the follwing: ${JSON.stringify(e)}`,
      }))
    }
  }
  // Hooks
  useEffect(() => {
    async function retrieveMyProperties() {
      const token = await getAccessTokenSilently({ audience })
      setAccessToken(token)
      console.log(token)
      const userAttributes = await retrieveUserAttributes(token)
      setFormState(prevState => ({
        ...prevState,
        full_name: userAttributes.full_name,
        given_name: userAttributes.given_name,
        family_name: userAttributes.family_name,
        user_metadata: userAttributes.user_metadata,
      }))
    }
    retrieveMyProperties()
  }, [getAccessTokenSilently])

  return (
    <Layout>
      <p>
        Your data: <br />
        <br /> <pre>{JSON.stringify(formState)}</pre>
      </p>
      <hr />
      <Form onSubmit={submitUpdateAttributesHandler}>
        {formState.showError && <Alert variant="danger">{formState.errorMessage}</Alert>}
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>Nome completo</Form.Label>
          <Form.Control
            value={formState.full_name}
            onChange={handleChange}
            name="full_name"
            type="text"
            disabled={formState.sending}
          />
        </Form.Group>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>Primeiro nome</Form.Label>
          <Form.Control
            value={formState.given_name}
            onChange={handleChange}
            name="given_name"
            type="text"
            disabled={formState.sending}
          />
        </Form.Group>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>Último nome</Form.Label>
          <Form.Control
            value={formState.family_name}
            onChange={handleChange}
            name="family_name"
            type="text"
            disabled={formState.sending}
          />
        </Form.Group>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>Cidade</Form.Label>
          <Form.Control value={formState.user_metadata?.city} onChange={handleChange} type="text" disabled={true} />
        </Form.Group>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>Estado</Form.Label>
          <Form.Control value={formState.user_metadata?.state} onChange={handleChange} type="text" disabled={true} />
        </Form.Group>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>Gênero</Form.Label>
          <Form.Control value={formState.user_metadata?.gender} onChange={handleChange} type="text" disabled={true} />
        </Form.Group>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>Aniversário</Form.Label>
          <Form.Control value={formState.user_metadata?.birthday} onChange={handleChange} type="text" disabled={true} />
        </Form.Group>
        <Button variant="primary" disabled={formState.sending} type="submit">
          {formState.saveButtonValue}
        </Button>
      </Form>
    </Layout>
  )
}

export default withAuthenticationRequired(Claims, {
  onRedirecting: () => <NotAuthenticated />,
  returnTo: () => window.location.href,
})
