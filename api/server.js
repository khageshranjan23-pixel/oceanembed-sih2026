import { api } from '../server/api.js';

export const config = { maxDuration: 60 };

export default async function handler(req, res) {
  try {
    const host = req.headers['x-forwarded-host'] || req.headers.host || 'localhost';
    const proto = req.headers['x-forwarded-proto'] || 'https';
    const url = new URL(req.url, proto + '://' + host);
    const chunks = [];
    if (req.method !== 'GET' && req.method !== 'HEAD') {
      for await (const chunk of req) {
        chunks.push(typeof chunk === 'string' ? Buffer.from(chunk) : chunk);
        if (chunks.reduce((s, x) => s + x.length, 0) > 6000) {
          res.status(413).end('Too large'); return;
        }
      }
    }
    const request = new Request(url.toString(), {
      method: req.method,
      headers: req.headers,
      ...(chunks.length ? { body: Buffer.concat(chunks) } : {}),
    });
    const response = await api(request, process.env);
    res.status(response.status);
    for (const [k, v] of response.headers.entries()) res.setHeader(k, v);
    res.end(Buffer.from(await response.arrayBuffer()));
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Unexpected server error.' });
  }
}