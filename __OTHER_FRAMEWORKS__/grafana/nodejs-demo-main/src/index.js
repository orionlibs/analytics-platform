import express from 'express';
import { collectDefaultMetrics, register } from 'prom-client';

collectDefaultMetrics();

const app = express();

const port = 4001;
const hostname = '0.0.0.0';

app.get('/', (_req, res) => {
    res.end('Greetings from Node.js!');
});

app.get('/metrics', async (_req, res) => {
  try {
    res.set('Content-Type', register.contentType);
    res.end(await register.metrics());
  } catch (err) {
    res.status(500).end(err);
  }
});

try {
  app.listen(port, hostname, () => {
    console.log(`🚀 App listening at http://${hostname}:${port}`);
  });
} catch (error) {
  console.error('💥 Failed to start app!', error);
}
