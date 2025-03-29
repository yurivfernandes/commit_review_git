import os

import streamlit as st
from dotenv import load_dotenv

from all_commit_dataset import AllCommit
from all_users import AllUsers
from chatgpt_report import ChatGPTReport
from project_dataset import ProjectDataset

load_dotenv(".env")


def render_dashboard(git_token, openai_api_key, empresa_url, plataforma):
    logo_path = "vp6_logo.png"

    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Poppins', sans-serif;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if os.path.exists(logo_path):
        st.sidebar.image(logo_path)
    else:
        st.sidebar.markdown("### Logo não encontrada.")

    with st.sidebar:
        st.markdown("## Menu")
        st.markdown("---")

        if plataforma == "GitLab":
            st.markdown("### Selecione o Usuário")
            user_dataset = AllUsers(
                git_token=git_token,
                empresa_url=empresa_url,
                plataforma=plataforma,
            ).dataset

            if len(user_dataset) > 0:
                user_options = user_dataset
                selected_user = st.selectbox(
                    "Selecione um usuário",
                    options=["Selecione um usuário"] + user_options,
                    format_func=lambda x: x["name"]
                    if isinstance(x, dict)
                    else str(x),
                    key="selected_user",
                )
                if selected_user == "Selecione um usuário":
                    selected_user = None
            else:
                st.warning("Nenhum usuário encontrado.")
                selected_user = None
        else:
            user_dataset = AllUsers(
                git_token=git_token,
                empresa_url=empresa_url,
                plataforma=plataforma,
            ).dataset
            selected_user = user_dataset.get("login")
            st.markdown(f"### Usuário: {selected_user}")

        st.markdown(
            f"### Selecione o {'Projeto' if plataforma == 'GitLab' else 'Repositório'}"
        )
        project_dataset = ProjectDataset(
            git_token=git_token,
            empresa_url=empresa_url,
            plataforma=plataforma,
        ).dataset

        if len(project_dataset) > 0:
            project_options = project_dataset
            selected_project = st.selectbox(
                f"Selecione um {'projeto' if plataforma == 'GitLab' else 'repositório'}",
                options=["Selecione um repositório"] + project_options,
                format_func=lambda x: x["name"]
                if isinstance(x, dict)
                else str(x),
                key="selected_project",
            )
            if selected_project == "Selecione um repositório":
                selected_project = None
        else:
            st.warning(
                f"Nenhum {'projeto' if plataforma == 'GitLab' else 'repositório'} encontrado."
            )
            selected_project = None

        # Filtro de Commits
        st.markdown("### Selecione o Commit")
        if selected_project and selected_user:
            project_id = (
                selected_project.get("id")
                if plataforma == "GitLab"
                else selected_project.get("name")
            )
            user_id = (
                selected_user.get("id")
                if plataforma == "GitLab"
                else selected_user
            )

            commit_dataset = AllCommit(
                user_id=user_id,
                repo_name=project_id,
                owner=selected_user,
                git_token=git_token,
                plataforma=plataforma,
            ).dataset

            if commit_dataset:
                commit_options = commit_dataset
                selected_commit = st.selectbox(
                    "Selecione um commit",
                    options=["Selecione um commit"] + commit_options,
                    format_func=lambda x: f"{x['commit']['message']}"
                    if isinstance(x, dict)
                    else str(x),
                    key="selected_commit",
                )
                if selected_commit == "Selecione um commit":
                    selected_commit = None
            else:
                st.warning("Nenhum commit encontrado.")
                selected_commit = None
        else:
            st.info(
                "Selecione um projeto e um usuário para carregar os commits."
            )
            selected_commit = None

        st.markdown("### Insira a User Story")
        user_story = st.text_area("User Story", "", key="user_story")
        generate_report_button = st.button("Gerar Relatório")

    if (
        generate_report_button
        and selected_user
        and selected_project
        and selected_commit
        and user_story
    ):
        commit_id = (
            selected_commit.get("id")
            if plataforma == "GitLab"
            else selected_commit.get("sha")
        )
        gpt_report = ChatGPTReport(
            user_story=user_story,
            projeto_id=selected_project["id"]
            if plataforma == "GitLab"
            else selected_project["name"],
            commit_id=commit_id,
            plataforma=plataforma,
            openai_api_key=openai_api_key,
            git_token=git_token,
            empresa_url=empresa_url,
            owner=selected_user,
        )._get_chatgpt_data

        st.write("### Relatório Gerado:")
        st.write(gpt_report)


if __name__ == "__main__":
    git_token = st.session_state.get("GIT_TOKEN", "")
    openai_api_key = st.session_state.get("OPENAI_API_KEY", "")
    empresa_url = st.session_state.get("EMPRESA_URL")
    plataforma = st.session_state.get("PLATAFORMA", "GitLab")

    render_dashboard(git_token, openai_api_key, empresa_url, plataforma)
