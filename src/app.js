import cors from 'cors';
import express from 'express';
import helmet from 'helmet';
import swaggerUi from 'swagger-ui-express';
import { createDatabase } from './config/database.js';
import { openApiDocument } from './config/openapi.js';
import { ProductController } from './controllers/product.controller.js';
import {
  errorHandler,
  notFoundHandler
} from './middlewares/error.middleware.js';
import { requestContext } from './middlewares/request-context.middleware.js';
import { ProductRepository } from './repositories/product.repository.js';
import { createProductRouter } from './routes/product.routes.js';
import { ProductService } from './services/product.service.js';

export function createApp(options = {}) {
  const databasePath = options.databasePath ?? process.env.DATABASE_PATH ?? './data/products.db';
  const db = createDatabase(databasePath);
  const productRepository = new ProductRepository(db);
  const productService = new ProductService(productRepository);
  const productController = new ProductController(productService);

  const app = express();
  app.disable('x-powered-by');
  app.use(requestContext);
  app.use(helmet({ contentSecurityPolicy: false }));
  app.use(cors({ origin: process.env.CORS_ORIGIN ?? '*' }));
  app.use(express.json({ limit: '32kb' }));

  app.get('/health', (request, response) => {
    response.status(200).json({
      data: {
        status: 'ok',
        service: 'partner-products-api',
        timestamp: new Date().toISOString()
      }
    });
  });

  app.use('/docs', swaggerUi.serve, swaggerUi.setup(openApiDocument));
  app.get('/openapi.json', (request, response) => response.json(openApiDocument));
  app.use('/api/v1/products', createProductRouter(productController));

  app.use(notFoundHandler);
  app.use(errorHandler);

  return { app, db, services: { productService } };
}
