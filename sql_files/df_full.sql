CREATE TABLE IF NOT EXISTS df_full (
    cod_localidad INT NOT NULL,
    id_provincia INT NOT NULL,
    id_departamento INT NOT NULL,
    categoria VARCHAR(255) NOT NULL,
    provincia VARCHAR(255) NOT NULL,
    localidad VARCHAR(255) NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    domicilio VARCHAR(255),
    codigo_postal VARCHAR(255),
    numero_telefono VARCHAR(255),
    mail VARCHAR(255),
    web VARCHAR(255)
);
