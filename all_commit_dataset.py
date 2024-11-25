import httpx
import polars as pl


class AllCommit:
    def __init__(
        self,
        user_id: int,
        git_token: str,
        empresa_url: str,
        plataforma: str,
        project_id: str,
    ):
        self.header = {"Private-Token": git_token}
        self.user_id = user_id
        self.url = ""
        if plataforma == "GitLab":
            self.url = f"https://gitlab{empresa_url}.com.br/api/v4/projects/{project_id}/repository/commits"
        else:
            self.url = f"https://github{empresa_url}.com.br/api/v4/projects/{project_id}/repository/commits"

    @property
    def dataset(self) -> pl.DataFrame:
        """Retorna um dataset com a lista de commits do projeto filtrados pelo usuário"""
        try:
            response = httpx.get(
                url=self.url,
                headers=self.header,
                params={"author_id": self.user_id, "ref_name": "homolog"},
            )

            if response.status_code == 200:
                commits = response.json()
                return pl.DataFrame(commits).select(["id", "title"])
            else:
                raise ValueError(
                    f"Erro na requisição: {response.status_code} - {response.text}"
                )
        except httpx.RequestError as e:
            raise ConnectionError(f"Erro na requisição HTTP: {e}")
        except Exception as e:
            raise RuntimeError(f"Erro desconhecido: {e}")
