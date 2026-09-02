FROM nginx:1.27-alpine

COPY index.html categorias.html productos.html /usr/share/nginx/html/
COPY css/ /usr/share/nginx/html/css/
COPY js/ /usr/share/nginx/html/js/

COPY docker/40-generate-frontend-config.sh /docker-entrypoint.d/40-generate-frontend-config.sh
RUN chmod +x /docker-entrypoint.d/40-generate-frontend-config.sh

EXPOSE 80
