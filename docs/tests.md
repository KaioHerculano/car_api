# Testes

## Estado atual

O projeto possui o diretório `tests`, mas ainda não há testes automatizados
implementados além do arquivo inicial `tests/__init__.py`.

## Estratégia recomendada

Para evoluir a cobertura, recomenda-se adicionar testes com `pytest`,
`httpx.AsyncClient` e fixtures de banco isolado.

Áreas prioritárias:

- Health check.
- Criação de usuário.
- Login e emissão de JWT.
- Refresh de token.
- CRUD de marcas.
- CRUD de carros.
- Restrições de acesso por proprietário.
- Validações de campos obrigatórios, enums, placa, preço e anos.
- Erros de duplicidade para username, email, marca e placa.

## Exemplos de cenários

| Cenário | Resultado esperado |
| --- | --- |
| Criar usuário com username duplicado | `400 Bad Request` |
| Autenticar com senha inválida | `401 Unauthorized` |
| Listar carros sem token | `403` ou `401`, conforme validação do HTTPBearer |
| Buscar carro de outro usuário | `403 Forbidden` |
| Deletar marca com carros associados | `400 Bad Request` |
| Criar carro com marca inexistente | `400 Bad Request` |

## Execução futura

Quando a suíte de testes for adicionada, o comando recomendado é:

```bash
poetry run pytest
```

Também é recomendado adicionar uma task no `pyproject.toml`, por exemplo:

```toml
test = 'pytest'
```
