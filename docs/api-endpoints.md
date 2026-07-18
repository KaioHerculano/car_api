# API Endpoints

## Health check

| Método | Rota | Autenticação | Descrição |
| --- | --- | --- | --- |
| `GET` | `/health_check` | Não | Verifica se a aplicação está respondendo. |

Resposta esperada:

```json
{
  "status": "ok"
}
```

## Autenticação

Prefixo: `/api/v1/auth`

| Método | Rota | Autenticação | Status | Descrição |
| --- | --- | --- | --- | --- |
| `POST` | `/token` | Não | `200` | Autentica por email e senha e retorna um token JWT. |
| `POST` | `/refresh_token` | Sim | `200` | Gera um novo token para o usuário autenticado. |

### `POST /api/v1/auth/token`

Corpo:

```json
{
  "email": "usuario@example.com",
  "password": "senha123"
}
```

Resposta:

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

## Usuários

Prefixo: `/api/v1/users`

| Método | Rota | Autenticação | Status | Descrição |
| --- | --- | --- | --- | --- |
| `POST` | `/` | Não | `201` | Cria um novo usuário. |
| `GET` | `/` | Sim | `200` | Lista usuários com paginação e busca. |
| `GET` | `/{user_id}` | Sim | `200` | Busca usuário por ID. |
| `PUT` | `/{user_id}` | Sim | `200` | Atualiza usuário por ID. |
| `DELETE` | `/{user_id}` | Sim | `204` | Remove usuário por ID. |

### Campos de criação

```json
{
  "username": "kaio",
  "email": "kaio@example.com",
  "password": "senha123"
}
```

### Query parameters de listagem

| Parâmetro | Tipo | Regra | Descrição |
| --- | --- | --- | --- |
| `offset` | `int` | `>= 0`, padrão `0` | Quantidade de registros a pular. |
| `limit` | `int` | `1..100`, padrão `100` | Quantidade máxima de registros. |
| `search` | `str` | opcional | Busca por username ou email. |

## Marcas

Prefixo: `/api/v1/brands`

| Método | Rota | Autenticação | Status | Descrição |
| --- | --- | --- | --- | --- |
| `POST` | `/` | Sim | `201` | Cria uma nova marca. |
| `GET` | `/` | Sim | `200` | Lista marcas com paginação e filtros. |
| `GET` | `/{brand_id}` | Sim | `200` | Busca marca por ID. |
| `PUT` | `/{brand_id}` | Sim | `200` | Atualiza marca por ID. |
| `DELETE` | `/{brand_id}` | Sim | `204` | Remove marca sem carros associados. |

### Campos de criação

```json
{
  "name": "Toyota",
  "description": "Marca japonesa",
  "is_active": true
}
```

### Query parameters de listagem

| Parâmetro | Tipo | Regra | Descrição |
| --- | --- | --- | --- |
| `offset` | `int` | `>= 0`, padrão `0` | Quantidade de registros a pular. |
| `limit` | `int` | padrão `100` | Quantidade máxima de registros. |
| `search` | `str` | opcional | Busca por nome da marca. |
| `is_active` | `bool` | opcional | Filtra por marcas ativas ou inativas. |

## Carros

Prefixo: `/api/v1/cars`

| Método | Rota | Autenticação | Status | Descrição |
| --- | --- | --- | --- | --- |
| `POST` | `/` | Sim | `201` | Cria um novo carro. |
| `GET` | `/` | Sim | `200` | Lista carros do usuário autenticado com filtros. |
| `GET` | `/{car_id}` | Sim | `200` | Busca carro por ID, validando propriedade. |
| `PUT` | `/{car_id}` | Sim | `200` | Atualiza carro por ID, validando propriedade. |
| `DELETE` | `/{car_id}` | Sim | `204` | Remove carro por ID, validando propriedade. |

### Campos de criação

```json
{
  "model": "Corolla",
  "factory_year": 2023,
  "model_year": 2024,
  "color": "Prata",
  "plate": "ABC1D23",
  "fuel_type": "flex",
  "transmission": "automatic",
  "price": "145000.00",
  "description": "Sedan em ótimo estado",
  "is_available": true,
  "brand_id": 1,
  "owner_id": 1
}
```

### Valores aceitos

Combustível:

- `gasolina`
- `ethanol`
- `flex`
- `diesel`
- `eletric`
- `hybrid`

Transmissão:

- `manual`
- `automatic`
- `semi_automatic`
- `cvt`

### Query parameters de listagem

| Parâmetro | Tipo | Regra | Descrição |
| --- | --- | --- | --- |
| `offset` | `int` | `>= 0`, padrão `0` | Quantidade de registros a pular. |
| `limit` | `int` | `1..100`, padrão `100` | Quantidade máxima de registros. |
| `search` | `str` | opcional | Busca por modelo, cor ou placa. |
| `brand_id` | `int` | opcional | Filtra por marca. |
| `owner_id` | `int` | opcional | Filtra por proprietário. |
| `fuel_type` | `FuelType` | opcional | Filtra por combustível. |
| `transmission` | `TransmissionType` | opcional | Filtra por transmissão. |
| `is_available` | `bool` | opcional | Filtra por disponibilidade. |
| `min_price` | `float` | opcional | Preço mínimo. |
| `max_price` | `float` | opcional | Preço máximo. |

## Códigos de erro recorrentes

| Status | Situação |
| --- | --- |
| `400` | Dados duplicados, marca/proprietário inexistente ou regra de negócio violada. |
| `401` | Token ausente, inválido, expirado ou credenciais incorretas. |
| `403` | Usuário autenticado não é proprietário do carro solicitado. |
| `404` | Recurso não encontrado. |
| `422` | Erro de validação do Pydantic/FastAPI. |
