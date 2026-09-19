import { createApp } from './app.js';

const port = Number(process.env.PORT ?? 3000);
const { app, db } = createApp();

const server = app.listen(port, () => {
  console.log(`Partner Products API disponível em http://localhost:${port}`);
  console.log(`Documentação Swagger em http://localhost:${port}/docs`);
});

function shutdown(signal) {
  console.log(`${signal} recebido. Encerrando a aplicação...`);
  server.close(() => {
    db.close();
    process.exit(0);
  });
}

process.on('SIGINT', () => shutdown('SIGINT'));
process.on('SIGTERM', () => shutdown('SIGTERM'));
