import { randomUUID } from 'node:crypto';

function mapRow(row) {
  if (!row) return null;

  return {
    id: row.id,
    name: row.name,
    description: row.description,
    price: row.price,
    stock: row.stock,
    active: Boolean(row.active),
    createdAt: row.created_at,
    updatedAt: row.updated_at
  };
}

function escapeLike(value) {
  return value.replace(/[\\%_]/g, '\\$&');
}

export class ProductRepository {
  constructor(db) {
    this.db = db;
  }

  findAll() {
    const rows = this.db
      .prepare('SELECT * FROM products ORDER BY created_at DESC, name ASC')
      .all();
    return rows.map(mapRow);
  }

  findById(id) {
    return mapRow(
      this.db.prepare('SELECT * FROM products WHERE id = ?').get(id)
    );
  }

  findByName(name) {
    const pattern = `%${escapeLike(name)}%`;
    const rows = this.db
      .prepare(`
        SELECT * FROM products
        WHERE name LIKE ? ESCAPE '\\' COLLATE NOCASE
        ORDER BY name ASC
      `)
      .all(pattern);
    return rows.map(mapRow);
  }

  findExactName(name, excludedId = null) {
    if (excludedId) {
      return mapRow(
        this.db
          .prepare('SELECT * FROM products WHERE name = ? COLLATE NOCASE AND id <> ?')
          .get(name, excludedId)
      );
    }

    return mapRow(
      this.db
        .prepare('SELECT * FROM products WHERE name = ? COLLATE NOCASE')
        .get(name)
    );
  }

  count() {
    return Number(
      this.db.prepare('SELECT COUNT(*) AS total FROM products').get().total
    );
  }

  create(input) {
    const now = new Date().toISOString();
    const product = {
      id: randomUUID(),
      ...input,
      createdAt: now,
      updatedAt: now
    };

    this.db
      .prepare(`
        INSERT INTO products
          (id, name, description, price, stock, active, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
      `)
      .run(
        product.id,
        product.name,
        product.description,
        product.price,
        product.stock,
        product.active ? 1 : 0,
        product.createdAt,
        product.updatedAt
      );

    return this.findById(product.id);
  }

  update(id, product) {
    const updatedAt = new Date().toISOString();

    this.db
      .prepare(`
        UPDATE products
        SET name = ?, description = ?, price = ?, stock = ?, active = ?, updated_at = ?
        WHERE id = ?
      `)
      .run(
        product.name,
        product.description,
        product.price,
        product.stock,
        product.active ? 1 : 0,
        updatedAt,
        id
      );

    return this.findById(id);
  }

  delete(id) {
    return this.db.prepare('DELETE FROM products WHERE id = ?').run(id).changes > 0;
  }
}
