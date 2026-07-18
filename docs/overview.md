# Visão geral do projeto

A **Car API** é uma aplicação backend construída com **FastAPI** para gerenciar
usuários, marcas e carros. O projeto usa SQLAlchemy assíncrono para persistência,
Alembic para migrações de banco de dados, Pydantic para validação de dados e JWT
Bearer para autenticação.

## Objetivo

O objetivo principal é fornecer uma API REST versionada para:

- Criar e autenticar usuários.
- Gerenciar marcas de veículos.
- Gerenciar carros associados a marcas e proprietários.
- Proteger endpoints por autenticação JWT.
- Restringir operações sensíveis de carros ao usuário proprietário.

## Stack principal

- **Python 3.13+**
- **FastAPI**
- **Pydantic v2**
- **SQLAlchemy AsyncIO**
- **SQLite com aiosqlite**
- **Alembic**
- **PyJWT**
- **pwdlib com Argon2**
- **Poetry**
- **Ruff**
- **Taskipy**
- **MkDocs Material**

## Convenções gerais

A API é organizada por domínios:

- `auth`: autenticação e renovação de token.
- `users`: cadastro e manutenção de usuários.
- `brands`: cadastro e manutenção de marcas.
- `cars`: cadastro e manutenção de carros.

As rotas públicas e autenticadas seguem o prefixo `/api/v1`, exceto o health
check, que fica em `/health_check`.
