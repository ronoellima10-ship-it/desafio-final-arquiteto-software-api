const productSchema = {
  type: 'object',
  required: ['id', 'name', 'description', 'price', 'stock', 'active', 'createdAt', 'updatedAt'],
  properties: {
    id: { type: 'string', format: 'uuid', example: '150d1a61-e0b8-4cd2-a39d-72e33408edb1' },
    name: { type: 'string', example: 'Notebook Pro 14' },
    description: { type: 'string', example: 'Notebook profissional com 16 GB de RAM.' },
    price: { type: 'number', format: 'double', minimum: 0, example: 5499.9 },
    stock: { type: 'integer', minimum: 0, example: 15 },
    active: { type: 'boolean', example: true },
    createdAt: { type: 'string', format: 'date-time' },
    updatedAt: { type: 'string', format: 'date-time' }
  }
};

const productInputSchema = {
  type: 'object',
  required: ['name', 'price', 'stock'],
  additionalProperties: false,
  properties: {
    name: { type: 'string', minLength: 2, maxLength: 120, example: 'Notebook Pro 14' },
    description: { type: 'string', maxLength: 500, default: '', example: 'Notebook profissional com 16 GB de RAM.' },
    price: { type: 'number', minimum: 0, example: 5499.9 },
    stock: { type: 'integer', minimum: 0, example: 15 },
    active: { type: 'boolean', default: true, example: true }
  }
};

const singleResponse = {
  type: 'object',
  properties: { data: { $ref: '#/components/schemas/Product' } }
};

const errorResponse = {
  description: 'Erro da API',
  content: {
    'application/json': {
      schema: { $ref: '#/components/schemas/Error' }
    }
  }
};

export const openApiDocument = {
  openapi: '3.1.0',
  info: {
    title: 'Partner Products API',
    version: '1.0.0',
    description: 'API REST para disponibilizar dados de produtos aos parceiros, implementada em JavaScript com Node.js, Express, MVC e SQLite.'
  },
  servers: [{ url: 'http://localhost:3000', description: 'Ambiente local' }],
  tags: [
    { name: 'Health', description: 'Disponibilidade do serviço' },
    { name: 'Products', description: 'CRUD e consultas de produtos' }
  ],
  paths: {
    '/health': {
      get: {
        tags: ['Health'],
        summary: 'Verifica a disponibilidade da API',
        responses: { 200: { description: 'API disponível' } }
      }
    },
    '/api/v1/products': {
      get: {
        tags: ['Products'],
        summary: 'Lista todos os produtos',
        responses: {
          200: {
            description: 'Lista de produtos',
            content: {
              'application/json': {
                schema: {
                  type: 'object',
                  properties: {
                    data: { type: 'array', items: { $ref: '#/components/schemas/Product' } },
                    meta: { $ref: '#/components/schemas/ListMeta' }
                  }
                }
              }
            }
          }
        }
      },
      post: {
        tags: ['Products'],
        summary: 'Cria um produto',
        requestBody: {
          required: true,
          content: { 'application/json': { schema: { $ref: '#/components/schemas/ProductInput' } } }
        },
        responses: {
          201: { description: 'Produto criado', content: { 'application/json': { schema: singleResponse } } },
          409: errorResponse,
          422: errorResponse
        }
      }
    },
    '/api/v1/products/count': {
      get: {
        tags: ['Products'],
        summary: 'Conta todos os produtos',
        responses: {
          200: {
            description: 'Quantidade total',
            content: {
              'application/json': {
                schema: {
                  type: 'object',
                  properties: { data: { type: 'object', properties: { total: { type: 'integer' } } } }
                }
              }
            }
          }
        }
      }
    },
    '/api/v1/products/name/{name}': {
      get: {
        tags: ['Products'],
        summary: 'Pesquisa produtos pelo nome',
        parameters: [{ name: 'name', in: 'path', required: true, schema: { type: 'string' } }],
        responses: { 200: { description: 'Produtos correspondentes' }, 422: errorResponse }
      }
    },
    '/api/v1/products/{id}': {
      parameters: [{ name: 'id', in: 'path', required: true, schema: { type: 'string', format: 'uuid' } }],
      get: {
        tags: ['Products'],
        summary: 'Busca um produto pelo ID',
        responses: {
          200: { description: 'Produto encontrado', content: { 'application/json': { schema: singleResponse } } },
          404: errorResponse
        }
      },
      put: {
        tags: ['Products'],
        summary: 'Atualiza um produto',
        requestBody: {
          required: true,
          content: { 'application/json': { schema: { $ref: '#/components/schemas/ProductUpdate' } } }
        },
        responses: { 200: { description: 'Produto atualizado' }, 404: errorResponse, 409: errorResponse, 422: errorResponse }
      },
      patch: {
        tags: ['Products'],
        summary: 'Atualiza parcialmente um produto',
        requestBody: {
          required: true,
          content: { 'application/json': { schema: { $ref: '#/components/schemas/ProductUpdate' } } }
        },
        responses: { 200: { description: 'Produto atualizado' }, 404: errorResponse, 409: errorResponse, 422: errorResponse }
      },
      delete: {
        tags: ['Products'],
        summary: 'Exclui um produto',
        responses: { 204: { description: 'Produto excluído' }, 404: errorResponse }
      }
    }
  },
  components: {
    schemas: {
      Product: productSchema,
      ProductInput: productInputSchema,
      ProductUpdate: { ...productInputSchema, required: [], minProperties: 1 },
      ListMeta: {
        type: 'object',
        properties: { total: { type: 'integer', minimum: 0 } }
      },
      Error: {
        type: 'object',
        properties: {
          error: {
            type: 'object',
            properties: {
              code: { type: 'string', example: 'NOT_FOUND' },
              message: { type: 'string' },
              requestId: { type: 'string', format: 'uuid' }
            }
          }
        }
      }
    }
  }
};
