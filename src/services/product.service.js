import { ConflictError, NotFoundError } from '../errors/AppError.js';
import {
  createProductSchema,
  productNameSchema,
  updateProductSchema
} from '../models/product.model.js';

export class ProductService {
  constructor(productRepository) {
    this.productRepository = productRepository;
  }

  listAll() {
    return this.productRepository.findAll();
  }

  findById(id) {
    const product = this.productRepository.findById(id);

    if (!product) {
      throw new NotFoundError(`Produto com ID ${id} não encontrado.`);
    }

    return product;
  }

  findByName(rawName) {
    const name = productNameSchema.parse(rawName);
    return this.productRepository.findByName(name);
  }

  count() {
    return this.productRepository.count();
  }

  create(rawInput) {
    const input = createProductSchema.parse(rawInput);

    if (this.productRepository.findExactName(input.name)) {
      throw new ConflictError(`Já existe um produto com o nome "${input.name}".`);
    }

    return this.productRepository.create(input);
  }

  update(id, rawInput) {
    const current = this.findById(id);
    const input = updateProductSchema.parse(rawInput);

    if (
      input.name &&
      this.productRepository.findExactName(input.name, id)
    ) {
      throw new ConflictError(`Já existe um produto com o nome "${input.name}".`);
    }

    return this.productRepository.update(id, { ...current, ...input });
  }

  delete(id) {
    this.findById(id);
    this.productRepository.delete(id);
  }
}
