-- Añadir columna `activo` a la tabla `categorias`
-- Ejecutar en la base de datos smart_warehouse (TiDB Cloud)

ALTER TABLE categorias ADD COLUMN activo TINYINT(1) NOT NULL DEFAULT 1;

-- Verificar
SELECT COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_DEFAULT
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'categorias';
