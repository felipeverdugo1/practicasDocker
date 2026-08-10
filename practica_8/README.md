# Comandos útiles

## Levantar el proyecto

```bash
docker compose up --build
```

## Inspección general

```bash
docker compose ps
docker network ls
docker network inspect docker-practica_frontend_net
docker network inspect docker-practica_backend_net
```

## Meterse dentro de un contenedor

```bash
docker exec -it <container> sh
```

## Desde adentro de un contenedor

```bash
ping backend
ping db
wget -O- http://backend:5000/api/health
```

Paso 1 — Escalar:

bash
docker compose up --build --scale backend=3


Paso 2 — Pegarle varias veces al endpoint y mirar qué cambia:

bash
for i in {1..6}; do curl -s http://localhost:8080/api/hello; echo; done
