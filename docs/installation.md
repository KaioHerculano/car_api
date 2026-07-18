# Instalação

## 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd car_api
```

## 2. Instalar dependências

```bash
poetry install
```

Esse comando cria ou reutiliza um ambiente virtual e instala as dependências de
produção e desenvolvimento declaradas no `pyproject.toml`.

## 3. Criar o arquivo de ambiente

Crie um arquivo `.env` na raiz do projeto com as variáveis esperadas pela
aplicação.

```env
DATABASE_URL=sqlite+aiosqlite:///./car.db
JWT_SECRET_KEY=troque-esta-chave-em-ambientes-reais
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30
```

## 4. Aplicar migrações

```bash
poetry run alembic upgrade head
```

## 5. Executar a API

```bash
poetry run task run
```

Depois disso, acesse:

- API: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- Health check: `http://127.0.0.1:8000/health_check`
