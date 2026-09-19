import request from 'supertest';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';
import { createApp } from '../src/app.js';

describe('Partner Products API', () => {
  let api;
  let db;

  beforeEach(() => {
    const context = createApp({ databasePath: ':memory:' });
    api = context.app;
    db = context.db;
  });

  afterEach(() => {
    db.close();
  });

  it('informa que o serviço está disponível', async () => {
    const response = await request(api).get('/health');

    expect(response.status).toBe(200);
    expect(response.body.data.status).toBe('ok');
    expect(response.headers['x-request-id']).toBeTruthy();
  });

  it('executa o fluxo completo de CRUD e contagem', async () => {
    const creation = await request(api).post('/api/v1/products').send({
      name: 'Notebook Pro 14',
      description: 'Notebook para uso profissional.',
      price: 5499.9,
      stock: 15
    });

    expect(creation.status).toBe(201);
    expect(creation.headers.location).toContain(creation.body.data.id);
    expect(creation.body.data.active).toBe(true);
    const productId = creation.body.data.id;

    const list = await request(api).get('/api/v1/products');
    expect(list.status).toBe(200);
    expect(list.body.meta.total).toBe(1);
    expect(list.body.data[0].id).toBe(productId);

    const byId = await request(api).get(`/api/v1/products/${productId}`);
    expect(byId.status).toBe(200);
    expect(byId.body.data.name).toBe('Notebook Pro 14');

    const count = await request(api).get('/api/v1/products/count');
    expect(count.status).toBe(200);
    expect(count.body.data.total).toBe(1);

    const update = await request(api)
      .patch(`/api/v1/products/${productId}`)
      .send({ price: 5199.9, stock: 12 });
    expect(update.status).toBe(200);
    expect(update.body.data.price).toBe(5199.9);
    expect(update.body.data.stock).toBe(12);

    const deletion = await request(api).delete(`/api/v1/products/${productId}`);
    expect(deletion.status).toBe(204);

    const missing = await request(api).get(`/api/v1/products/${productId}`);
    expect(missing.status).toBe(404);
    expect(missing.body.error.code).toBe('NOT_FOUND');
  });

  it('pesquisa produtos por parte do nome sem diferenciar maiúsculas', async () => {
    await request(api).post('/api/v1/products').send({
      name: 'Teclado Mecânico',
      price: 349.9,
      stock: 30
    });
    await request(api).post('/api/v1/products').send({
      name: 'Mouse Sem Fio',
      price: 149.9,
      stock: 25
    });

    const response = await request(api).get('/api/v1/products/name/TECLADO');

    expect(response.status).toBe(200);
    expect(response.body.meta.total).toBe(1);
    expect(response.body.data[0].name).toBe('Teclado Mecânico');
  });

  it('rejeita produto inválido com erro padronizado', async () => {
    const response = await request(api).post('/api/v1/products').send({
      name: 'X',
      price: -10,
      stock: 1.5
    });

    expect(response.status).toBe(422);
    expect(response.body.error.code).toBe('VALIDATION_ERROR');
    expect(response.body.error.details.length).toBeGreaterThanOrEqual(3);
  });

  it('impede nomes de produtos duplicados', async () => {
    const payload = { name: 'Monitor 27', price: 1699, stock: 8 };
    await request(api).post('/api/v1/products').send(payload);

    const response = await request(api)
      .post('/api/v1/products')
      .send({ ...payload, name: 'monitor 27' });

    expect(response.status).toBe(409);
    expect(response.body.error.code).toBe('CONFLICT');
  });

  it('retorna erro padronizado para rota inexistente', async () => {
    const response = await request(api).get('/rota-que-nao-existe');

    expect(response.status).toBe(404);
    expect(response.body.error.code).toBe('ROUTE_NOT_FOUND');
  });
});
