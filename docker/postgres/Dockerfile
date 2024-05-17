FROM postgres:13-alpine
COPY init.sql /docker-entrypoint-initdb.d
CMD ["docker-entrypoint.sh", "postgres"]
