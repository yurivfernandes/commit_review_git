import os

import streamlit as st

from all_commit_dataset import AllCommit
from all_users import AllUsers
from grok_report import GrokReport
from project_dataset import ProjectDataset


# Função para renderizar o dashboard principal
def render_dashboard(git_token, grok_api_key, empresa_url, plataforma):
    st.title("Commit Review - Dashboard Principal")
    st.write(f"**Plataforma:** {plataforma}")
    if empresa_url != "":
        empresa_url = "." + empresa_url

    if plataforma == "GitLab":
        url = f"https://gitlab{empresa_url}.com.br/api/v4"
    else:
        url = f"https://github{empresa_url}.com.br/api/v4"
    st.write(f"**URL API:** {url}")
    logo_path = "logo.png"

    if os.path.exists(logo_path):
        st.sidebar.image(logo_path)
    else:
        st.sidebar.markdown("### Logo não encontrada.")

    with st.sidebar:
        st.write("## Menu")
        st.write("---")

        st.markdown("### Selecione o Usuário")
        user_dataset = AllUsers(
            git_token=git_token, plataforma=plataforma, empresa_url=empresa_url
        ).dataset

        if len(user_dataset) > 0:
            user_options = user_dataset
            selected_user = st.selectbox(
                "Selecione um usuário",
                options=user_options,
                format_func=lambda x: x["name"],
            )
        else:
            st.warning("Nenhum usuário encontrado.")
            selected_user = None

        st.markdown("### Selecione o Projeto")
        project_dataset = ProjectDataset(
            git_token=git_token, plataforma=plataforma, empresa_url=empresa_url
        ).dataset

        if len(project_dataset) > 0:
            project_options = project_dataset
            selected_project = st.selectbox(
                "Selecione um projeto",
                options=project_options,
                format_func=lambda x: x["name"],
            )
        else:
            st.warning("Nenhum projeto encontrado.")
            selected_project = None

        st.markdown("### Selecione o Commit")
        if selected_project and selected_user:
            user_id = selected_user.get("id")
            project_id = selected_project.get("id")

            commit_dataset = AllCommit(
                git_token=git_token,
                plataforma=plataforma,
                empresa_url=empresa_url,
                user_id=user_id,
                project_id=project_id,
            ).dataset

            if not commit_dataset.is_empty():
                commit_options = commit_dataset.sort("id").to_dicts()
                selected_commit = st.selectbox(
                    "Selecione um commit",
                    options=commit_options,
                    format_func=lambda x: f'{x["title"]}',
                )
            else:
                st.warning("Nenhum commit encontrado.")
                selected_commit = None
        else:
            st.info(
                "Selecione um projeto e um usuário para carregar os commits."
            )
            selected_commit = None

        st.markdown("### Insira a User Story")
        user_story = st.text_area("User Story", "")
        generate_report_button = st.button("Gerar Relatório")
    st.write(f"**User Story:** {user_story}")
    if (
        generate_report_button
        and selected_user
        and selected_project
        and selected_commit
        and user_story
    ):
        gpt_report = GrokReport(
            user_story=user_story,
            projeto_id=selected_project["id"],
            commit_id=selected_commit["id"],
            git_token=git_token,
            grok_api_key=grok_api_key,
            plataforma=plataforma,
            empresa_url=empresa_url,
        )._get_grok_data
        st.write(gpt_report)
