import { ZodError } from 'zod';
import { AppError } from '../errors/AppError.js';

export function notFoundHandler(request, response) {
  return response.status(404).json({
    error: {
      code: 'ROUTE_NOT_FOUND',
      message: `Rota ${request.method} ${request.originalUrl} não encontrada.`,
      requestId: request.id
    }
  });
}

export function errorHandler(error, request, response, _next) {
  if (error instanceof ZodError) {
    return response.status(422).json({
      error: {
        code: 'VALIDATION_ERROR',
        message: 'Os dados enviados são inválidos.',
        details: error.issues.map((issue) => ({
          field: issue.path.join('.') || 'body',
          message: issue.message
        })),
        requestId: request.id
      }
    });
  }

  if (error instanceof AppError) {
    return response.status(error.statusCode).json({
      error: {
        code: error.code,
        message: error.message,
        ...(error.details && { details: error.details }),
        requestId: request.id
      }
    });
  }

  console.error(
    JSON.stringify({
      level: 'error',
      requestId: request.id,
      message: error.message,
      stack: process.env.NODE_ENV === 'production' ? undefined : error.stack
    })
  );

  return response.status(500).json({
    error: {
      code: 'INTERNAL_ERROR',
      message: 'Ocorreu um erro interno inesperado.',
      requestId: request.id
    }
  });
}
