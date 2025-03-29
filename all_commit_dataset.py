import httpx

class AllCommit:
    def __init__(self, user_id: int, repo_name: str, owner: str, git_token: str, plataforma: str):
        self.user_id = user_id
        self.header = {"Private-Token": git_token} if plataforma == "GitLab" else {"Authorization": f"token {git_token}"}
        if plataforma == "GitLab":
            base_url = "https://gitlab.com/api/v4/projects"
            self.url = f"{base_url}/{repo_name}/repository/commits" if not owner else f"https://gitlab.{owner}.com.br/api/v4/projects/{repo_name}/repository/commits"
        else:
            base_url = "https://api.github.com/repos"
            self.url = f"{base_url}/{owner}/{repo_name}/commits"

    @property
    def dataset(self) -> dict:
        """Retorna um dataset com a lista de commits do projeto filtrados pelo usuário"""
        try:
            response = httpx.get(
                url=self.url,
                headers=self.header,
                params={"author": self.user_id, "per_page": 100},
            )

            if response.status_code == 200:
                return response.json()
            else:
                raise ValueError(
                    f"Erro na requisição: {response.status_code} - {response.text}"
                )
        except httpx.RequestError as e:
            raise ConnectionError(f"Erro na requisição HTTP: {e}")
        except Exception as e:
            raise RuntimeError(f"Erro desconhecido: {e}")
