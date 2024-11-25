import httpx


class AllUsers:
    def __init__(self, git_token: str, empresa_url: str, plataforma: str):
        self.header = {"Private-Token": git_token}
        self.url = ""
        if plataforma == "GitLab":
            self.url = f"https://gitlab{empresa_url}.com.br/api/v4/users"
        else:
            self.url = f"https://github{empresa_url}.com.br/search/users"

    @property
    def dataset(self) -> dict:
        """Retorna um dicionário com a lista de usuários ativos."""
        try:
            response = httpx.get(
                url=self.url,
                headers=self.header,
                params={"active": True, "per_page": 100},
            )
            if response.status_code == 200:
                users = response.json()
                # Seleciona apenas os campos 'id' e 'name' e retorna como lista de dicionários
                return [
                    {"id": user["id"], "name": user["name"]} for user in users
                ]
            else:
                raise ValueError(
                    f"Erro na requisição: {response.status_code} - {response.text}"
                )
        except httpx.RequestError as e:
            raise ConnectionError(f"Erro na requisição HTTP: {e}")
        except Exception as e:
            raise RuntimeError(f"Erro desconhecido: {e}")
