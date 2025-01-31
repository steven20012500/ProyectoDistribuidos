CREATE DATABASE IF NOT EXISTS pedidos;

USE pedidos;

CREATE TABLE IF NOT EXISTS pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY
);

-- Verificar y agregar columnas si no existen
SET @table_name = 'pedidos';

-- Verificar y agregar columna 'sucursal'
SET @sql = NULL;
SELECT
    IF(
        NOT EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_schema = DATABASE()
              AND table_name = @table_name
              AND column_name = 'sucursal'
        ),
        'ALTER TABLE pedidos ADD COLUMN sucursal VARCHAR(255) NOT NULL;',
        NULL
    ) INTO @sql;
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Verificar y agregar columna 'producto'
SET @sql = NULL;
SELECT
    IF(
        NOT EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_schema = DATABASE()
              AND table_name = @table_name
              AND column_name = 'producto'
        ),
        'ALTER TABLE pedidos ADD COLUMN producto VARCHAR(255) NOT NULL;',
        NULL
    ) INTO @sql;
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Verificar y agregar columna 'cantidad'
SET @sql = NULL;
SELECT
    IF(
        NOT EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_schema = DATABASE()
              AND table_name = @table_name
              AND column_name = 'cantidad'
        ),
        'ALTER TABLE pedidos ADD COLUMN cantidad INT NOT NULL;',
        NULL
    ) INTO @sql;
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Verificar y agregar columna 'fecha'
SET @sql = NULL;
SELECT
    IF(
        NOT EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_schema = DATABASE()
              AND table_name = @table_name
              AND column_name = 'fecha'
        ),
        'ALTER TABLE pedidos ADD COLUMN fecha DATETIME NOT NULL;',
        NULL
    ) INTO @sql;
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
