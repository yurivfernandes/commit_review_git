import json

import requests

from all_settings import GROK_API_URL, MODEL
from especific_commit_dataset import EspecificCommit
from playbooks import FINAL_PLAYBOOK, INITIAL_PLAYBOOK


class GrokReport:
    """Classe para interagir com a API da Meta AI via Hugging Face."""

    def __init__(
        self,
        user_story: str,
        projeto_id: int,
        commit_id: str,
        empresa_url: str,
        plataforma: str,
        grok_api_key: str,
        git_token: str,
    ):
        self.user_story = user_story
        self.projeto_id = projeto_id
        self.commit_id = commit_id
        self.empresa_url = empresa_url
        self.plataforma = plataforma
        self.git_token = git_token
        self.headers = {
            "Authorization": f"Bearer {grok_api_key}",
            "Content-Type": "application/json",
        }

    @property
    def _get_grok_data(self) -> str:
        """Busca os dados da API da Meta AI para efetuar os tratamentos necessários."""
        print("Iniciado...")
        body = json.dumps(
            {
                "messages": [
                    {
                        "role": "system",
                        "content": f"{FINAL_PLAYBOOK + str(self.user_story)}",
                    },
                    {
                        "role": "user",
                        "content": f"{self._code_analysis_response}",
                    },
                ],
                "model": MODEL,
                "stream": False,
                "temperature": 0,
            }
        )

        print(f"Buscando o relatório final...")
        final_response = requests.post(
            url=GROK_API_URL, headers=self.headers, data=body
        )
        print(f"Relatório final recebido. Finalizando a requisição...")
        if final_response.status_code != 200:
            return "Resposta vazia."

        return final_response.json().get("choices")[0]["message"]["content"]

    @property
    def _code_analysis_response(self) -> list:
        """Cria uma lista com os resultados dos playbooks intermediários."""
        playbooks = self._playbook_dataset
        print("Playbook com os dados do Commit criado...")
        i = 1
        code_analysis_response = []
        for playbook in playbooks:
            body = json.dumps(
                {
                    "messages": [
                        {
                            "role": "system",
                            "content": f"{INITIAL_PLAYBOOK + str(self.user_story)}",
                        },
                        {"role": "user", "content": f"{playbooks[playbook]}"},
                    ],
                    "model": MODEL,
                    "stream": False,
                    "temperature": 0,
                }
            )

            response = requests.post(
                url=GROK_API_URL, headers=self.headers, data=body
            )
            print(f"Enviado o arquivo: {i}. Aguardando Resposta...")
            if response.status_code != 200:
                break

            code_analysis_response.append(
                response.json().get("choices")[0]["message"]["content"]
            )
            print(f"Resposta do arquivo {i} recebida...")
            i = i + 1
        return code_analysis_response

    @property
    def _playbook_dataset(self) -> dict:
        """Método que monta o Playbook para enviar ao Meta AI."""
        files = EspecificCommit(
            commit_id=self.commit_id,
            project_id=self.projeto_id,
            git_token=self.git_token,
            empresa_url=self.empresa_url,
            plataforma=self.plataforma,
        ).dataset.to_dicts()
        return {"playbook" + str(i + 1): file for i, file in enumerate(files)}
