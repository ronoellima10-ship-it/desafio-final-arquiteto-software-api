export class AppError extends Error {
  constructor(message, statusCode = 500, code = 'INTERNAL_ERROR', details) {
    super(message);
    this.name = 'AppError';
    this.statusCode = statusCode;
    this.code = code;
    this.details = details;
    Error.captureStackTrace?.(this, AppError);
  }
}

export class NotFoundError extends AppError {
  constructor(message = 'Recurso não encontrado.') {
    super(message, 404, 'NOT_FOUND');
  }
}

export class ConflictError extends AppError {
  constructor(message = 'O recurso já existe.') {
    super(message, 409, 'CONFLICT');
  }
}
