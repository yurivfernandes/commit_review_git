import json
import time

import requests

from especific_commit_dataset import EspecificCommit
from playbooks import FINAL_PLAYBOOK, INITIAL_PLAYBOOK


class CloudFlareReport:
    """Classe para interagir com a API do Cloudflare AI usando o modelo Llama 4."""

    def __init__(
        self,
        user_story: str,
        projeto_id: int,
        commit_id: str,
        empresa_url: str,
        plataforma: str,
        cloudflare_api_key: str,
        cloudflare_account_id: str,
        git_token: str,
        owner: str,
        model: str = None,  # Parâmetro opcional que não será utilizado
    ):
        self.user_story = user_story
        self.projeto_id = projeto_id
        self.commit_id = commit_id
        self.empresa_url = empresa_url
        self.plataforma = plataforma
        self.git_token = git_token
        self.owner = owner
        # Sempre usar o modelo fixo, independente do que for passado
        self.model = "@cf/meta/llama-4-scout-17b-16e-instruct"
        self.cloudflare_api_url = f"https://api.cloudflare.com/client/v4/accounts/{cloudflare_account_id}/ai/run/{self.model}"
        self.headers = {
            "Authorization": f"Bearer {cloudflare_api_key}",
            "Content-Type": "application/json",
        }

    def _make_request(self, body):
        """Faz uma requisição à API do Cloudflare AI com lógica de retry para lidar com código de status HTTP 429."""
        max_retries = 5
        retry_delay = 1  # segundos

        for attempt in range(max_retries):
            response = requests.post(
                url=self.cloudflare_api_url, headers=self.headers, data=body
            )
            if response.status_code == 429:
                print(
                    f"Rate limit exceeded. Retrying in {retry_delay} seconds..."
                )
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                return response

        raise Exception("Max retries exceeded")

    @property
    def _get_deepseek_data(self) -> str:
        """Busca os dados da API do Cloudflare para efetuar os tratamentos necessários."""
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
                "temperature": 0,
            }
        )

        print(f"Buscando o relatório final...")
        final_response = self._make_request(body)
        print(f"Relatório final recebido. Finalizando a requisição...")
        if final_response.status_code != 200:
            return "Resposta vazia."

        # O formato de resposta do Cloudflare pode ser diferente, ajuste conforme necessário
        return final_response.json().get("result", {}).get("response", "")

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
                    "temperature": 0,
                }
            )

            response = self._make_request(body)

            print(f"Enviado o arquivo: {i}. Aguardando Resposta...")
            if response.status_code != 200:
                break

            # Adaptação para o formato de resposta do Cloudflare
            code_analysis_response.append(
                response.json().get("result", {}).get("response", "")
            )
            print(f"Resposta do arquivo {i} recebida...")
            i = i + 1
        return code_analysis_response

    @property
    def _playbook_dataset(self) -> dict:
        """Método que monta o Playbook para enviar ao DeepSeek."""
        files = EspecificCommit(
            commit_id=self.commit_id,
            project_id=self.projeto_id,
            git_token=self.git_token,
            empresa_url=self.empresa_url,
            plataforma=self.plataforma,
            owner=self.owner,
        ).dataset
        return {"playbook" + str(i + 1): file for i, file in enumerate(files)}

    def get_report(self) -> str:
        """Método público para obter o relatório completo."""
        return self._get_deepseek_data
