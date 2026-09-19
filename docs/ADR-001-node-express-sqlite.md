# ADR-001 - Node.js, Express e SQLite

## Status

Aceita em 19/09/2026.

## Contexto

A solução deve expor publicamente um CRUD de domínio, seguir MVC, ser simples de
avaliar localmente e demonstrar persistência funcional.

## Decisão

Adotar JavaScript com Node.js 24, Express 5 e o SQLite nativo do Node. Organizar
o código em Routes, Controllers, Services, Models e Repositories. Publicar o
contrato em OpenAPI 3.1 e verificar os casos de uso com testes de integração.

## Consequências

- Baixa fricção de execução e banco armazenado em um único arquivo.
- Separação clara de responsabilidades e facilidade para trocar o repositório.
- SQLite atende ao desafio e a uma implantação pequena; alta escala ou escrita
  concorrente exigiria migração do repositório para PostgreSQL.
- A versão mínima do Node.js é 24 por causa do módulo nativo `node:sqlite`.
