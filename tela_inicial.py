import os

import streamlit as st

import tela_principal

st.set_page_config(
    page_title="Commit Review",
    layout="centered",
)


def render_tela_inicial():
    logo_path = "logo.png"
    col1, col2, col3 = st.columns([1, 1, 1])
    if os.path.exists(logo_path):
        with col2:
            st.image(logo_path, width=200)
    else:
        st.markdown("### Logo não encontrada.")
    st.title("Bem-vindo ao Commit Review!")
    st.write("Para sua segurança, os dados de token não são salvos!")
    st.write("Ao fechar o aplicativo os dados serão perdidos.")
    st.write("Preencha os campos obrigatórios para continuar:")

    plataforma = st.selectbox("Selecione a Plataforma", ["GitLab"])
    git_token = st.text_input(
        "Git Token", type="password", help="Insira o seu token do Git."
    )
    grok_api_key = st.text_input(
        "Grok API Key", type="password", help="Insira a chave de API do Grok."
    )
    empresa_url = st.text_input(
        "Empresa URL (opcional)",
        help="Caso sua empresa utilize uma url personalizada no git, insira somente o nome da empresa, da forma que aparece na url aqui.",
    )

    if st.button("Continuar"):
        if not git_token or not grok_api_key:
            st.error("Os campos GitLab Token e Grok API Key são obrigatórios.")
        else:
            st.session_state["plataforma"] = plataforma
            st.session_state["git_token"] = git_token
            st.session_state["grok_api_key"] = grok_api_key
            st.session_state["empresa_url"] = (
                empresa_url if empresa_url else ""
            )
            st.session_state["pagina"] = "tela_principal"


if "pagina" not in st.session_state:
    st.session_state["pagina"] = "tela_inicial"

if st.session_state["pagina"] == "tela_inicial":
    render_tela_inicial()
elif st.session_state["pagina"] == "tela_principal":
    tela_principal.render_dashboard(
        git_token=st.session_state["git_token"],
        grok_api_key=st.session_state["grok_api_key"],
        empresa_url=st.session_state["empresa_url"],
        plataforma=st.session_state["plataforma"],
    )
