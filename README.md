# Code Review 📋
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI_API-GPT_3.5-green.svg?logo=openai&logoColor=white)](https://openai.com/)
[![Cloudflare](https://img.shields.io/badge/Cloudflare_AI-Llama_4-F38020.svg?logo=cloudflare&logoColor=white)](https://developers.cloudflare.com/ai-gateway/)
[![GitLab](https://img.shields.io/badge/GitLab_API-v4-orange.svg?logo=gitlab&logoColor=white)](https://docs.gitlab.com/ee/api/)
[![GitHub](https://img.shields.io/badge/GitHub_API-v3-black.svg?logo=github&logoColor=white)](https://docs.github.com/en/rest)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<div align="center">
  <img src="https://via.placeholder.com/600x300?text=Code+Review+App" alt="Code Review Banner" width="600px"/>
</div>

## 🚀 Sobre o Projeto

O **Code Review** é uma aplicação interativa desenvolvida em **Streamlit** que permite gerar relatórios detalhados sobre as mudanças feitas em um commit de um projeto no GitLab ou GitHub. Utilizando a tecnologia da **OpenAI** (ChatGPT) ou **Cloudflare AI** (Llama 4), o aplicativo analisa as alterações e gera um relatório claro e conciso que resume as ações realizadas no commit, como arquivos **criados**, **alterados** ou **deletados**.

## ✨ Funcionalidades

O objetivo principal do **Code Review** é oferecer uma visão rápida e clara sobre o impacto de um commit em um projeto. Através da interface do Streamlit, o usuário pode:

- Selecionar a plataforma (GitLab ou GitHub)
- Escolher o modelo de IA a ser utilizado (ChatGPT ou Llama 4)
- Selecionar o projeto/repositório e o commit
- Fornecer uma user story para contextualizar a análise
- Ver um relatório detalhado gerado pela IA mostrando o que foi **criado**, **alterado** ou **deletado**
- Utilizar a integração com as APIs do GitLab e GitHub para acessar informações dos commits
- Obter uma análise automatizada que facilita a compreensão das alterações

## 🛠️ Tecnologias Utilizadas

- **Streamlit**: Framework para criar aplicações web interativas
- **Python**: Linguagem de programação principal
- **OpenAI API**: Para geração de análises contextualizadas via ChatGPT
- **Cloudflare AI API**: Para geração de análises usando o modelo Llama 4 (com limite de uso gratuito)
- **GitLab/GitHub API**: Para buscar informações dos repositórios e commits
- **Polars**: Para manipulação eficiente de dados
- **HTTPX**: Cliente HTTP assíncrono para Python

## 🤖 Modelos de IA Disponíveis

- **ChatGPT (OpenAI)**: Modelo avançado de linguagem natural para análises detalhadas
- **Llama 4 (Cloudflare AI)**: Modelo alternativo com limite de uso gratuito via Cloudflare Workers AI

## 📋 Pré-requisitos

Para executar este projeto, você precisará:

- Python 3.9 ou superior
- Uma chave API da OpenAI (se utilizar o ChatGPT)
- Uma chave API e ID da conta Cloudflare (se utilizar o Llama 4)
- Um token de acesso pessoal do GitLab ou GitHub

## 🔧 Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/commit_review_git.git
   cd commit_review_git
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure o arquivo `.env` (opcional):
   ```
   GIT_TOKEN=seu_token_aqui
   OPENAI_API_KEY=sua_chave_openai_aqui
   CLOUDFLARE_API_KEY=sua_chave_cloudflare_aqui
   CLOUDFLARE_ACCOUNT_ID=seu_account_id_cloudflare_aqui
   ```

## ⚙️ Configuração

O aplicativo pode ser configurado de duas maneiras:

1. **Utilizando o arquivo .env** (recomendado para uso frequente):
   - Crie um arquivo `.env` na raiz do projeto
   - Adicione suas credenciais no formato mostrado acima
   - As variáveis serão carregadas automaticamente quando o aplicativo iniciar

2. **Via interface do usuário**:
   - Se o arquivo `.env` não for encontrado ou estiver incompleto, o aplicativo solicitará as credenciais na tela inicial
   - Esta opção é mais segura para ambientes compartilhados, pois as credenciais não são salvas

## 🚀 Executando o aplicativo

```bash
streamlit run app.py
```

## 💡 Como usar

1. Inicie o aplicativo
2. Insira suas credenciais (se não configuradas no `.env`)
3. Selecione a plataforma (GitLab ou GitHub)
4. Escolha o modelo de IA (ChatGPT ou Llama 4)
5. Escolha o usuário, projeto e commit que deseja analisar
6. Forneça a user story relacionada ao commit
7. Clique em "Gerar Relatório"
8. Aguarde enquanto a IA analisa as alterações e gera o relatório

## 📝 Licença

Este projeto está sob a licença MIT - veja o arquivo LICENSE para mais detalhes.

## 👤 Autor

Desenvolvido por [Yuri Viana Fernandes](https://github.com/yurivfernandes)





