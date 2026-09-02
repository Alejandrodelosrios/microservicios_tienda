CREATE TABLE IF NOT EXISTS producto (
    codigo SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    precio NUMERIC(10, 2) NOT NULL,
    categoria_codigo INTEGER NOT NULL
);
