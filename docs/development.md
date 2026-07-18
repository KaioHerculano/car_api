# Desenvolvimento

## Executar localmente

```bash
poetry run task run
```

Esse comando executa:

```bash
fastapi dev car_api/app.py
```

## Fluxo recomendado

1. Criar ou atualizar models em `car_api/models`.
2. Criar ou atualizar schemas em `car_api/schemas`.
3. Implementar regras e endpoints em `car_api/routers`.
4. Gerar migração com Alembic, quando houver mudança de schema.
5. Rodar lint e formatação.
6. Atualizar documentação quando houver mudança de comportamento público.

## Criar migrações

```bash
poetry run alembic revision --autogenerate -m "descricao_da_migracao"
poetry run alembic upgrade head
```

Antes de commitar uma migração gerada, revise o arquivo em
`migrations/versions` para confirmar que o Alembic detectou apenas as mudanças
esperadas.

## Lint e formatação

```bash
poetry run task lint
poetry run task format
```

## Documentação local

```bash
poetry run task docs
```

O site da documentação fica disponível em:

```text
http://127.0.0.1:8001
```

## Adição de novos endpoints

Ao adicionar um endpoint:

- Defina status HTTP explícito.
- Use schemas Pydantic para entrada e saída.
- Evite retornar modelos internos com campos sensíveis.
- Adicione dependência `get_current_user` quando a rota exigir autenticação.
- Documente parâmetros de rota, query parameters e exemplos de payload.
