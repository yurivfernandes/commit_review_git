import httpx
import streamlit as st


class ProjectDataset:
    """Classe para obter um dataset com o nome e o ID dos projetos do GitLab ou repositórios do GitHub"""

    def __init__(self, git_token: str, empresa_url: str, plataforma: str):
        self.header = (
            {"Private-Token": git_token}
            if plataforma == "GitLab"
            else {"Authorization": f"token {git_token}"}
        )
        self.url = ""
        if plataforma == "GitLab":
            self.url = f"https://gitlab{empresa_url}.com.br/api/v4/projects?order_by=name&page="
        else:
            self.url = (
                f"https://api.github.com/user/repos?per_page=100&page="
                if not empresa_url
                else f"https://api.github.com/orgs/{empresa_url}/repos?per_page=100&page="
            )

    @property
    def dataset(self) -> dict:
        """Retorna uma lista de dicionários com o nome e o ID dos projetos do GitLab ou repositórios do GitHub"""
        all_projects = []

        try:
            page = 1

            while True:
                response = httpx.get(self.url + str(page), headers=self.header)

                if response.status_code == 200:
                    projects = response.json()

                    if not projects:
                        break
                    filtered_projects = [
                        {"id": project["id"], "name": project["name"]}
                        for project in projects
                    ]

                    all_projects.extend(filtered_projects)
                    page += 1

                else:
                    raise ValueError(
                        f"Erro na requisição: {response.status_code} - {response.text}"
                    )

            return all_projects

        except httpx.RequestError as e:
            raise ConnectionError(f"Erro na requisição HTTP: {e}")
        except Exception as e:
            raise RuntimeError(f"Erro desconhecido: {e}")


# Adicionando um método para inicializar o estado da sessão
if "pagina" not in st.session_state:
    st.session_state["pagina"] = "tela_inicial"
