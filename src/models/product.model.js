import { z } from 'zod';

const moneySchema = z.coerce
  .number({ error: 'O preço deve ser numérico.' })
  .finite('O preço deve ser finito.')
  .min(0, 'O preço não pode ser negativo.')
  .max(999_999_999.99, 'O preço excede o limite permitido.');

const stockSchema = z.coerce
  .number({ error: 'O estoque deve ser numérico.' })
  .int('O estoque deve ser inteiro.')
  .min(0, 'O estoque não pode ser negativo.')
  .max(1_000_000, 'O estoque excede o limite permitido.');

const productFields = {
  name: z
    .string({ error: 'O nome é obrigatório.' })
    .trim()
    .min(2, 'O nome deve ter ao menos 2 caracteres.')
    .max(120, 'O nome deve ter no máximo 120 caracteres.'),
  description: z
    .string({ error: 'A descrição deve ser um texto.' })
    .trim()
    .max(500, 'A descrição deve ter no máximo 500 caracteres.'),
  price: moneySchema,
  stock: stockSchema,
  active: z.boolean({ error: 'O campo active deve ser booleano.' })
};

export const createProductSchema = z
  .object({
    ...productFields,
    description: productFields.description.optional().default(''),
    active: productFields.active.optional().default(true)
  })
  .strict('Existem campos não reconhecidos no corpo da requisição.');

export const updateProductSchema = z
  .object(productFields)
  .partial()
  .strict('Existem campos não reconhecidos no corpo da requisição.')
  .refine((value) => Object.keys(value).length > 0, {
    message: 'Informe ao menos um campo para atualização.'
  });

export const productNameSchema = z
  .string()
  .trim()
  .min(1, 'Informe um nome para a pesquisa.')
  .max(120, 'O nome pesquisado deve ter no máximo 120 caracteres.');
