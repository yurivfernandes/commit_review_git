import sys

import httpx
import polars as pl

from all_settings import GIT_LAB_HEADERS, GIT_LAB_URL


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
    def dataset(self) -> pl.DataFrame:
        """Extrai e transforma o dataset principal"""
        return self._get_git_commits.with_columns(
            pl.col("new_path").cast(pl.Utf8),
            pl.struct(
                [
                    "new_path",
                    "old_path",
                    "is_new_file",
                    "is_renamed_file",
                    "is_deleted_file",
                    pl.col("changes").str.replace_all(" ", ""),
                ]
            ).alias("info"),
        ).drop(
            [
                "new_path",
                "old_path",
                "is_new_file",
                "is_renamed_file",
                "is_deleted_file",
                "changes",
            ]
        )

    @property
    def _get_git_commits(self) -> pl.DataFrame:
        """Busca os dados da API do Git Lab para efetuar os tratamentos necessários"""
        schema = {
            "diff": {"type": pl.Utf8, "rename": "changes"},
            "old_path": {"type": pl.Utf8, "rename": "old_path"},
            "new_path": {"type": pl.Utf8, "rename": "new_path"},
            "new_file": {"type": pl.Boolean, "rename": "is_new_file"},
            "renamed_file": {"type": pl.Boolean, "rename": "is_renamed_file"},
            "deleted_file": {"type": pl.Boolean, "rename": "is_deleted_file"},
        }

        try:
            response = httpx.get(self.url, headers=GIT_LAB_HEADERS)

            if response.status_code == 200:
                data = response.json()
                columns = {key: field["type"] for key, field in schema.items()}
                renamed_columns = {
                    key: field["rename"] for key, field in schema.items()
                }

                return pl.DataFrame(data, schema=columns).rename(
                    renamed_columns
                )
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
