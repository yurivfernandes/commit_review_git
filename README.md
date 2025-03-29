# Code Review 📋
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI_API-GPT_3.5-green.svg?logo=openai&logoColor=white)](https://openai.com/)
[![GitLab](https://img.shields.io/badge/GitLab_API-v4-orange.svg?logo=gitlab&logoColor=white)](https://docs.gitlab.com/ee/api/)
[![GitHub](https://img.shields.io/badge/GitHub_API-v3-black.svg?logo=github&logoColor=white)](https://docs.github.com/en/rest)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<div align="center">
  <img src="https://via.placeholder.com/600x300?text=Code+Review+App" alt="Code Review Banner" width="600px"/>
</div>

## 🚀 Sobre o Projeto

O **Code Review** é uma aplicação interativa desenvolvida em **Streamlit** que permite gerar relatórios detalhados sobre as mudanças feitas em um commit de um projeto no GitLab ou GitHub. Utilizando a tecnologia da **OpenAI**, o aplicativo analisa as alterações e gera um relatório claro e conciso que resume as ações realizadas no commit, como arquivos **criados**, **alterados** ou **deletados**.

## ✨ Funcionalidades

O objetivo principal do **Code Review** é oferecer uma visão rápida e clara sobre o impacto de um commit em um projeto. Através da interface do Streamlit, o usuário pode:

- Selecionar a plataforma (GitLab ou GitHub)
- Selecionar o projeto/repositório e o commit
- Fornecer uma user story para contextualizar a análise
- Ver um relatório detalhado gerado pelo ChatGPT mostrando o que foi **criado**, **alterado** ou **deletado**
- Utilizar a integração com as APIs do GitLab e GitHub para acessar informações dos commits
- Obter uma análise automatizada que facilita a compreensão das alterações

## 🛠️ Tecnologias Utilizadas

- **Streamlit**: Framework para criar aplicações web interativas
- **Python**: Linguagem de programação principal
- **OpenAI API**: Para geração de análises contextualizadas via ChatGPT
- **GitLab/GitHub API**: Para buscar informações dos repositórios e commits
- **Polars**: Para manipulação eficiente de dados
- **HTTPX**: Cliente HTTP assíncrono para Python

## 📋 Pré-requisitos

Para executar este projeto, você precisará:

- Python 3.9 ou superior
- Uma chave API da OpenAI
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
4. Escolha o usuário, projeto e commit que deseja analisar
5. Forneça a user story relacionada ao commit
6. Clique em "Gerar Relatório"
7. Aguarde enquanto o ChatGPT analisa as alterações e gera o relatório

## 📝 Licença

Este projeto está sob a licença MIT - veja o arquivo LICENSE para mais detalhes.

## 👤 Autor

Desenvolvido por [Yuri Viana Fernandes](https://github.com/yurivfernandes)





