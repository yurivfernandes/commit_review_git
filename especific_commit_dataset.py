import sys

import httpx


class EspecificCommit:
    """Efetua a consulta na api do GITLab e retorna um relatório das modificações efetuadas."""

    def __init__(
        self,
        git_token: str,
        empresa_url: str,
        plataforma: str,
        project_id: str,
        commit_id: str,
    ):
        self.header = {"Private-Token": git_token}
        self.url = ""
        if plataforma == "GitLab":
            self.url = f"https://gitlab{empresa_url}.com.br/api/v4/projects/{project_id}/repository/commits/{commit_id}/diff"
        else:
            self.url = f"https://github{empresa_url}.com.br/api/v4/projects/{project_id}/repository/commits/{commit_id}/diff"

    @property
    def dataset(self) -> dict:
        """Extrai e transforma o dataset principal"""
        return [
            {
                **commit,
                "info": {
                    "new_path": commit.get("new_path"),
                    "old_path": commit.get("old_path"),
                    "is_new_file": commit.get("new_file"),
                    "is_renamed_file": commit.get("renamed_file"),
                    "is_deleted_file": commit.get("deleted_file"),
                    "changes": commit.get("diff", "").replace(" ", ""),
                },
            }
            for commit in self._get_git_commits
        ]

    @property
    def _get_git_commits(self) -> dict:
        """Busca os dados da API do Git Lab para efetuar os tratamentos necessários"""
        fields = [
            "diff",
            "old_path",
            "new_path",
            "new_file",
            "renamed_file",
            "deleted_file",
        ]

        try:
            response = httpx.get(self.url, headers=self.header)

            if response.status_code == 200:
                data = response.json()
                for commit in data:
                    for field in fields:
                        if field in commit:
                            commit[field] = commit.pop(field)

                return data
            else:
                print(f"Erro na requisição: {response.status_code}")
                print(response.text)
                sys.exit(f"Erro na requisição: {response.status_code}")
        except httpx.RequestError as e:
            print(f"Erro na requisição HTTP: {e}")
            sys.exit(f"Erro na requisição HTTP: {e}")
        except Exception as e:
            print(f"Erro desconhecido: {e}")
            sys.exit(f"Erro desconhecido: {e}")
