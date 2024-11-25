import httpx
import polars as pl


class ProjectDataset:
    """Classe para obter um dataset com o nome e o ID dos projetos do GitLab"""

    def __init__(self, git_token: str, empresa_url: str, plataforma: str):
        self.header = {"Private-Token": git_token}
        self.url = ""
        if plataforma == "GitLab":
            self.url = f"https://gitlab{empresa_url}.com.br/api/v4/projects?order_by=name&page="
        else:
            self.url = f"https://github{empresa_url}.com.br/api/v4/projects?order_by=name&page="

    @property
    def dataset(self) -> pl.DataFrame:
        """Retorna um dataset com o nome e o ID dos projetos do GitLab"""
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

            return pl.DataFrame(data=all_projects).sort("name")

        except httpx.RequestError as e:
            raise ConnectionError(f"Erro na requisição HTTP: {e}")
        except Exception as e:
            raise RuntimeError(f"Erro desconhecido: {e}")
