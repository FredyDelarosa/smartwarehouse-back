-- ============================================================
-- FIX: reinserción de datos transaccionales por CÓDIGO
-- (no depende de IDs autoincrementales)
-- ============================================================
USE smart_warehouse;

-- 1. Limpiar (orden por FKs)
DELETE FROM incidencias;
DELETE FROM busquedas;
DELETE FROM movimientos;
DELETE FROM inventario;

-- ============================================================
-- 2. INVENTARIO
-- ============================================================
INSERT INTO inventario (producto_id, ubicacion_id, cantidad)
SELECT p.id, u.id, v.cantidad
FROM (
    -- Tornillería (Pasillo 3)
    SELECT 'T001' AS codigo_producto, 'P3-A-01' AS codigo_ubicacion, 350 AS cantidad UNION ALL
    SELECT 'T002', 'P3-A-02', 520 UNION ALL
    SELECT 'T003', 'P3-A-03', 800 UNION ALL
    SELECT 'T004', 'P3-B-01', 280 UNION ALL
    SELECT 'T005', 'P3-B-02', 410 UNION ALL
    SELECT 'T006', 'P3-B-03', 620 UNION ALL
    SELECT 'T007', 'P3-C-01', 190 UNION ALL
    SELECT 'T008', 'P3-C-02', 230 UNION ALL
    SELECT 'T009', 'P3-C-03', 950 UNION ALL
    SELECT 'T010', 'P3-D-01', 480 UNION ALL
    SELECT 'T001', 'P3-D-02', 120 UNION ALL
    SELECT 'T003', 'P3-D-03', 200 UNION ALL
    SELECT 'T009', 'P3-E-01', 300 UNION ALL
    -- Herramientas manuales (Pasillo 2)
    SELECT 'HM01', 'P2-A-01', 18 UNION ALL
    SELECT 'HM02', 'P2-A-02', 25 UNION ALL
    SELECT 'HM03', 'P2-A-03', 22 UNION ALL
    SELECT 'HM04', 'P2-B-01', 30 UNION ALL
    SELECT 'HM05', 'P2-B-02', 28 UNION ALL
    SELECT 'HM06', 'P2-B-03', 14 UNION ALL
    -- Herramientas eléctricas (Pasillo 2)
    SELECT 'HE01', 'P2-C-01', 7 UNION ALL
    SELECT 'HE02', 'P2-C-02', 6 UNION ALL
    SELECT 'HE03', 'P2-C-03', 4 UNION ALL
    SELECT 'HE04', 'P2-D-01', 5 UNION ALL
    SELECT 'HE05', 'P2-D-02', 3 UNION ALL
    -- EPP (Pasillo 1)
    SELECT 'G001', 'P1-A-01', 180 UNION ALL
    SELECT 'G002', 'P1-A-02', 120 UNION ALL
    SELECT 'G003', 'P1-A-03', 65 UNION ALL
    SELECT 'G004', 'P1-B-01', 250 UNION ALL
    SELECT 'G005', 'P1-B-02', 210 UNION ALL
    SELECT 'G006', 'P1-B-03', 35 UNION ALL
    SELECT 'G001', 'P1-C-01', 60 UNION ALL
    SELECT 'G005', 'P1-C-02', 80 UNION ALL
    -- Insumos (Pasillo 1)
    SELECT 'I001', 'P1-D-01', 45 UNION ALL
    SELECT 'I002', 'P1-D-02', 75 UNION ALL
    SELECT 'I003', 'P1-D-03', 60 UNION ALL
    SELECT 'I004', 'P1-E-01', 40 UNION ALL
    SELECT 'I005', 'P1-E-02', 22 UNION ALL
    SELECT 'I001', 'P1-E-03', 20 UNION ALL
    -- Eléctrico (Pasillo 4)
    SELECT 'E001', 'P4-A-01', 14 UNION ALL
    SELECT 'E002', 'P4-A-02', 16 UNION ALL
    SELECT 'E003', 'P4-A-03', 90 UNION ALL
    SELECT 'E004', 'P4-B-01', 85 UNION ALL
    SELECT 'E005', 'P4-B-02', 140 UNION ALL
    SELECT 'E006', 'P4-B-03', 110 UNION ALL
    SELECT 'E001', 'P4-D-01', 6 UNION ALL
    SELECT 'E005', 'P4-D-02', 60 UNION ALL
    -- Plomería (Pasillo 4)
    SELECT 'P001', 'P4-C-01', 55 UNION ALL
    SELECT 'P002', 'P4-C-02', 180 UNION ALL
    SELECT 'P003', 'P4-C-03', 140 UNION ALL
    SELECT 'P004', 'P4-D-03', 32 UNION ALL
    SELECT 'P005', 'P4-E-01', 40 UNION ALL
    SELECT 'P002', 'P4-E-02', 80 UNION ALL
    -- Pintura (Pasillo 5)
    SELECT 'N001', 'P5-A-01', 12 UNION ALL
    SELECT 'N002', 'P5-A-02', 18 UNION ALL
    SELECT 'N003', 'P5-A-03', 55 UNION ALL
    SELECT 'N004', 'P5-B-01', 48 UNION ALL
    SELECT 'N005', 'P5-B-02', 35 UNION ALL
    SELECT 'N006', 'P5-B-03', 10 UNION ALL
    SELECT 'N007', 'P5-C-01', 22 UNION ALL
    SELECT 'N001', 'P5-C-02', 5 UNION ALL
    SELECT 'N002', 'P5-C-03', 6 UNION ALL
    SELECT 'N004', 'P5-D-01', 25
) v
JOIN productos  p ON p.codigo = v.codigo_producto
JOIN ubicaciones u ON u.codigo_ubicacion = v.codigo_ubicacion;

