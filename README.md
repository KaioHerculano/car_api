# Car API

API REST desenvolvida com FastAPI para gerenciamento de usuários, marcas e
carros. O projeto foi criado durante a primeira etapa do curso FastMaster, da
PycodeBR Treinamentos, com foco em backend Python, boas práticas de organização,
validação de dados, autenticação e testes.

## Sobre o projeto

A aplicação permite criar usuários, autenticar com JWT, cadastrar marcas e
gerenciar carros associados aos usuários. A estrutura do projeto separa routers,
schemas, models e configurações centrais, mantendo a API organizada e preparada
para evolução.

## Principais recursos

- API REST com FastAPI
- Programação assíncrona com SQLAlchemy
- Validação de dados com Pydantic
- CRUD de usuários, marcas e carros
- Autenticação com JSON Web Token
- Hash e verificação de senhas
- Migrations com Alembic
- Testes automatizados com pytest
- Banco SQLite em memória para testes
- Documentação do projeto com MkDocs

## Tecnologias

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- SQLite
- PyJWT
- Pytest
- MkDocs
- Poetry

## Como executar

Instale as dependências:

```bash
poetry install
```

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=sqlite+aiosqlite:///./car.db
JWT_SECRET_KEY=change-this-secret
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30
```

Aplique as migrations:

```bash
poetry run alembic upgrade head
```

Execute a API:

```bash
poetry run task run
```

Depois acesse:

- API: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- Health check: `http://127.0.0.1:8000/health_check`

## Testes

Execute a suíte de testes com coverage:

```bash
poetry run task test
```

O relatório HTML de cobertura é gerado em `htmlcov/index.html`.

## Documentação

A documentação completa do projeto está em `docs/` e pode ser executada com:

```bash
poetry run task docs
```

Ela inclui visão geral, instalação, configuração, endpoints, autenticação,
modelagem, testes, deploy e guidelines do projeto.
