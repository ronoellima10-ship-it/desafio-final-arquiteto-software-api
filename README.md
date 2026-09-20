# Partner Products API

[Português](#português) · [English](#english) · [C4 Model](docs/architecture/C4.md)

[![CI](https://github.com/ronoellima10-ship-it/desafio-final-arquiteto-software-api/actions/workflows/ci.yml/badge.svg)](https://github.com/ronoellima10-ship-it/desafio-final-arquiteto-software-api/actions/workflows/ci.yml)

API REST de produtos desenvolvida para o Desafio Final do Bootcamp Arquiteto(a) de Software.

## Português

### Visão geral

A **Partner Products API** é uma API REST de produtos implementada em JavaScript, Node.js e Express. A solução adapta o padrão MVC para uma interface HTTP, separa regras de negócio e persistência em camadas, armazena os dados em SQLite e publica um contrato OpenAPI interativo.

### Entregáveis

- [Relatório técnico final em PDF](docs/entregavel-final-arquitetura-software.pdf)
- [Diagramas da arquitetura em PDF](docs/diagramas-arquitetura.pdf)
- [Arquivo editável do draw.io](docs/arquitetura.drawio)
- [Diagrama C4 de contêineres em SVG](docs/diagramas/c4-conteineres.svg)
- [Diagrama dos componentes MVC em SVG](docs/diagramas/mvc-componentes.svg)
- [Índice C4 bilíngue](docs/architecture/C4.md)
- [Decisão arquitetural ADR-001](docs/ADR-001-node-express-sqlite.md)
- [Descrição da estrutura e dos componentes](docs/estrutura-e-componentes.md)

### Funcionalidades

- CRUD completo de produtos;
- contagem total de registros;
- listagem de todos os registros;
- consulta por ID;
- pesquisa parcial por nome, sem diferenciar maiúsculas e minúsculas;
- persistência em SQLite com restrições e índice;
- validação de entrada e respostas de erro padronizadas;
- OpenAPI 3.1 e Swagger UI;
- testes automatizados de integração;
- Docker, health check e pipeline de integração contínua.

### Arquitetura

![C4 - Contêineres](docs/diagramas/c4-conteineres.svg)

```text
Cliente HTTP -> Middlewares -> Routes -> Controller -> Service -> Model/Repository -> SQLite
```

Na adaptação do MVC para uma API REST:

- **Model:** representa e valida o produto e participa da camada de dados;
- **Controller:** adapta a requisição HTTP e produz status e representação JSON;
- **View:** é a representação JSON entregue ao consumidor;
- **Service:** mantém as regras de negócio fora do Controller;
- **Repository:** isola SQL e persistência, permitindo trocar o banco com menor impacto.

Veja os níveis C1, C2 e C3, o fluxo de criação e os links para os arquivos visuais em [docs/architecture/C4.md](docs/architecture/C4.md).

### Tecnologias

| Área | Tecnologias |
|---|---|
| Runtime | JavaScript ES Modules e Node.js 24 |
| API | Express 5 |
| Banco de dados | SQLite nativo com `node:sqlite` |
| Validação | Zod |
| Segurança e integração | Helmet e CORS |
| Contrato | OpenAPI 3.1 e Swagger UI |
| Testes | Vitest e Supertest |
| Entrega | Docker, Docker Compose e GitHub Actions |

### Como executar localmente

Requisito: Node.js 24 ou superior.

```bash
npm ci
cp .env.example .env
npm run seed
npm start
```

A API ficará disponível em `http://localhost:3000`. A documentação interativa estará em `http://localhost:3000/docs`.

Para desenvolvimento com recarregamento automático:

```bash
npm run dev
```

### Como executar com Docker

```bash
docker compose up --build
```

O volume `product_data` preserva o banco entre reinicializações.

### Endpoints

| Método | Rota | Finalidade |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/api/v1/products` | Listar todos |
| `GET` | `/api/v1/products/count` | Contar registros |
| `GET` | `/api/v1/products/:id` | Buscar por ID |
| `GET` | `/api/v1/products/name/:name` | Buscar por nome |
| `POST` | `/api/v1/products` | Criar |
| `PUT` | `/api/v1/products/:id` | Atualizar completamente |
| `PATCH` | `/api/v1/products/:id` | Atualizar parcialmente |
| `DELETE` | `/api/v1/products/:id` | Excluir |
| `GET` | `/docs` | Swagger UI |
| `GET` | `/openapi.json` | Contrato OpenAPI |

Exemplo de criação:

```bash
curl -X POST http://localhost:3000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Notebook Pro 14",
    "description": "Notebook profissional com 16 GB de RAM.",
    "price": 5499.90,
    "stock": 15,
    "active": true
  }'
```

### Estrutura de pastas

```text
.
├── .github/workflows/ci.yml       # integração contínua
├── data/                           # banco SQLite local
├── docs/
│   ├── architecture/C4.md         # índice C4 bilíngue
│   ├── arquitetura.drawio         # diagrama editável em duas páginas
│   ├── diagramas/                  # exportações vetoriais
│   ├── diagramas-arquitetura.pdf   # entregável visual
│   └── entregavel-final-arquitetura-software.pdf
├── scripts/seed.js                 # dados de demonstração
├── src/
│   ├── config/                     # banco e OpenAPI
│   ├── controllers/                # entrada e saída HTTP
│   ├── errors/                     # erros de domínio e aplicação
│   ├── middlewares/                # aspectos transversais
│   ├── models/                     # entidade e validação
│   ├── repositories/               # persistência SQL
│   ├── routes/                     # rotas REST
│   ├── services/                   # casos de uso e regras
│   ├── app.js                      # composição da aplicação
│   └── server.js                   # inicialização do servidor
└── tests/                          # testes de integração da API
```

### Testes

```bash
npm test
```

Os testes usam SQLite em memória e cobrem disponibilidade, CRUD, contagem, consulta por nome, validação, conflito e rota inexistente.

---

## English

### Overview

**Partner Products API** is a REST products API created for the Software Architect Bootcamp final challenge. It uses JavaScript, Node.js, Express, an MVC-inspired layered architecture, and SQLite persistence.

### Deliverables

- [Final technical report in PDF, written in Portuguese](docs/entregavel-final-arquitetura-software.pdf)
- [Architecture diagrams in PDF](docs/diagramas-arquitetura.pdf)
- [Editable draw.io source](docs/arquitetura.drawio)
- [C4 container diagram in SVG](docs/diagramas/c4-conteineres.svg)
- [MVC component diagram in SVG](docs/diagramas/mvc-componentes.svg)
- [Bilingual C4 index](docs/architecture/C4.md)
- [ADR-001: Node.js, Express, and SQLite](docs/ADR-001-node-express-sqlite.md)

### Features

- complete products CRUD;
- record count and full listing;
- lookup by ID;
- case-insensitive partial name search;
- SQLite persistence with constraints and an index;
- input validation and standardized error responses;
- OpenAPI 3.1 contract and Swagger UI;
- automated integration tests;
- Docker packaging, health check, and continuous integration.

### Architecture

```text
HTTP client -> Middlewares -> Routes -> Controller -> Service -> Model/Repository -> SQLite
```

The REST adaptation treats the domain and validation as the Model, the HTTP adapter as the Controller, and the returned JSON representation as the View. A Service owns application rules, while the Repository isolates SQL and database mapping.

See [docs/architecture/C4.md](docs/architecture/C4.md) for the system context, containers, API components, create-product sequence, and links to the editable and exported diagrams.

### Technology stack

| Area | Technologies |
|---|---|
| Runtime | JavaScript ES Modules and Node.js 24 |
| API | Express 5 |
| Database | Native SQLite through `node:sqlite` |
| Validation | Zod |
| Security and integration | Helmet and CORS |
| Contract | OpenAPI 3.1 and Swagger UI |
| Tests | Vitest and Supertest |
| Delivery | Docker, Docker Compose, and GitHub Actions |

### Running locally

Node.js 24 or newer is required.

```bash
npm ci
cp .env.example .env
npm run seed
npm start
```

The API listens on `http://localhost:3000`, and Swagger UI is available at `http://localhost:3000/docs`.

For development mode:

```bash
npm run dev
```

For Docker:

```bash
docker compose up --build
```

### Endpoints

| Method | Route | Purpose |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/api/v1/products` | List all products |
| `GET` | `/api/v1/products/count` | Count products |
| `GET` | `/api/v1/products/:id` | Find by ID |
| `GET` | `/api/v1/products/name/:name` | Search by name |
| `POST` | `/api/v1/products` | Create a product |
| `PUT` | `/api/v1/products/:id` | Fully update a product |
| `PATCH` | `/api/v1/products/:id` | Partially update a product |
| `DELETE` | `/api/v1/products/:id` | Delete a product |
| `GET` | `/docs` | Swagger UI |
| `GET` | `/openapi.json` | OpenAPI contract |

### Tests

```bash
npm test
```

The integration suite uses an in-memory SQLite database and covers availability, CRUD, record count, name search, validation, conflicts, and unknown routes.

## Author

Ronoel Lima — Software Architect Bootcamp final challenge, 2026.

## License

[MIT](LICENSE)
