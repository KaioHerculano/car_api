# Deploy

## Visão geral

O projeto ainda não possui arquivos específicos de deploy, como Dockerfile,
pipeline CI/CD ou manifesto de infraestrutura. A aplicação, porém, já tem os
elementos principais para ser publicada como uma API FastAPI:

- Configuração por variáveis de ambiente.
- Migrações com Alembic.
- Endpoint de health check.
- Dependências declaradas no `pyproject.toml`.

## Checklist para produção

- Definir `DATABASE_URL` do banco de produção.
- Definir `JWT_SECRET_KEY` forte e secreta.
- Confirmar `JWT_ALGORITHM`.
- Ajustar `JWT_EXPIRATION_MINUTES` conforme política de segurança.
- Executar `alembic upgrade head` antes de liberar tráfego.
- Servir a aplicação com servidor ASGI apropriado para produção.
- Habilitar HTTPS.
- Configurar logs, métricas e monitoramento.
- Configurar backup do banco.

## Comando de migração

```bash
poetry run alembic upgrade head
```

## Comando de aplicação

Em desenvolvimento, o comando existente é:

```bash
poetry run task run
```

Para produção, prefira um servidor ASGI voltado a execução contínua, como
Uvicorn ou equivalente, apontando para:

```text
car_api.app:app
```

## Health check

Use o endpoint abaixo em balanceadores, plataformas de deploy ou probes:

```http
GET /health_check
```

Resposta esperada:

```json
{
  "status": "ok"
}
```

## Recomendações futuras

- Adicionar Dockerfile.
- Adicionar pipeline de lint, testes e build.
- Adicionar estratégia de ambientes: desenvolvimento, staging e produção.
- Adicionar documentação específica da plataforma escolhida para deploy.
