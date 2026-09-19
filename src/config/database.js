import { mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { DatabaseSync } from 'node:sqlite';

function resolveDatabasePath(databasePath) {
  if (databasePath === ':memory:') return databasePath;

  const absolutePath = resolve(databasePath);
  mkdirSync(dirname(absolutePath), { recursive: true });
  return absolutePath;
}

export function createDatabase(databasePath = './data/products.db') {
  const db = new DatabaseSync(resolveDatabasePath(databasePath));

  db.exec('PRAGMA foreign_keys = ON;');
  db.exec('PRAGMA busy_timeout = 5000;');

  if (databasePath !== ':memory:') {
    db.exec('PRAGMA journal_mode = WAL;');
  }

  db.exec(`
    CREATE TABLE IF NOT EXISTS products (
      id TEXT PRIMARY KEY,
      name TEXT NOT NULL COLLATE NOCASE UNIQUE,
      description TEXT NOT NULL DEFAULT '',
      price REAL NOT NULL CHECK (price >= 0),
      stock INTEGER NOT NULL CHECK (stock >= 0),
      active INTEGER NOT NULL DEFAULT 1 CHECK (active IN (0, 1)),
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL
    );

    CREATE INDEX IF NOT EXISTS idx_products_name
      ON products(name COLLATE NOCASE);
  `);

  return db;
}
