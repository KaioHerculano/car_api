# Car API

Bem-vindo à documentação da **Car API**, uma API REST para cadastro,
consulta e gerenciamento de usuários, marcas e carros.

Esta documentação está organizada para apoiar uso local, desenvolvimento,
manutenção e evolução do projeto.

## Conteúdo

- [Visão geral do projeto](overview.md)
- [Pré-requisitos](prerequisites.md)
- [Instalação](installation.md)
- [Configuração do Projeto](configuration.md)
- [Guidelines e padrões](guidelines.md)
- [Estrutura do Projeto](project-structure.md)
- [API Endpoints](api-endpoints.md)
- [Modelagem do Sistema](system-modeling.md)
- [Autenticação e Segurança](authentication-security.md)
- [Desenvolvimento](development.md)
- [Testes](tests.md)
- [Deploy](deploy.md)
- [Contribuição](contribution.md)
- [Release Notes](release-notes.md)

## Atalhos rápidos

### Rodar a API

```bash
poetry install
poetry run task run
```

### Rodar as migrações

```bash
poetry run alembic upgrade head
```

### Servir a documentação localmente

```bash
poetry run task docs
```

Por padrão, a API expõe a documentação interativa do FastAPI em `/docs` e
`/redoc`, enquanto esta documentação do projeto é servida pelo MkDocs.