-- ============================================================
-- 3. MOVIMIENTOS
-- ============================================================
INSERT INTO movimientos (tipo, producto_id, ubicacion_origen_id, ubicacion_destino_id,
                         cantidad, usuario_id, fecha, referencia, observaciones)
SELECT v.tipo, p.id, uo.id, ud.id, v.cantidad, us.id, v.fecha, v.referencia, v.observaciones
FROM (
    -- Julio 2025
    SELECT 'ENTRADA' AS tipo, 'T001' AS codigo_producto, NULL AS codigo_origen, 'P3-A-01' AS codigo_destino, 400 AS cantidad, 'carlos.mendez@xyz.com' AS email_usuario, '2025-07-03 09:15:00' AS fecha, 'OC-2025-0712' AS referencia, 'Recepción proveedor Aceros del Norte' AS observaciones UNION ALL
    SELECT 'ENTRADA', 'T002', NULL, 'P3-A-02', 500, 'carlos.mendez@xyz.com', '2025-07-03 09:40:00', 'OC-2025-0712', 'Recepción proveedor Aceros del Norte' UNION ALL
    SELECT 'ENTRADA', 'G001', NULL, 'P1-A-01', 200, 'maria.lopez@xyz.com', '2025-07-04 10:10:00', 'OC-2025-0715', 'Ingreso EPP seguridad' UNION ALL
    SELECT 'SALIDA', 'T001', 'P3-A-01', NULL, 50, 'jorge.hernandez@xyz.com', '2025-07-08 11:20:00', 'REQ-MTO-0221', 'Consumo área mantenimiento' UNION ALL
    SELECT 'SALIDA', 'G001', 'P1-A-01', NULL, 20, 'jorge.hernandez@xyz.com', '2025-07-08 11:25:00', 'REQ-MTO-0221', 'Entrega EPP a cuadrilla 3' UNION ALL
    SELECT 'ENTRADA', 'E001', NULL, 'P4-A-01', 15, 'carlos.mendez@xyz.com', '2025-07-10 08:55:00', 'OC-2025-0721', 'Recepción material eléctrico' UNION ALL
    SELECT 'SALIDA', 'E001', 'P4-A-01', NULL, 2, 'maria.lopez@xyz.com', '2025-07-15 16:00:00', 'REQ-ELE-0110', 'Instalación nave 2' UNION ALL
    SELECT 'TRASLADO', 'T009', 'P3-C-03', 'P3-E-01', 200, 'jorge.hernandez@xyz.com', '2025-07-18 15:10:00', NULL, 'Reubicación por falta de espacio' UNION ALL
    SELECT 'AJUSTE', 'T003', 'P3-A-03', NULL, 15, 'luis.ramirez@xyz.com', '2025-07-20 18:00:00', 'AJU-2025-003', 'Ajuste por conteo físico (reducción)' UNION ALL
    SELECT 'ENTRADA', 'P001', NULL, 'P4-C-01', 60, 'carlos.mendez@xyz.com', '2025-07-22 09:00:00', 'OC-2025-0728', 'Recepción plomería' UNION ALL
    SELECT 'SALIDA', 'P002', 'P4-C-02', NULL, 30, 'jorge.hernandez@xyz.com', '2025-07-24 10:30:00', 'REQ-PLO-0140', 'Mantenimiento hidráulico' UNION ALL
    SELECT 'ENTRADA', 'N001', NULL, 'P5-A-01', 15, 'carlos.mendez@xyz.com', '2025-07-28 09:20:00', 'OC-2025-0731', 'Recepción pintura' UNION ALL
    SELECT 'SALIDA', 'N003', 'P5-A-03', NULL, 10, 'jorge.hernandez@xyz.com', '2025-07-29 11:45:00', 'REQ-PIN-0155', 'Trabajos nave 1' UNION ALL
    -- Agosto 2025
    SELECT 'ENTRADA', 'T004', NULL, 'P3-B-01', 300, 'carlos.mendez@xyz.com', '2025-08-01 09:05:00', 'OC-2025-0801', 'Recepción tornillería' UNION ALL
    SELECT 'ENTRADA', 'G005', NULL, 'P1-B-02', 250, 'maria.lopez@xyz.com', '2025-08-02 10:15:00', 'OC-2025-0803', 'Ingreso EPP respiratoria' UNION ALL
    SELECT 'SALIDA', 'G005', 'P1-B-02', NULL, 40, 'jorge.hernandez@xyz.com', '2025-08-05 07:50:00', 'REQ-MTO-0240', 'Entrega a cuadrilla de soldadura' UNION ALL
    SELECT 'SALIDA', 'G002', 'P1-A-02', NULL, 15, 'jorge.hernandez@xyz.com', '2025-08-06 08:20:00', 'REQ-MTO-0241', 'Entrega lentes a nuevo personal' UNION ALL
    SELECT 'TRASLADO', 'G001', 'P1-A-01', 'P1-C-01', 60, 'jorge.hernandez@xyz.com', '2025-08-08 15:30:00', NULL, 'Desdoblamiento de inventario' UNION ALL
    SELECT 'ENTRADA', 'E001', NULL, 'P4-A-01', 10, 'carlos.mendez@xyz.com', '2025-08-11 09:35:00', 'OC-2025-0812', 'Recepción cable' UNION ALL
    SELECT 'SALIDA', 'E001', 'P4-A-01', NULL, 3, 'maria.lopez@xyz.com', '2025-08-13 14:00:00', 'REQ-ELE-0125', 'Trabajos en subestación' UNION ALL
    SELECT 'SALIDA', 'T001', 'P3-A-01', NULL, 80, 'jorge.hernandez@xyz.com', '2025-08-14 10:10:00', 'REQ-MTO-0255', 'Consumo proyecto A' UNION ALL
    SELECT 'AJUSTE', 'T004', 'P3-B-01', NULL, 10, 'luis.ramirez@xyz.com', '2025-08-18 18:15:00', 'AJU-2025-007', 'Diferencia en conteo cíclico' UNION ALL
    SELECT 'ENTRADA', 'N002', NULL, 'P5-A-02', 20, 'carlos.mendez@xyz.com', '2025-08-20 09:10:00', 'OC-2025-0822', 'Recepción pintura' UNION ALL
    SELECT 'SALIDA', 'E005', 'P4-B-02', NULL, 30, 'jorge.hernandez@xyz.com', '2025-08-22 11:05:00', 'REQ-ELE-0130', 'Reemplazo luminarias nave 3' UNION ALL
    SELECT 'TRASLADO', 'G005', 'P1-B-02', 'P1-C-02', 80, 'jorge.hernandez@xyz.com', '2025-08-26 16:20:00', NULL, 'Segunda ubicación por alta demanda' UNION ALL
    SELECT 'SALIDA', 'I001', 'P1-D-01', NULL, 8, 'jorge.hernandez@xyz.com', '2025-08-27 09:15:00', 'REQ-INS-0180', 'Empaque y embalaje' UNION ALL
    SELECT 'ENTRADA', 'P003', NULL, 'P4-C-03', 80, 'carlos.mendez@xyz.com', '2025-08-29 10:00:00', 'OC-2025-0830', 'Recepción plomería' UNION ALL
    -- Septiembre 2025
    SELECT 'ENTRADA', 'N004', NULL, 'P5-B-01', 30, 'carlos.mendez@xyz.com', '2025-09-02 09:20:00', 'OC-2025-0902', 'Recepción pintura' UNION ALL
    SELECT 'SALIDA', 'N001', 'P5-A-01', NULL, 3, 'jorge.hernandez@xyz.com', '2025-09-04 08:30:00', 'REQ-PIN-0160', 'Trabajos de mantenimiento' UNION ALL
    SELECT 'SALIDA', 'HM02', 'P2-A-02', NULL, 4, 'maria.lopez@xyz.com', '2025-09-05 11:40:00', 'REQ-HER-0205', 'Herramienta cuadrilla 2' UNION ALL
    SELECT 'TRASLADO', 'N001', 'P5-A-01', 'P5-C-02', 5, 'jorge.hernandez@xyz.com', '2025-09-06 15:50:00', NULL, 'Segunda ubicación por volumen' UNION ALL
    SELECT 'ENTRADA', 'T009', NULL, 'P3-C-03', 500, 'carlos.mendez@xyz.com', '2025-09-08 09:00:00', 'OC-2025-0908', 'Recepción tornillería' UNION ALL
    SELECT 'SALIDA', 'T009', 'P3-C-03', NULL, 150, 'jorge.hernandez@xyz.com', '2025-09-10 10:20:00', 'REQ-MTO-0270', 'Consumo proyecto B' UNION ALL
    SELECT 'ENTRADA', 'E004', NULL, 'P4-B-01', 100, 'carlos.mendez@xyz.com', '2025-09-12 09:35:00', 'OC-2025-0912', 'Recepción material eléctrico' UNION ALL
    SELECT 'SALIDA', 'E003', 'P4-A-03', NULL, 20, 'maria.lopez@xyz.com', '2025-09-15 12:10:00', 'REQ-ELE-0140', 'Adecuación oficinas' UNION ALL
    SELECT 'AJUSTE', 'N001', 'P5-C-02', NULL, 1, 'luis.ramirez@xyz.com', '2025-09-16 18:30:00', 'AJU-2025-011', 'Ajuste por derrame' UNION ALL
    SELECT 'SALIDA', 'G001', 'P1-A-01', NULL, 30, 'jorge.hernandez@xyz.com', '2025-09-18 08:45:00', 'REQ-MTO-0280', 'Entrega EPP nuevo ingreso' UNION ALL
    SELECT 'ENTRADA', 'P004', NULL, 'P4-D-03', 24, 'carlos.mendez@xyz.com', '2025-09-19 09:15:00', 'OC-2025-0919', 'Recepción plomería' UNION ALL
    SELECT 'SALIDA', 'HE01', 'P2-C-01', NULL, 1, 'maria.lopez@xyz.com', '2025-09-22 15:00:00', 'REQ-HER-0215', 'Herramienta prestada' UNION ALL
    SELECT 'TRASLADO', 'N004', 'P5-B-01', 'P5-D-01', 25, 'jorge.hernandez@xyz.com', '2025-09-24 16:10:00', NULL, 'Desdoblamiento de inventario' UNION ALL
    SELECT 'ENTRADA', 'N005', NULL, 'P5-B-02', 40, 'carlos.mendez@xyz.com', '2025-09-25 09:05:00', 'OC-2025-0925', 'Recepción solventes' UNION ALL
    SELECT 'SALIDA', 'P002', 'P4-C-02', NULL, 40, 'jorge.hernandez@xyz.com', '2025-09-26 10:40:00', 'REQ-PLO-0155', 'Reparación de red hidráulica' UNION ALL
    SELECT 'SALIDA', 'I003', 'P1-D-03', NULL, 12, 'jorge.hernandez@xyz.com', '2025-09-27 09:50:00', 'REQ-INS-0200', 'Trabajos de pintura nave 4' UNION ALL
    SELECT 'ENTRADA', 'N007', NULL, 'P5-C-01', 25, 'carlos.mendez@xyz.com', '2025-09-29 09:30:00', 'OC-2025-0929', 'Recepción esmalte' UNION ALL
    SELECT 'SALIDA', 'E005', 'P4-B-02', NULL, 20, 'jorge.hernandez@xyz.com', '2025-09-30 11:00:00', 'REQ-ELE-0150', 'Reemplazo luminarias bodega'
) v
JOIN productos  p  ON p.codigo = v.codigo_producto
LEFT JOIN ubicaciones uo ON uo.codigo_ubicacion = v.codigo_origen
LEFT JOIN ubicaciones ud ON ud.codigo_ubicacion = v.codigo_destino
JOIN usuarios  us ON us.email = v.email_usuario;

