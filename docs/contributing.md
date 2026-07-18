# Contribuição

## Fluxo sugerido

1. Criar uma branch a partir da branch principal.
2. Implementar a alteração mantendo a organização por domínio.
3. Rodar formatação e lint.
4. Criar ou atualizar migrações, se houver mudança no banco.
5. Atualizar documentação quando a alteração mudar comportamento público.
6. Abrir pull request com resumo claro da mudança.

## Antes de enviar alterações

Execute:

```bash
poetry run task lint
poetry run task format
```

Se a suíte de testes for adicionada:

```bash
poetry run pytest
```

## Boas práticas

- Manter endpoints pequenos e focados.
- Não expor campos sensíveis em schemas públicos.
- Centralizar regras compartilhadas em `core` quando fizer sentido.
- Usar migrations para qualquer mudança estrutural no banco.
- Revisar mensagens de erro e status HTTP.
- Atualizar exemplos de payload na documentação de endpoints.

## Commits

Use mensagens objetivas, descrevendo a mudança principal:

```text
docs: add project documentation
feat: add car filters
fix: validate brand before creating car
test: cover authentication flow
```
