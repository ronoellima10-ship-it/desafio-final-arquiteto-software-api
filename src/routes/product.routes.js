import { Router } from 'express';

export function createProductRouter(productController) {
  const router = Router();

  router.get('/count', productController.count);
  router.get('/name/:name', productController.findByName);
  router.get('/', productController.listAll);
  router.get('/:id', productController.findById);
  router.post('/', productController.create);
  router.put('/:id', productController.update);
  router.patch('/:id', productController.update);
  router.delete('/:id', productController.delete);

  return router;
}
