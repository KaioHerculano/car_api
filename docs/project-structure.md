# Estrutura do Projeto

```text
car_api/
├── car_api/
│   ├── app.py
│   ├── core/
│   │   ├── database.py
│   │   ├── security.py
│   │   └── settings.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── cars.py
│   │   └── users.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── brands.py
│   │   ├── cars.py
│   │   └── users.py
│   └── schemas/
│       ├── auth.py
│       ├── brands.py
│       ├── cars.py
│       └── users.py
├── docs/
├── migrations/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── tests/
├── alembic.ini
├── mkdocs.yml
├── poetry.lock
├── pyproject.toml
└── README.md
```

## Arquivos e diretórios principais

| Caminho | Responsabilidade |
| --- | --- |
| `car_api/app.py` | Cria a aplicação FastAPI, registra os roteadores e define o health check. |
| `car_api/core/settings.py` | Define as configurações carregadas do `.env`. |
| `car_api/core/database.py` | Cria o engine assíncrono e fornece sessões de banco por dependência. |
| `car_api/core/security.py` | Centraliza hash de senha, JWT, autenticação e autorização de carros. |
| `car_api/models/base.py` | Base declarativa do SQLAlchemy. |
| `car_api/models/users.py` | Modelo de usuário. |
| `car_api/models/cars.py` | Modelos de marca e carro, além dos enums de combustível e transmissão. |
| `car_api/schemas/*.py` | Schemas Pydantic de entrada, atualização, saída e listagem. |
| `car_api/routers/*.py` | Endpoints HTTP organizados por domínio. |
| `migrations/env.py` | Configuração do Alembic integrada ao `DATABASE_URL`. |
| `migrations/versions` | Histórico de migrações do banco. |
| `tests` | Diretório reservado para testes automatizados. |
| `mkdocs.yml` | Configuração da documentação do projeto. |
| `docs` | Arquivos Markdown da documentação. |
