-- Base de Datos para Donación de Peluches App Flask
CREATE DATABASE IF NOT EXISTS esquema_peluches;
USE esquema_peluches;

-- Tabla "usuarios"
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(200) NOT NULL,
    contrasena VARCHAR(225) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NULL ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50),
    updated_by VARCHAR(50),
    deleted TINYINT(1) NOT NULL DEFAULT 0,
    CONSTRAINT uq_email UNIQUE (email) 
);

-- Tabla "peluches"
CREATE TABLE IF NOT EXISTS peluches (
    id_peluche INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(500) NOT NULL,
    creador_id INT NOT NULL,
    adoptador_id INT,
    vistas INT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NULL ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50),
    updated_by VARCHAR(50),
    deleted TINYINT(1) NOT NULL DEFAULT 0,
    FOREIGN KEY (creador_id) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (adoptador_id) REFERENCES usuarios(id_usuario) ON DELETE SET NULL
);
