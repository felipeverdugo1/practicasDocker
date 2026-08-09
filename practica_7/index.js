const express = require('express');
const { Pool } = require('pg');
const redis = require('redis');

const app = express();
app.use(express.json());

// Conexión a PostgreSQL usando el nombre de host del servicio en Docker
const pool = new Pool({
  host: process.env.DB_HOST || 'db',
  user: process.env.POSTGRES_USER,
  password: process.env.POSTGRES_PASSWORD,
  database: process.env.POSTGRES_DB,
  port: 5432,
});

// Conexión a Redis usando el nombre de host del servicio en Docker
const redisClient = redis.createClient({
  url: `redis://${process.env.REDIS_HOST || 'cache'}:6379`
});

redisClient.connect().catch(console.error);

app.get('/api/v0/status', async (req, res) => {
  try {
    // 1. Intentar leer desde la caché de Redis
    const cachedStatus = await redisClient.get('app_status');
    if (cachedStatus) {
      return res.json({ fuente: 'cache_redis', mensaje: cachedStatus });
    }

    // 2. Si no está en caché, consultar PostgreSQL
    const result = await pool.query('SELECT NOW() as fecha_actual');
    const mensaje = `DB Conectada OK a las: ${result.rows[0].fecha_actual}`;

    // 3. Guardar en Redis por 10 segundos
    await redisClient.setEx('app_status', 10, mensaje);

    return res.json({ fuente: 'base_de_datos', mensaje });
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
});

app.listen(3000, () => console.log('API corriendo en puerto 3000'));