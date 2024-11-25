# Code Review

O **Code Review** é uma aplicação interativa desenvolvida em **Streamlit** que permite gerar relatórios detalhados sobre as mudanças feitas em um commit de um projeto no GitLab. O relatório resume as ações realizadas no commit, como arquivos **criados**, **alterados** ou **deletados**, com base nas diferenças no código enviadas no commit.

## Funcionalidade

O objetivo principal do **Code Review** é oferecer uma visão rápida e clara sobre o impacto de um commit em um projeto. Através da interface do Streamlit, o usuário pode:

- Selecionar o projeto e o commit do GitLab.
- Ver um relatório detalhado mostrando o que foi **criado**, **alterado** ou **deletado**.
- Utilizar a integração com a **API do GitLab** para acessar as informações do commit e analisar os arquivos modificados.
- O relatório é gerado automaticamente e inclui uma visão geral dos arquivos e alterações feitas.

## Instalação

Este projeto requer a instalação de algumas bibliotecas para funcionar corretamente. Utilize o seguinte comando para instalar todas as dependências necessárias:

### Configurações necessárias:

Abra o arquivo kens_and_tokens.py e adicione o seu token do Gitlab, o seu token do Grokapi e caso sua empresa tenha uma url personalizada, adicione o nome com um ponto antes. Caso não tenha, deixe vazio.

```bash
pip install -r requirements.txt





