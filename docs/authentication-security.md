# Autenticação e Segurança

## Estratégia de autenticação

A API usa autenticação **JWT Bearer**. O token é gerado em
`POST /api/v1/auth/token` após validação de email e senha.

O token contém:

- `sub`: ID do usuário autenticado em formato string.
- `exp`: data e hora de expiração calculada a partir de
  `JWT_EXPIRATION_MINUTES`.

## Uso do token

Depois de autenticar, envie o token no header:

```http
Authorization: Bearer <access_token>
```

## Renovação

O endpoint `POST /api/v1/auth/refresh_token` recebe um token válido e retorna um
novo token para o mesmo usuário.

## Senhas

As senhas são processadas por `pwdlib.PasswordHash.recommended()`. Na prática:

- A senha em texto puro é recebida apenas no cadastro, login ou atualização.
- O banco armazena apenas o hash.
- Os schemas públicos não retornam o campo `password`.

## Proteção de endpoints

Endpoints públicos:

- `GET /health_check`
- `POST /api/v1/users/`
- `POST /api/v1/auth/token`

Endpoints protegidos:

- Listagem, consulta, atualização e remoção de usuários.
- Todas as rotas de marcas.
- Todas as rotas de carros.
- Renovação de token.

## Autorização por proprietário

As rotas de carros aplicam uma regra adicional: operações de busca por ID,
atualização e exclusão exigem que `current_user.id` seja igual ao `owner_id` do
carro.

Na listagem de carros, a consulta já começa filtrando por:

```python
Car.owner_id == current_user.id
```

Isso impede que um usuário liste carros de outros proprietários por padrão.

## Pontos de atenção

- Use uma `JWT_SECRET_KEY` forte e diferente por ambiente.
- Não versionar arquivos `.env` com segredos reais.
- Em produção, usar HTTPS para proteger o tráfego dos tokens.
- Revisar regras de autorização antes de adicionar endpoints administrativos.
- Considerar políticas de rotação de segredo e revogação de tokens em versões
  futuras.
