import React from "react"
import * as S from "./styled"

const NotAuthenticated = () => {
  return (
    <>
      <S.MainWrapper className="d-flex align-items-center flex-column bd-highlight mb-3">
        <div className="spinner-border" role="status" />
        <S.Message className="text-center">
          Você não está autenticado! Estamos redirecionando para a página de login 😅
        </S.Message>
      </S.MainWrapper>
    </>
  )
}

export default NotAuthenticated
