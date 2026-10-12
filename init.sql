-- ============================================================
-- BASE DE DATOS: SmartWarehouse (Almacén Fácil)
-- Motor: InnoDB
-- Codificación: utf8mb4
-- ============================================================

CREATE DATABASE IF NOT EXISTS smart_warehouse
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE smart_warehouse;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS incidencias;
DROP TABLE IF EXISTS busquedas;
DROP TABLE IF EXISTS movimientos;
DROP TABLE IF EXISTS inventario;
DROP TABLE IF EXISTS ubicaciones;
DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS categorias;
DROP TABLE IF EXISTS almacenes;
DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS roles;

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================
-- 1. ROLES
-- ============================================================
CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ============================================================
-- 2. USUARIOS
-- ============================================================
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    rol_id INT NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultimo_acceso TIMESTAMP NULL,
    CONSTRAINT fk_usuarios_roles
        FOREIGN KEY (rol_id) REFERENCES roles(id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- ============================================================
-- 3. ALMACENES
-- ============================================================
CREATE TABLE almacenes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(255),
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ============================================================
-- 4. CATEGORÍAS
-- ============================================================
CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ============================================================
-- 5. PRODUCTOS
-- ============================================================
CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(50) NOT NULL UNIQUE,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    categoria_id INT,
    unidad_medida VARCHAR(20) DEFAULT 'pieza',
    stock_minimo INT DEFAULT 0 CHECK (stock_minimo >= 0),
    foto_url VARCHAR(255),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_productos_categorias
        FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        ON UPDATE CASCADE ON DELETE SET NULL,
    INDEX idx_productos_nombre (nombre),
    INDEX idx_productos_codigo (codigo)
) ENGINE=InnoDB;

-- ============================================================
-- 6. UBICACIONES (Pasillo, Estante, Nivel)
-- ============================================================
CREATE TABLE ubicaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    almacen_id INT NOT NULL,
    pasillo VARCHAR(10) NOT NULL,
    estante VARCHAR(10) NOT NULL,
    nivel VARCHAR(10) NOT NULL,
    codigo_ubicacion VARCHAR(20) NOT NULL UNIQUE,  -- Ej: 'P3-B-02'
    codigo_qr VARCHAR(255) UNIQUE,                  -- Contenido del QR físico
    coordenada_x DECIMAL(10,2) NULL,                -- Para mapa y distancia
    coordenada_y DECIMAL(10,2) NULL,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_ubicaciones_almacenes
        FOREIGN KEY (almacen_id) REFERENCES almacenes(id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    UNIQUE KEY uk_ubicacion_fisica (almacen_id, pasillo, estante, nivel),
    INDEX idx_ubicaciones_codigo (codigo_ubicacion),
    INDEX idx_ubicaciones_pasillo_estante_nivel (pasillo, estante, nivel)
) ENGINE=InnoDB;

-- ============================================================
-- 7. INVENTARIO (Stock por producto y ubicación)
-- ============================================================
CREATE TABLE inventario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT NOT NULL,
    ubicacion_id INT NOT NULL,
    cantidad INT NOT NULL DEFAULT 0 CHECK (cantidad >= 0),
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_inventario_productos
        FOREIGN KEY (producto_id) REFERENCES productos(id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_inventario_ubicaciones
        FOREIGN KEY (ubicacion_id) REFERENCES ubicaciones(id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    UNIQUE KEY uk_inventario_producto_ubicacion (producto_id, ubicacion_id),
    INDEX idx_inventario_producto (producto_id),
    INDEX idx_inventario_ubicacion (ubicacion_id)
) ENGINE=InnoDB;

-- ============================================================
-- 8. MOVIMIENTOS (Entradas, salidas, traslados, ajustes)
-- ============================================================
CREATE TABLE movimientos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo ENUM('ENTRADA','SALIDA','TRASLADO','AJUSTE') NOT NULL,
    producto_id INT NOT NULL,
    ubicacion_origen_id INT NULL,
    ubicacion_destino_id INT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    usuario_id INT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    referencia VARCHAR(100),
    observaciones TEXT,
    CONSTRAINT fk_movimientos_productos
        FOREIGN KEY (producto_id) REFERENCES productos(id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_movimientos_ubicacion_origen
        FOREIGN KEY (ubicacion_origen_id) REFERENCES ubicaciones(id)
        ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_movimientos_ubicacion_destino
        FOREIGN KEY (ubicacion_destino_id) REFERENCES ubicaciones(id)
        ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_movimientos_usuarios
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    INDEX idx_movimientos_fecha (fecha),
    INDEX idx_movimientos_producto (producto_id),
    INDEX idx_movimientos_usuario (usuario_id)
) ENGINE=InnoDB;

-- ============================================================
-- 9. BÚSQUEDAS (Métricas de localización)
-- ============================================================
CREATE TABLE busquedas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    producto_id INT NULL,
    termino_busqueda VARCHAR(150) NOT NULL,
    fecha_hora_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_hora_fin TIMESTAMP NULL,
    tiempo_busqueda_segundos INT NULL,
    ubicacion_encontrada_id INT NULL,
    exito BOOLEAN DEFAULT FALSE,
    observaciones TEXT,
    CONSTRAINT fk_busquedas_usuarios
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_busquedas_productos
        FOREIGN KEY (producto_id) REFERENCES productos(id)
        ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_busquedas_ubicaciones
        FOREIGN KEY (ubicacion_encontrada_id) REFERENCES ubicaciones(id)
        ON UPDATE CASCADE ON DELETE SET NULL,
    INDEX idx_busquedas_fecha (fecha_hora_inicio),
    INDEX idx_busquedas_usuario (usuario_id),
    INDEX idx_busquedas_producto (producto_id)
) ENGINE=InnoDB;

-- ============================================================
-- 10. INCIDENCIAS (Productos mal ubicados, faltantes, dañados)
-- ============================================================
CREATE TABLE incidencias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo ENUM('MAL_UBICADO','FALTANTE','DANADO','OTRO') NOT NULL,
    producto_id INT NULL,
    ubicacion_id INT NULL,
    usuario_id INT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    descripcion TEXT,
    resuelta BOOLEAN DEFAULT FALSE,
    fecha_resolucion TIMESTAMP NULL,
    CONSTRAINT fk_incidencias_productos
        FOREIGN KEY (producto_id) REFERENCES productos(id)
        ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_incidencias_ubicaciones
        FOREIGN KEY (ubicacion_id) REFERENCES ubicaciones(id)
        ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_incidencias_usuarios
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    INDEX idx_incidencias_fecha (fecha),
    INDEX idx_incidencias_tipo (tipo)
) ENGINE=InnoDB;
