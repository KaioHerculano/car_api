# Release Notes

## 0.1.0

Estado documentado do projeto em julho de 2026.

### Adicionado

- Aplicação FastAPI.
- Health check em `/health_check`.
- Rotas versionadas em `/api/v1`.
- Cadastro e autenticação de usuários.
- Emissão e renovação de tokens JWT.
- CRUD de usuários.
- CRUD de marcas.
- CRUD de carros.
- Proteção de endpoints por Bearer Token.
- Verificação de propriedade para operações sensíveis em carros.
- Models SQLAlchemy para `User`, `Brand` e `Car`.
- Migrações Alembic para criação das tabelas `users`, `brands` e `cars`.
- Validações Pydantic para usuários, marcas e carros.
- Configuração com Poetry, Ruff, Taskipy, Alembic e MkDocs.
- Documentação em Markdown com diagramas Mermaid.

### Observações

- A suíte de testes automatizados ainda não foi implementada.
- O deploy ainda não possui configuração específica de plataforma.
- A documentação de API detalha o comportamento atual observado no código.
