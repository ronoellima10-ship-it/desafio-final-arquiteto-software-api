export class ProductController {
  constructor(productService) {
    this.productService = productService;
  }

  listAll = (request, response) => {
    const products = this.productService.listAll();
    return response.status(200).json({
      data: products,
      meta: { total: products.length }
    });
  };

  findById = (request, response) => {
    const product = this.productService.findById(request.params.id);
    return response.status(200).json({ data: product });
  };

  findByName = (request, response) => {
    const products = this.productService.findByName(request.params.name);
    return response.status(200).json({
      data: products,
      meta: { total: products.length, query: request.params.name }
    });
  };

  count = (request, response) => {
    return response.status(200).json({
      data: { total: this.productService.count() }
    });
  };

  create = (request, response) => {
    const product = this.productService.create(request.body);
    return response
      .location(`/api/v1/products/${product.id}`)
      .status(201)
      .json({ data: product });
  };

  update = (request, response) => {
    const product = this.productService.update(request.params.id, request.body);
    return response.status(200).json({ data: product });
  };

  delete = (request, response) => {
    this.productService.delete(request.params.id);
    return response.status(204).send();
  };
}
