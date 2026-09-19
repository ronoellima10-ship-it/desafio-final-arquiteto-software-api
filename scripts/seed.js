import { createApp } from '../src/app.js';

const { db, services } = createApp();

const products = [
  {
    name: 'Notebook Pro 14',
    description: 'Notebook profissional com 16 GB de RAM e SSD de 512 GB.',
    price: 5499.9,
    stock: 15,
    active: true
  },
  {
    name: 'Teclado Mecânico',
    description: 'Teclado ABNT2 com iluminação ajustável.',
    price: 349.9,
    stock: 30,
    active: true
  },
  {
    name: 'Mouse Sem Fio',
    description: 'Mouse ergonômico com conexão Bluetooth.',
    price: 149.9,
    stock: 25,
    active: true
  }
];

for (const product of products) {
  try {
    services.productService.create(product);
    console.log(`Produto criado: ${product.name}`);
  } catch (error) {
    if (error.code === 'CONFLICT') {
      console.log(`Produto já existente: ${product.name}`);
    } else {
      throw error;
    }
  }
}

db.close();
