# Guidelines e padrões

## Organização por domínio

O projeto separa responsabilidades por domínio:

- `routers`: endpoints HTTP.
- `schemas`: contratos de entrada e saída com Pydantic.
- `models`: entidades SQLAlchemy.
- `core`: infraestrutura compartilhada, como configurações, banco e segurança.
- `migrations`: versionamento do schema do banco.
- `tests`: espaço reservado para testes automatizados.

## Estilo de código

O projeto usa Ruff como ferramenta de lint e formatação.

Comandos disponíveis:

```bash
poetry run task lint
poetry run task format
```

Padrões configurados:

- Linha máxima de 79 caracteres.
- Aspas simples no formatador.
- Imports organizados.
- Regras de lint dos grupos `I`, `F`, `E`, `W`, `PL` e `PT`.

## Padrões de API

- Prefixo versionado: `/api/v1`.
- Separação por recurso: `/auth`, `/users`, `/brands`, `/cars`.
- Uso de `response_model` para respostas públicas.
- Uso de status HTTP explícito nos decorators das rotas.
- Paginação com `offset` e `limit` em listagens.
- Filtros via query parameters.

## Padrões de segurança

- Senhas nunca são retornadas nos schemas públicos.
- Senhas são armazenadas com hash gerado por `pwdlib`.
- Tokens JWT carregam o identificador do usuário no claim `sub`.
- Endpoints protegidos usam autenticação `Bearer`.
- Operações em carros validam se o usuário atual é o proprietário.

## Padrões de banco de dados

- Modelos declaram `created_at` e `updated_at` com default no banco.
- Campos únicos são declarados no modelo e nas migrações.
- Relações são expressas com `relationship` e chaves estrangeiras.
- Consultas que retornam carros carregam marca e proprietário com
  `selectinload` quando a resposta pública exige esses dados.
