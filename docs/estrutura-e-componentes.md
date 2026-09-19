# Estrutura e componentes

## Fluxo arquitetural

`Cliente HTTP -> Routes -> Controller -> Service -> Repository -> SQLite`

- **Routes:** associam método e URL à operação do Controller.
- **Controller:** adapta HTTP para o caso de uso e define status/JSON da resposta.
- **Service:** concentra regras de negócio, validação e conflitos.
- **Model:** define e valida o contrato da entidade Produto.
- **Repository:** abstrai as consultas SQL e o mapeamento dos dados.
- **Database:** cria a conexão, tabela, restrições e índice do SQLite.
- **Middlewares:** tratam contexto da requisição, segurança, CORS e erros.

O padrão MVC foi adaptado a uma API REST: o Model abrange entidade e regras de
dados, o Controller coordena a interface HTTP e a View é a representação JSON
devolvida ao consumidor.
