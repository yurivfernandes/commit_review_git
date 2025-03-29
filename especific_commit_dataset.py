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
        owner: str,
    ):
        self.header = {"Private-Token": git_token} if plataforma == "GitLab" else {"Authorization": f"token {git_token}"}
        if plataforma == "GitLab":
            base_url = "https://gitlab.com/api/v4/projects"
            self.url = f"{base_url}/{project_id}/repository/commits/{commit_id}/diff" if not empresa_url else f"https://gitlab.{empresa_url}.com.br/api/v4/projects/{project_id}/repository/commits/{commit_id}/diff"
        else:
            base_url = "https://api.github.com/repos"
            self.url = f"{base_url}/{owner}/{project_id}/commits/{commit_id}"


    @property
    def dataset(self) -> dict:
        """Extrai e transforma o dataset principal"""
        if "gitlab" in self.url:
            return self._get_gitlab_commits
        else:
            return self._get_github_commits

    @property
    def _get_gitlab_commits(self) -> dict:
        """Busca os dados da API do GitLab para efetuar os tratamentos necessários"""
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
                    for commit in data
                ]
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

    @property
    def _get_github_commits(self) -> dict:
        """Busca os dados da API do GitHub para efetuar os tratamentos necessários"""
        try:
            response = httpx.get(self.url, headers=self.header)

            if response.status_code == 200:
                data = response.json()
                files = data.get("files", [])
                return [
                    {
                        "info": {
                            "new_path": file.get("filename"),
                            "old_path": None,
                            "is_new_file": file.get("status") == "added",
                            "is_renamed_file": file.get("status") == "renamed",
                            "is_deleted_file": file.get("status") == "removed",
                            "changes": file.get("patch", "").replace(" ", ""),
                        },
                    }
                    for file in files
                ]
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