-- ============================================================
-- 4. BÚSQUEDAS
-- ============================================================
INSERT INTO busquedas (usuario_id, producto_id, termino_busqueda,
                       fecha_hora_inicio, fecha_hora_fin,
                       tiempo_busqueda_segundos, ubicacion_encontrada_id, exito)
SELECT us.id, p.id, v.termino, v.inicio, v.fin, v.segundos, u.id, v.exito
FROM (
    -- Julio 2025 (fase 1, ~8 min promedio)
    SELECT 'carlos.mendez@xyz.com' AS email, 'T001' AS codigo_producto, 'Tornillos 1/4' AS termino, '2025-07-05 09:10:00' AS inicio, '2025-07-05 09:19:20' AS fin, 560 AS segundos, 'P3-A-01' AS codigo_ubicacion, TRUE AS exito UNION ALL
    SELECT 'maria.lopez@xyz.com', 'G001', 'Guantes', '2025-07-05 10:05:00', '2025-07-05 10:13:30', 510, 'P1-A-01', TRUE UNION ALL
    SELECT 'jorge.hernandez@xyz.com', 'HM02', 'Desarmador plano', '2025-07-06 08:40:00', '2025-07-06 08:48:05', 485, 'P2-A-02', TRUE UNION ALL
    SELECT 'carlos.mendez@xyz.com', 'E001', 'Cable 12', '2025-07-07 11:15:00', '2025-07-07 11:23:40', 520, 'P4-A-01', TRUE UNION ALL
    SELECT 'jorge.hernandez@xyz.com', 'N001', 'Pintura blanca', '2025-07-08 09:50:00', '2025-07-08 10:00:20', 620, 'P5-A-01', TRUE UNION ALL
    SELECT 'patricia.ruiz@xyz.com', 'I001', 'Cinta industrial', '2025-07-09 14:30:00', '2025-07-09 14:39:10', 550, 'P1-D-01', TRUE UNION ALL
    SELECT 'maria.lopez@xyz.com', 'HE01', 'Taladro', '2025-07-10 10:00:00', '2025-07-10 10:07:50', 470, 'P2-C-01', TRUE UNION ALL
    SELECT 'carlos.mendez@xyz.com', 'P002', 'Codo PVC', '2025-07-11 08:20:00', '2025-07-11 08:28:40', 520, 'P4-C-02', TRUE UNION ALL
    SELECT 'jorge.hernandez@xyz.com', 'G003', 'Casco', '2025-07-12 15:20:00', '2025-07-12 15:29:00', 540, 'P1-A-03', TRUE UNION ALL
    SELECT 'patricia.ruiz@xyz.com', 'N003', 'Brocha 4', '2025-07-14 09:05:00', '2025-07-14 09:13:00', 480, 'P5-A-03', TRUE UNION ALL
    SELECT 'carlos.mendez@xyz.com', 'T004', 'Tornillos 3/8', '2025-07-15 07:50:00', '2025-07-15 07:59:10', 550, 'P3-B-01', TRUE UNION ALL
    SELECT 'jorge.hernandez@xyz.com', 'E005', 'Foco LED', '2025-07-16 11:30:00', '2025-07-16 11:38:00', 480, 'P4-B-02', TRUE UNION ALL
    SELECT 'maria.lopez@xyz.com', 'G005', 'Mascarilla N95', '2025-07-17 10:15:00', '2025-07-17 10:23:10', 490, 'P1-B-02', TRUE UNION ALL
    SELECT 'carlos.mendez@xyz.com', 'I002', 'Cinta aislar', '2025-07-18 09:25:00', '2025-07-18 09:33:30', 510, 'P1-D-02', TRUE UNION ALL
    SELECT 'jorge.hernandez@xyz.com', 'HM01', 'Martillo', '2025-07-19 16:40:00', '2025-07-19 16:48:00', 480, 'P2-A-01', TRUE UNION ALL
    SELECT 'patricia.ruiz@xyz.com', 'N002', 'Pintura roja', '2025-07-21 08:55:00', '2025-07-21 09:03:30', 510, 'P5-A-02', TRUE UNION ALL
    SELECT 'carlos.mendez@xyz.com', 'E003', 'Contacto doble', '2025-07-22 14:10:00', '2025-07-22 14:18:20', 500, 'P4-A-03', TRUE UNION ALL
    SELECT 'jorge.hernandez@xyz.com', 'T009', 'Remaches', '2025-07-24 11:20:00', '2025-07-24 11:28:40', 520, 'P3-C-03', TRUE UNION ALL
    SELECT 'maria.lopez@xyz.com', 'HE02', 'Esmeriladora', '2025-07-25 09:30:00', '2025-07-25 09:38:00', 480, 'P2-C-02', TRUE UNION ALL
    SELECT 'patricia.ruiz@xyz.com', 'P005', 'Llave de paso', '2025-07-28 10:45:00', '2025-07-28 10:53:30', 510, 'P4-E-01', TRUE UNION ALL
    -- Agosto 2025 (fase 2, ~3.5 min promedio)
    SELECT 'carlos.mendez@xyz.com', 'T002', 'Tuercas 1/4', '2025-08-01 09:15:00', '2025-08-01 09:18:30', 210, 'P3-A-02', TRUE UNION ALL
    SELECT 'jorge.hernandez@xyz.com', 'G002', 'Lentes', '2025-08-02 10:20:00', '2025-08-02 10:23:50', 230, 'P1-A-02', TRUE UNION ALL
    SELECT 'maria.lopez@xyz.com', 'HM03', 'Desarmador Phillips', '2025-08-04 08:00:00', '2025-08-04 08:03:40', 220, 'P2-A-03', TRUE UNION ALL
    SELECT 'patricia.ruiz@xyz.com', 'E002', 'Cable 14', '2025-08-05 11:10:00', '2025-08-05 11:13:30', 210, 'P4-A-02', TRUE UNION ALL
    SELECT 'carlos.mendez@xyz.com', 'N007', 'Esmalte', '2025-08-06 15:20:00', '2025-08-06 15:23:40', 220, 'P5-C-01', TRUE UNION ALL
    SELECT 'jorge.hernandez@xyz.com', 'I004', 'Estopa', '2025-08-07 09:35:00', '2025-08-07 09:38:50', 230, 'P1-E-01', TRUE UNION ALL
    SELECT 'maria.lopez@xyz.com', 'HE03', 'Sierra circular', '2025-08-08 10:10:00', '2025-08-08 10:13:20', 200, 'P2-C-03', TRUE UNION ALL
    SELECT 'carlos.mendez@xyz.com', 'G006', 'Careta', '2025-08-11 08:25:00', '2025-08-11 08:28:40', 220, 'P1-B-03', TRUE UNION ALL
    SELECT 'patricia.ruiz@xyz.com', 'T006', 'Arandelas 3/8', '2025-08-12 14:15:00', '2025-08-12 14:18:20', 200, 'P3-B-03', TRUE UNION ALL
    SELECT 'jorge.hernandez@xyz.com', 'P001', 'Tubo PVC', '2025-08-13 09:50:00', '2025-08-13 09:53:30', 210, 'P4-C-01', TRUE UNION ALL
    SELECT 'maria.lopez@xyz.com', 'HM05', 'Llave 13', '2025-08-14 16:30:00', '2025-08-14 16:33:20', 200, 'P2-B-02', TRUE UNION ALL
    SELECT 'carlos.mendez@xyz.com', 'N005', 'Thinner', '2025-08-15 09:00:00', '2025-08-15 09:03:40', 220, 'P5-B-02', TRUE UNION ALL
    SELECT 'patricia.ruiz@xyz.com', 'HE05', 'Rotomartillo', '2025-08-18 10:25:00', '2025-08-18 10:29:00', 220, 'P2-D-02', TRUE UNION ALL
    SELECT 'jorge.hernandez@xyz.com', 'I005', 'Cinta métrica', '2025-08-19 11:15:00', '2025-08-19 11:18:40', 220, 'P1-E-02', TRUE UNION ALL
    SELECT 'maria.lopez@xyz.com', 'T010', 'Rondanas presión', '2025-08-20 08:20:00', '2025-08-20 08:23:30', 210, 'P3-D-01', TRUE UNION ALL
    SELECT 'carlos.mendez@xyz.com', 'E006', 'Caja eléctrica', '2025-08-21 15:40:00', '2025-08-21 15:43:50', 230, 'P4-B-03', TRUE UNION ALL
    SELECT 'jorge.hernandez@xyz.com', 'P004', 'Pegamento PVC', '2025-08-22 09:10:00', '2025-08-22 09:13:30', 210, 'P4-D-03', TRUE UNION ALL
    SELECT 'patricia.ruiz@xyz.com', 'HM04', 'Llave 10', '2025-08-25 10:05:00', '2025-08-25 10:08:20', 200, 'P2-B-01', TRUE UNION ALL
    SELECT 'carlos.mendez@xyz.com', 'T005', 'Tuercas 3/8', '2025-08-26 08:35:00', '2025-08-26 08:38:50', 230, 'P3-B-02', TRUE UNION ALL
    SELECT 'maria.lopez@xyz.com', 'N006', 'Anticorrosivo', '2025-08-27 14:50:00', '2025-08-27 14:53:40', 220, 'P5-B-03', TRUE UNION ALL
    SELECT 'jorge.hernandez@xyz.com', 'E004', 'Apagador', '2025-08-28 09:25:00', '2025-08-28 09:28:30', 210, 'P4-B-01', TRUE UNION ALL
    SELECT 'patricia.ruiz@xyz.com', 'HE04', 'Pistola de calor', '2025-08-29 11:40:00', '2025-08-29 11:44:10', 250, 'P2-D-01', TRUE UNION ALL
    -- Septiembre 2025 (fase 3, ~1.4 min promedio)
    SELECT 'carlos.mendez@xyz.com', 'T001', 'Tornillos 1/4', '2025-09-01 09:05:00', '2025-09-01 09:06:25', 85, 'P3-A-01', TRUE UNION ALL
    SELECT 'jorge.hernandez@xyz.com', 'G001', 'Guantes', '2025-09-01 10:10:00', '2025-09-01 10:11:20', 80, 'P1-A-01', TRUE UNION ALL
    SELECT 'maria.lopez@xyz.com', 'I001', 'Cinta industrial', '2025-09-02 08:30:00', '2025-09-02 08:31:25', 85, 'P1-D-01', TRUE UNION ALL
    SELECT 'patricia.ruiz@xyz.com', 'N001', 'Pintura blanca', '2025-09-03 11:15:00', '2025-09-03 11:16:35', 95, 'P5-A-01', TRUE UNION ALL
    SELECT 'carlos.mendez@xyz.com', 'HE01', 'Taladro', '2025-09-04 09:45:00', '2025-09-04 09:46:30', 90, 'P2-C-01', TRUE UNION ALL
    SELECT 'jorge.hernandez@xyz.com', 'G005', 'Mascarilla N95', '2025-09-05 10:20:00', '2025-09-05 10:21:15', 75, 'P1-B-02', TRUE UNION ALL
    SELECT 'maria.lopez@xyz.com', 'E005', 'Foco LED', '2025-09-08 08:10:00', '2025-09-08 08:11:10', 70, 'P4-B-02', TRUE UNION ALL
    SELECT 'carlos.mendez@xyz.com', 'E001', 'Cable 12', '2025-09-09 15:25:00', '2025-09-09 15:26:35', 95, 'P4-A-01', TRUE UNION ALL
    SELECT 'patricia.ruiz@xyz.com', 'P002', 'Codo PVC', '2025-09-10 09:00:00', '2025-09-10 09:01:20', 80, 'P4-C-02', TRUE UNION ALL
    SELECT 'jorge.hernandez@xyz.com', 'N004', 'Rodillo 9', '2025-09-11 10:40:00', '2025-09-11 10:41:35', 95, 'P5-B-01', TRUE UNION ALL
    SELECT 'carlos.mendez@xyz.com', 'T009', 'Remaches', '2025-09-12 08:45:00', '2025-09-12 08:46:35', 95, 'P3-C-03', TRUE UNION ALL
    SELECT 'maria.lopez@xyz.com', 'HM02', 'Desarmador plano', '2025-09-15 09:20:00', '2025-09-15 09:21:10', 70, 'P2-A-02', TRUE UNION ALL
    SELECT 'patricia.ruiz@xyz.com', 'N002', 'Pintura roja', '2025-09-16 11:50:00', '2025-09-16 11:52:00', 85, 'P5-A-02', TRUE UNION ALL
    SELECT 'jorge.hernandez@xyz.com', 'I002', 'Cinta aislar', '2025-09-17 10:30:00', '2025-09-17 10:31:20', 80, 'P1-D-02', TRUE UNION ALL
    SELECT 'carlos.mendez@xyz.com', 'G003', 'Casco', '2025-09-18 08:25:00', '2025-09-18 08:26:15', 75, 'P1-A-03', TRUE UNION ALL
    SELECT 'maria.lopez@xyz.com', 'HM01', 'Martillo', '2025-09-19 09:55:00', '2025-09-19 09:57:00', 85, 'P2-A-01', TRUE UNION ALL
    SELECT 'patricia.ruiz@xyz.com', 'E003', 'Contacto doble', '2025-09-22 14:10:00', '2025-09-22 14:11:25', 85, 'P4-A-03', TRUE UNION ALL
    SELECT 'jorge.hernandez@xyz.com', 'P003', 'Tee PVC', '2025-09-23 10:00:00', '2025-09-23 10:01:10', 70, 'P4-C-03', TRUE UNION ALL
    SELECT 'carlos.mendez@xyz.com', 'N003', 'Brocha 4', '2025-09-24 11:30:00', '2025-09-24 11:31:30', 90, 'P5-A-03', TRUE UNION ALL
    SELECT 'maria.lopez@xyz.com', 'G002', 'Lentes', '2025-09-25 08:15:00', '2025-09-25 08:16:10', 70, 'P1-A-02', TRUE UNION ALL
    SELECT 'patricia.ruiz@xyz.com', 'HE02', 'Esmeriladora', '2025-09-26 09:40:00', '2025-09-26 09:41:40', 100, 'P2-C-02', TRUE UNION ALL
    SELECT 'jorge.hernandez@xyz.com', 'P004', 'Pegamento PVC', '2025-09-29 10:05:00', '2025-09-29 10:06:20', 80, 'P4-D-03', TRUE UNION ALL
    SELECT 'carlos.mendez@xyz.com', 'N007', 'Esmalte', '2025-09-30 09:15:00', '2025-09-30 09:16:15', 75, 'P5-C-01', TRUE UNION ALL
    SELECT 'maria.lopez@xyz.com', 'HE04', 'Pistola de calor', '2025-09-30 15:50:00', '2025-09-30 15:52:00', 85, 'P2-D-01', TRUE
) v
JOIN usuarios  us ON us.email = v.email
JOIN productos p  ON p.codigo = v.codigo_producto
JOIN ubicaciones u ON u.codigo_ubicacion = v.codigo_ubicacion;

