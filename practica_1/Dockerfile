FROM nginx:alpine

WORKDIR /app

# Defines el puerto interno que usará la aplicación
ENV PUERTO=80

# Documentas que el contenedor expondrá ese puerto interno
EXPOSE ${PUERTO}

CMD ["nginx", "-g", "daemon off;"]


