# Configuração do Projeto

As configurações da aplicação ficam centralizadas em
`car_api/core/settings.py` e são carregadas por `pydantic-settings` a partir do
arquivo `.env`.

## Variáveis de ambiente

| Variável | Obrigatória | Valor padrão | Descrição |
| --- | --- | --- | --- |
| `DATABASE_URL` | Sim | - | URL de conexão do banco usada pela aplicação e pelo Alembic. |
| `JWT_SECRET_KEY` | Sim | - | Chave secreta usada para assinar e validar tokens JWT. |
| `JWT_ALGORITHM` | Não | `HS256` | Algoritmo usado na assinatura do JWT. |
| `JWT_EXPIRATION_MINUTES` | Não | `30` | Tempo de expiração do token de acesso em minutos. |

## Banco de dados

O projeto usa SQLAlchemy assíncrono. Em desenvolvimento local, a configuração
esperada é SQLite com `aiosqlite`:

```env
DATABASE_URL=sqlite+aiosqlite:///./car.db
```

O mesmo valor é usado:

- Pela aplicação, em `car_api/core/database.py`.
- Pelo Alembic, em `migrations/env.py`.

## Migrações

As migrações ficam em `migrations/versions`.

Migração atual do banco:

```bash
poetry run alembic upgrade head
```

Gerar nova migração por autogenerate:

```bash
poetry run alembic revision --autogenerate -m "descricao_da_migracao"
```

## Documentação

O MkDocs é configurado em `mkdocs.yml`. O comando de desenvolvimento da
documentação é:

```bash
poetry run task docs
```
