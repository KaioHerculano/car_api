# Pré-requisitos

Antes de instalar e executar o projeto, tenha os seguintes itens disponíveis no
ambiente de desenvolvimento.

## Obrigatórios

- Python `>=3.13,<4.0`
- Poetry compatível com projetos baseados em `pyproject.toml`
- Git

## Recomendados

- VS Code ou outro editor com suporte a Python.
- Cliente HTTP, como Bruno, Insomnia, Postman ou `curl`.
- SQLite Browser, DBeaver ou ferramenta equivalente para inspecionar o banco
  local, quando necessário.

## Conhecimentos úteis

- Noções de FastAPI e OpenAPI.
- Noções de SQLAlchemy assíncrono.
- Noções de Alembic para migração de banco de dados.
- Conceitos básicos de JWT Bearer.

## Portas usadas em desenvolvimento

- API FastAPI: definida pelo comando `fastapi dev`, normalmente em
  `http://127.0.0.1:8000`.
- Documentação MkDocs: `http://127.0.0.1:8001`.
