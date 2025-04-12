import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Commit Review",
    layout="centered",
)

import tela_principal

# Busca os tokens do .env ou solicita ao usuário
default_git_token = os.getenv("GIT_TOKEN", "")
default_openai_api_key = os.getenv("OPENAI_API_KEY", "")
default_cloudflare_api_key = os.getenv("CLOUDFLARE_API_KEY", "")
default_cloudflare_account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID", "")


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

    plataforma = st.selectbox("Selecione a Plataforma", ["GitHub", "GitLab"])
    git_token = st.text_input(
        "Git Token",
        type="password",
        help="Insira o seu token do Git.",
        value=default_git_token,
    )

    llm_model = st.selectbox("Selecione o Modelo LLM", ["ChatGPT", "Llama 4"])

    if llm_model == "ChatGPT":
        openai_api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Insira a chave de API do OpenAI.",
            value=default_openai_api_key,
        )
        cloudflare_api_key = ""
        cloudflare_account_id = ""
    else:  # Llama 4
        cloudflare_api_key = st.text_input(
            "Cloudflare API Key",
            type="password",
            help="Insira a chave de API do Cloudflare.",
            value=default_cloudflare_api_key,
        )
        cloudflare_account_id = st.text_input(
            "Cloudflare Account ID",
            type="password",
            help="Insira o ID da sua conta Cloudflare.",
            value=default_cloudflare_account_id,
        )
        openai_api_key = ""

    empresa_url = st.text_input(
        "Empresa URL (opcional)",
        help="Caso sua empresa utilize uma url personalizada no git, insira somente o nome da empresa, da forma que aparece na url aqui.",
        value=st.session_state.get("empresa_url", ""),
    )

    if st.button("Continuar"):
        campos_obrigatorios_preenchidos = False

        if llm_model == "ChatGPT" and git_token and openai_api_key:
            campos_obrigatorios_preenchidos = True
        elif (
            llm_model == "Llama 4"
            and git_token
            and cloudflare_api_key
            and cloudflare_account_id
        ):
            campos_obrigatorios_preenchidos = True

        if campos_obrigatorios_preenchidos:
            st.session_state["llm_model"] = llm_model
            st.session_state["plataforma"] = plataforma
            st.session_state["git_token"] = git_token
            st.session_state["openai_api_key"] = openai_api_key
            st.session_state["cloudflare_api_key"] = cloudflare_api_key
            st.session_state["cloudflare_account_id"] = cloudflare_account_id
            st.session_state["empresa_url"] = (
                empresa_url if empresa_url else ""
            )
            st.session_state["pagina"] = "tela_principal"
        else:
            if llm_model == "ChatGPT":
                st.error(
                    "Os campos Git Token e OpenAI API Key são obrigatórios."
                )
            else:
                st.error(
                    "Os campos Git Token, Cloudflare API Key e Cloudflare Account ID são obrigatórios."
                )


if "pagina" not in st.session_state:
    st.session_state["pagina"] = "tela_inicial"

if st.session_state["pagina"] == "tela_inicial":
    render_tela_inicial()
elif st.session_state["pagina"] == "tela_principal":
    tela_principal.render_dashboard(
        git_token=st.session_state["git_token"],
        openai_api_key=st.session_state.get("openai_api_key", ""),
        cloudflare_api_key=st.session_state.get("cloudflare_api_key", ""),
        cloudflare_account_id=st.session_state.get(
            "cloudflare_account_id", ""
        ),
        empresa_url=st.session_state["empresa_url"],
        plataforma=st.session_state["plataforma"],
        llm_model=st.session_state["llm_model"],
    )