-- ============================================================
-- 5. INCIDENCIAS
-- ============================================================
INSERT INTO incidencias (tipo, producto_id, ubicacion_id, usuario_id,
                         fecha, descripcion, resuelta, fecha_resolucion)
SELECT v.tipo, p.id, u.id, us.id, v.fecha, v.descripcion, v.resuelta, v.fecha_resolucion
FROM (
    SELECT 'MAL_UBICADO' AS tipo, 'G001' AS codigo_producto, 'P1-D-03' AS codigo_ubicacion, 'jorge.hernandez@xyz.com' AS email_usuario, '2025-07-12 10:20:00' AS fecha, 'Guantes encontrados en pasillo de insumos en lugar de EPP' AS descripcion, TRUE AS resuelta, '2025-07-12 11:00:00' AS fecha_resolucion UNION ALL
    SELECT 'FALTANTE', 'T003', 'P3-A-03', 'maria.lopez@xyz.com', '2025-07-20 17:50:00', 'Diferencia de 15 piezas en conteo cíclico', TRUE, '2025-07-21 09:30:00' UNION ALL
    SELECT 'MAL_UBICADO', 'T009', 'P3-C-03', 'jorge.hernandez@xyz.com', '2025-07-25 15:40:00', 'Remaches hallados en ubicación incorrecta', TRUE, '2025-07-25 16:20:00' UNION ALL
    SELECT 'DANADO', 'HE01', 'P2-C-01', 'jorge.hernandez@xyz.com', '2025-08-02 11:15:00', 'Taladro con cable dañado, requiere revisión', TRUE, '2025-08-05 09:00:00' UNION ALL
    SELECT 'MAL_UBICADO', 'E001', 'P4-A-01', 'jorge.hernandez@xyz.com', '2025-08-13 16:30:00', 'Cable calibre 14 colocado en ubicación de calibre 12', TRUE, '2025-08-13 17:15:00' UNION ALL
    SELECT 'FALTANTE', 'N002', 'P5-A-02', 'maria.lopez@xyz.com', '2025-08-22 18:10:00', 'Faltan 2 cubetas de pintura roja vs. sistema', TRUE, '2025-08-25 10:00:00' UNION ALL
    SELECT 'DANADO', 'N003', 'P5-A-03', 'patricia.ruiz@xyz.com', '2025-08-27 09:40:00', 'Brochas con cerdas desprendidas, no aptas para uso', TRUE, '2025-08-28 08:50:00' UNION ALL
    SELECT 'MAL_UBICADO', 'G005', 'P1-B-02', 'jorge.hernandez@xyz.com', '2025-09-03 10:25:00', 'Mascarillas N95 en ubicación de tapones auditivos', TRUE, '2025-09-03 11:00:00' UNION ALL
    SELECT 'FALTANTE', 'N001', 'P5-A-01', 'maria.lopez@xyz.com', '2025-09-06 17:30:00', 'Pintura blanca con faltante de 1 cubeta', TRUE, '2025-09-08 08:45:00' UNION ALL
    SELECT 'DANADO', 'N005', 'P5-B-02', 'patricia.ruiz@xyz.com', '2025-09-15 14:20:00', 'Botella de thinner con fuga, se desecha', TRUE, '2025-09-15 15:10:00' UNION ALL
    SELECT 'MAL_UBICADO', 'N004', 'P5-B-01', 'jorge.hernandez@xyz.com', '2025-09-22 11:35:00', 'Rodillos en pasillo 4 en lugar de pasillo 5', TRUE, '2025-09-22 12:05:00' UNION ALL
    SELECT 'OTRO', 'T005', 'P3-B-02', 'maria.lopez@xyz.com', '2025-09-28 16:50:00', 'Estante B nivel 2 requiere refuerzo estructural', FALSE, NULL
) v
JOIN productos  p  ON p.codigo = v.codigo_producto
JOIN ubicaciones u ON u.codigo_ubicacion = v.codigo_ubicacion
JOIN usuarios  us ON us.email = v.email_usuario;

-- ============================================================
-- 6. VERIFICACIÓN
-- ============================================================
SELECT 'inventario' AS tabla, COUNT(*) AS filas FROM inventario
UNION ALL SELECT 'movimientos', COUNT(*) FROM movimientos
UNION ALL SELECT 'busquedas',   COUNT(*) FROM busquedas
UNION ALL SELECT 'incidencias', COUNT(*) FROM incidencias;