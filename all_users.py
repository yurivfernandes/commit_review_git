import httpx

class AllUsers:
    def __init__(self, git_token: str, empresa_url: str, plataforma: str):
        if plataforma == "GitLab":
            self.header = {"Private-Token": git_token}
            self.url = f"https://gitlab.com/api/v4/users" if not empresa_url else f"https://gitlab.{empresa_url}.com.br/api/v4/users"
        else:
            self.header = {"Authorization": f"token {git_token}"}
            self.url = f"https://api.github.com/user" if not empresa_url else f"https://api.github.com/orgs/{empresa_url}/members"

    @property
    def dataset(self) -> dict:
        """Retorna um dataset com a lista de usuários ativos."""
        try:
            response = httpx.get(
                url=self.url,
                headers=self.header,
                params={"active": True, "per_page": 100},
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
