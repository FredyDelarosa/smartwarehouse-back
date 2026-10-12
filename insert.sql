USE smart_warehouse;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE incidencias;
TRUNCATE TABLE busquedas;
TRUNCATE TABLE movimientos;
TRUNCATE TABLE inventario;
TRUNCATE TABLE ubicaciones;
TRUNCATE TABLE productos;
TRUNCATE TABLE categorias;
TRUNCATE TABLE almacenes;
TRUNCATE TABLE usuarios;
TRUNCATE TABLE roles;
SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================
-- 1. ROLES
-- ============================================================
INSERT INTO roles (id, nombre, descripcion) VALUES
(1, 'Administrador', 'Acceso total: usuarios, configuración y catálogos'),
(2, 'Supervisor',    'Consulta métricas, aprueba ajustes y revisa incidencias'),
(3, 'Almacenero',    'Realiza búsquedas, movimientos y escaneo de QR');

-- ============================================================
-- 2. USUARIOS
-- ============================================================
INSERT INTO usuarios (id, nombre, email, password_hash, rol_id, activo, ultimo_acceso) VALUES
(1, 'Ana Torres',       'ana.torres@xyz.com',       '$2b$12$PLACEHOLDERHASH00000000000000000000000000000000000000', 1, TRUE, '2025-09-30 08:12:00'),
(2, 'Luis Ramírez',     'luis.ramirez@xyz.com',     '$2b$12$PLACEHOLDERHASH00000000000000000000000000000000000000', 2, TRUE, '2025-09-30 07:55:00'),
(3, 'Carlos Méndez',    'carlos.mendez@xyz.com',    '$2b$12$PLACEHOLDERHASH00000000000000000000000000000000000000', 3, TRUE, '2025-09-30 06:50:00'),
(4, 'María López',      'maria.lopez@xyz.com',      '$2b$12$PLACEHOLDERHASH00000000000000000000000000000000000000', 3, TRUE, '2025-09-30 07:20:00'),
(5, 'Jorge Hernández',  'jorge.hernandez@xyz.com',  '$2b$12$PLACEHOLDERHASH00000000000000000000000000000000000000', 3, TRUE, '2025-09-30 08:05:00'),
(6, 'Patricia Ruiz',    'patricia.ruiz@xyz.com',    '$2b$12$PLACEHOLDERHASH00000000000000000000000000000000000000', 3, TRUE, '2025-09-29 17:40:00');

-- ============================================================
-- 3. ALMACENES
-- ============================================================
INSERT INTO almacenes (id, nombre, direccion, activo) VALUES
(1, 'Almacén Industrial XYZ', 'Av. de los Procesos 1450, Parque Industrial Norte', TRUE);

-- ============================================================
-- 4. CATEGORÍAS
-- ============================================================
INSERT INTO categorias (id, nombre, descripcion) VALUES
(1, 'Tornillería',             'Tornillos, tuercas, arandelas y remaches'),
(2, 'Herramientas manuales',   'Herramienta de mano de uso común'),
(3, 'Herramientas eléctricas', 'Herramienta motorizada y eléctrica'),
(4, 'EPP',                     'Equipo de protección personal'),
(5, 'Insumos generales',       'Cintas, estopa y consumibles varios'),
(6, 'Eléctrico',               'Cable, contactos y material eléctrico'),
(7, 'Plomería',                'Tubería, conexiones y accesorios'),
(8, 'Pintura',                 'Pinturas, brochas, rodillos y solventes');

-- ============================================================
-- 5. PRODUCTOS (50)
-- ============================================================
INSERT INTO productos (id, codigo, nombre, descripcion, categoria_id, unidad_medida, stock_minimo, foto_url) VALUES
(1,  'T001', 'Tornillos 1/4"',                'Tornillo hexagonal cabeza, acero inoxidable 1/4"',        1, 'pieza', 100, '/assets/products/T001.jpg'),
(2,  'T002', 'Tuercas 1/4"',                  'Tuerca hexagonal estándar 1/4"',                          1, 'pieza', 100, '/assets/products/T002.jpg'),
(3,  'T003', 'Arandelas planas 1/4"',         'Arandela plana de acero 1/4"',                            1, 'pieza', 200, '/assets/products/T003.jpg'),
(4,  'T004', 'Tornillos 3/8"',                'Tornillo hexagonal 3/8" grado 5',                         1, 'pieza', 100, '/assets/products/T004.jpg'),
(5,  'T005', 'Tuercas 3/8"',                  'Tuerca hexagonal 3/8"',                                   1, 'pieza', 100, '/assets/products/T005.jpg'),
(6,  'T006', 'Arandelas planas 3/8"',         'Arandela plana 3/8"',                                     1, 'pieza', 200, '/assets/products/T006.jpg'),
(7,  'T007', 'Tornillos 5/16"',               'Tornillo hexagonal 5/16"',                                1, 'pieza', 100, '/assets/products/T007.jpg'),
(8,  'T008', 'Tuercas 5/16"',                 'Tuerca hexagonal 5/16"',                                  1, 'pieza', 100, '/assets/products/T008.jpg'),
(9,  'T009', 'Remaches 1/8"',                 'Remache pop aluminio 1/8"',                               1, 'pieza', 200, '/assets/products/T009.jpg'),
(10, 'T010', 'Rondanas de presión 1/4"',      'Rondana de presión (grower) 1/4"',                        1, 'pieza', 150, '/assets/products/T010.jpg'),
(11, 'HM01', 'Martillo de bola 16 oz',        'Mango de fibra, cabeza forjada',                          2, 'pieza', 5,   '/assets/products/HM01.jpg'),
(12, 'HM02', 'Desarmador plano 6"',           'Punta plana 6"',                                          2, 'pieza', 8,   '/assets/products/HM02.jpg'),
(13, 'HM03', 'Desarmador Phillips #2',        'Punta Phillips #2 mango ergonómico',                      2, 'pieza', 8,   '/assets/products/HM03.jpg'),
(14, 'HM04', 'Llave mixta 10 mm',             'Llave mixta (abierta/estrella) 10 mm',                    2, 'pieza', 10,  '/assets/products/HM04.jpg'),
(15, 'HM05', 'Llave mixta 13 mm',             'Llave mixta 13 mm',                                       2, 'pieza', 10,  '/assets/products/HM05.jpg'),
(16, 'HM06', 'Pinza de corte 8"',             'Pinza de corte diagonal 8"',                              2, 'pieza', 6,   '/assets/products/HM06.jpg'),
(17, 'HE01', 'Taladro percutor 1/2"',         'Taladro percutor 850W, 1/2"',                             3, 'pieza', 3,   '/assets/products/HE01.jpg'),
(18, 'HE02', 'Esmeriladora angular 4.5"',     'Esmeriladora 900W disco 4.5"',                            3, 'pieza', 3,   '/assets/products/HE02.jpg'),
(19, 'HE03', 'Sierra circular 7-1/4"',        'Sierra circular 1400W, disco 7-1/4"',                     3, 'pieza', 2,   '/assets/products/HE03.jpg'),
(20, 'HE04', 'Pistola de calor 1500W',        'Pistola de calor con dos niveles de temperatura',         3, 'pieza', 2,   '/assets/products/HE04.jpg'),
(21, 'HE05', 'Rotomartillo SDS Plus',         'Rotomartillo SDS-Plus 800W',                              3, 'pieza', 2,   '/assets/products/HE05.jpg'),
(22, 'G001', 'Guantes de seguridad',          'Guante de carnaza reforzado',                             4, 'par',   60,  '/assets/products/G001.jpg'),
(23, 'G002', 'Lentes de protección',          'Lente de policarbonato claro antiempañante',              4, 'pieza', 50,  '/assets/products/G002.jpg'),
(24, 'G003', 'Casco de seguridad',            'Casco ANSI clase A, ajuste ratchet',                      4, 'pieza', 30,  '/assets/products/G003.jpg'),
(25, 'G004', 'Tapones auditivos',             'Tapón auditivo desechable NRR 32',                        4, 'par',   100, '/assets/products/G004.jpg'),
(26, 'G005', 'Mascarilla N95',                'Respirador N95, ajuste facial',                           4, 'pieza', 80,  '/assets/products/G005.jpg'),
(27, 'G006', 'Careta facial transparente',    'Careta de policarbonato con banda ajustable',             4, 'pieza', 20,  '/assets/products/G006.jpg'),
(28, 'I001', 'Cinta industrial',              'Cinta adhesiva industrial 48 mm x 50 m',                  5, 'rollo', 20,  '/assets/products/I001.jpg'),
(29, 'I002', 'Cinta de aislar',               'Cinta aislante eléctrica 3/4" x 20 m',                    5, 'rollo', 30,  '/assets/products/I002.jpg'),
(30, 'I003', 'Cinta de enmascarar',           'Cinta de papel enmascarar 1" x 50 m',                     5, 'rollo', 25,  '/assets/products/I003.jpg'),
(31, 'I004', 'Estopa para limpieza',          'Estopa blanca de algodón (kg)',                           5, 'kg',    15,  '/assets/products/I004.jpg'),
(32, 'I005', 'Cinta métrica 5 m',             'Flexómetro 5 m con seguro',                               5, 'pieza', 10,  '/assets/products/I005.jpg'),
(33, 'E001', 'Cable calibre 12 (rollo 100m)', 'Cable THW calibre 12, rollo 100 m',                       6, 'rollo', 8,   '/assets/products/E001.jpg'),
(34, 'E002', 'Cable calibre 14 (rollo 100m)', 'Cable THW calibre 14, rollo 100 m',                       6, 'rollo', 8,   '/assets/products/E002.jpg'),
(35, 'E003', 'Contacto doble',                'Contacto dúplex polarizado 15A',                          6, 'pieza', 30,  '/assets/products/E003.jpg'),
(36, 'E004', 'Apagador sencillo',             'Apagador de 1 polo 15A',                                  6, 'pieza', 30,  '/assets/products/E004.jpg'),
(37, 'E005', 'Foco LED 9W',                   'Foco LED luz blanca 9W E27',                              6, 'pieza', 50,  '/assets/products/E005.jpg'),
(38, 'E006', 'Caja eléctrica cuadrada',       'Caja eléctrica cuadrada metálica 1/2"',                   6, 'pieza', 40,  '/assets/products/E006.jpg'),
(39, 'P001', 'Tubo PVC 1/2" x 3 m',           'Tubo PVC hidráulico 1/2" x 3 m',                          7, 'pieza', 20,  '/assets/products/P001.jpg'),
(40, 'P002', 'Codo PVC 1/2"',                 'Codo PVC 90° hidráulico 1/2"',                            7, 'pieza', 60,  '/assets/products/P002.jpg'),
(41, 'P003', 'Tee PVC 1/2"',                  'Tee PVC hidráulica 1/2"',                                 7, 'pieza', 50,  '/assets/products/P003.jpg'),
(42, 'P004', 'Pegamento PVC 250 ml',          'Adhesivo para PVC 250 ml',                                7, 'bote',  12,  '/assets/products/P004.jpg'),
(43, 'P005', 'Llave de paso 1/2"',            'Llave de paso esfera 1/2"',                               7, 'pieza', 15,  '/assets/products/P005.jpg'),
(44, 'N001', 'Pintura blanca 19 L',           'Pintura vinílica blanca, cubeta 19 L',                    8, 'cubeta',5,   '/assets/products/N001.jpg'),
(45, 'N002', 'Pintura roja 4 L',              'Pintura esmalte rojo, cubeta 4 L',                        8, 'cubeta',8,   '/assets/products/N002.jpg'),
(46, 'N003', 'Brocha 4"',                     'Brocha de cerdas naturales 4"',                           8, 'pieza', 20,  '/assets/products/N003.jpg'),
(47, 'N004', 'Rodillo 9"',                    'Rodillo felpa 9" con marco',                              8, 'pieza', 20,  '/assets/products/N004.jpg'),
(48, 'N005', 'Thinner 1 L',                   'Thinner estándar, botella 1 L',                           8, 'bote',  15,  '/assets/products/N005.jpg'),
(49, 'N006', 'Pintura anticorrosiva 4 L',     'Anticorrosivo gris, cubeta 4 L',                          8, 'cubeta',6,   '/assets/products/N006.jpg'),
(50, 'N007', 'Esmalte sintético 1 L',         'Esmalte sintético brillante, 1 L',                        8, 'bote',  12,  '/assets/products/N007.jpg');

-- ============================================================
-- 6. UBICACIONES (5 pasillos × 10 estantes × 3 niveles = 150)
--    Formato de código: P{pasillo}-{estante}-{nivel:02}
--    coordenada_x = pasillo * 10 ; coordenada_y = (estante+1) * 5
-- ============================================================
INSERT INTO ubicaciones (almacen_id, pasillo, estante, nivel, codigo_ubicacion, codigo_qr, coordenada_x, coordenada_y)
WITH RECURSIVE
  p AS (SELECT 1 AS i UNION ALL SELECT i + 1 FROM p WHERE i < 5),
  e AS (SELECT 0 AS i UNION ALL SELECT i + 1 FROM e WHERE i < 9),
  n AS (SELECT 1 AS i UNION ALL SELECT i + 1 FROM n WHERE i < 3)
SELECT
  1,
  CONCAT('P', p.i),
  CHAR(65 + e.i),
  CAST(n.i AS CHAR),
  CONCAT('P', p.i, '-', CHAR(65 + e.i), '-', LPAD(n.i, 2, '0')),
  CONCAT('QR-P', p.i, '-', CHAR(65 + e.i), '-', LPAD(n.i, 2, '0')),
  p.i * 10,
  (e.i + 1) * 5
FROM p CROSS JOIN e CROSS JOIN n;

-- Verificación rápida: SELECT COUNT(*) FROM ubicaciones;  -- debe ser 150

SELECT COUNT(*) FROM ubicaciones;

-- ============================================================
-- 7. INVENTARIO (productos en su ubicación principal + secundarias)
-- ============================================================
INSERT INTO inventario (producto_id, ubicacion_id, cantidad) VALUES
-- Tornillería (Pasillo 3, estantes A-D)
(1,  61, 350), (2,  62, 520), (3,  63, 800), (4,  64, 280), (5,  65, 410),
(6,  66, 620), (7,  67, 190), (8,  68, 230), (9,  69, 950), (10, 70, 480),
-- Ubicaciones secundarias de alta rotación (tornillería)
(1,  71, 120), (3,  72, 200), (9,  73, 300),
-- Herramientas manuales (Pasillo 2, estantes A-B)
(11, 31, 18), (12, 32, 25), (13, 33, 22), (14, 34, 30), (15, 35, 28), (16, 36, 14),
-- Herramientas eléctricas (Pasillo 2, estantes C-D)
(17, 37, 7), (18, 38, 6), (19, 39, 4), (20, 40, 5), (21, 41, 3),
-- EPP (Pasillo 1, estantes A-C)
(22,  1, 180), (23,  2, 120), (24,  3,  65), (25,  4, 250), (26,  5, 210), (27,  6,  35),
(22,  7,  60), (26,  8,  80),
-- Insumos (Pasillo 1, estantes D-E)
(28, 10, 45), (29, 11, 75), (30, 12, 60), (31, 13, 40), (32, 14, 22),
(28, 15, 20),
-- Eléctrico (Pasillo 4, estantes A-B)
(33, 91, 14), (34, 92, 16), (35, 93, 90), (36, 94, 85), (37, 95, 140), (38, 96, 110),
(33, 102, 6), (37, 103, 60),
-- Plomería (Pasillo 4, estantes C-E)
(39, 97, 55), (40, 98, 180), (41, 99, 140), (42, 100, 32), (43, 101, 40),
(40, 104, 80),
-- Pintura (Pasillo 5, estantes A-D)
(44, 121, 12), (45, 122, 18), (46, 123, 55), (47, 124, 48), (48, 125, 35),
(49, 126, 10), (50, 127, 22),
(44, 128, 5), (45, 129, 6), (47, 130, 25);

-- ============================================================
-- 8. MOVIMIENTOS (Jul-Sep 2025: entradas, salidas, traslados, ajustes)
-- ============================================================
INSERT INTO movimientos (tipo, producto_id, ubicacion_origen_id, ubicacion_destino_id, cantidad, usuario_id, fecha, referencia, observaciones) VALUES
-- Julio 2025
('ENTRADA',  1,  NULL, 61, 400, 3, '2025-07-03 09:15:00', 'OC-2025-0712', 'Recepción proveedor Aceros del Norte'),
('ENTRADA',  2,  NULL, 62, 500, 3, '2025-07-03 09:40:00', 'OC-2025-0712', 'Recepción proveedor Aceros del Norte'),
('ENTRADA', 22,  NULL,  1, 200, 4, '2025-07-04 10:10:00', 'OC-2025-0715', 'Ingreso EPP seguridad'),
('SALIDA',   1,  61, NULL, 50, 5, '2025-07-08 11:20:00', 'REQ-MTO-0221', 'Consumo área mantenimiento'),
('SALIDA',  22,   1, NULL, 20, 5, '2025-07-08 11:25:00', 'REQ-MTO-0221', 'Entrega EPP a cuadrilla 3'),
('ENTRADA', 33,  NULL, 91, 15, 3, '2025-07-10 08:55:00', 'OC-2025-0721', 'Recepción material eléctrico'),
('SALIDA',  33,  91, NULL,  2, 4, '2025-07-15 16:00:00', 'REQ-ELE-0110', 'Instalación nave 2'),
('TRASLADO', 9,  69, 73,  200, 5, '2025-07-18 15:10:00', NULL,           'Reubicación por falta de espacio'),
('AJUSTE',   3,  63, NULL, -15, 2, '2025-07-20 18:00:00', 'AJU-2025-003', 'Ajuste por conteo físico'),
('ENTRADA', 39,  NULL, 97,  60, 3, '2025-07-22 09:00:00', 'OC-2025-0728', 'Recepción plomería'),
('SALIDA',  40,  98, NULL,  30, 5, '2025-07-24 10:30:00', 'REQ-PLO-0140', 'Mantenimiento hidráulico'),
('ENTRADA', 44,  NULL, 121, 15, 3, '2025-07-28 09:20:00', 'OC-2025-0731', 'Recepción pintura'),
('SALIDA',  46, 123, NULL,  10, 5, '2025-07-29 11:45:00', 'REQ-PIN-0155', 'Trabajos nave 1'),

-- Agosto 2025
('ENTRADA',  4,  NULL, 64, 300, 3, '2025-08-01 09:05:00', 'OC-2025-0801', 'Recepción tornillería'),
('ENTRADA', 26,  NULL,  5, 250, 4, '2025-08-02 10:15:00', 'OC-2025-0803', 'Ingreso EPP respiratoria'),
('SALIDA',  26,   5, NULL, 40, 5, '2025-08-05 07:50:00', 'REQ-MTO-0240', 'Entrega a cuadrilla de soldadura'),
('SALIDA',  23,   2, NULL, 15, 5, '2025-08-06 08:20:00', 'REQ-MTO-0241', 'Entrega lentes a nuevo personal'),
('TRASLADO', 22,   1,  7,   60, 5, '2025-08-08 15:30:00', NULL,           'Desdoblamiento de inventario'),
('ENTRADA', 33,  NULL, 91,  10, 3, '2025-08-11 09:35:00', 'OC-2025-0812', 'Recepción cable'),
('SALIDA',  33,  91, NULL,   3, 4, '2025-08-13 14:00:00', 'REQ-ELE-0125', 'Trabajos en subestación'),
('SALIDA',   1,  61, NULL,  80, 5, '2025-08-14 10:10:00', 'REQ-MTO-0255', 'Consumo proyecto A'),
('AJUSTE',   4,  64, NULL, -10, 2, '2025-08-18 18:15:00', 'AJU-2025-007', 'Diferencia en conteo cíclico'),
('ENTRADA', 45,  NULL, 122, 20, 3, '2025-08-20 09:10:00', 'OC-2025-0822', 'Recepción pintura'),
('SALIDA',  37,  95, NULL,  30, 5, '2025-08-22 11:05:00', 'REQ-ELE-0130', 'Reemplazo luminarias nave 3'),
('TRASLADO', 26,   5,  8,   80, 5, '2025-08-26 16:20:00', NULL,           'Segunda ubicación por alta demanda'),
('SALIDA',  28,  10, NULL,   8, 5, '2025-08-27 09:15:00', 'REQ-INS-0180', 'Empaque y embalaje'),
('ENTRADA', 41,  NULL, 99,  80, 3, '2025-08-29 10:00:00', 'OC-2025-0830', 'Recepción plomería'),

-- Septiembre 2025
('ENTRADA', 47,  NULL, 124, 30, 3, '2025-09-02 09:20:00', 'OC-2025-0902', 'Recepción pintura'),
('SALIDA',  44, 121, NULL,   3, 5, '2025-09-04 08:30:00', 'REQ-PIN-0160', 'Trabajos de mantenimiento'),
('SALIDA',  12,  32, NULL,   4, 4, '2025-09-05 11:40:00', 'REQ-HER-0205', 'Herramienta cuadrilla 2'),
('TRASLADO', 44, 121, 128,   5, 5, '2025-09-06 15:50:00', NULL,           'Segunda ubicación por volumen'),
('ENTRADA',  9,  NULL,  69, 500, 3, '2025-09-08 09:00:00', 'OC-2025-0908', 'Recepción tornillería'),
('SALIDA',   9,   69, NULL, 150, 5, '2025-09-10 10:20:00', 'REQ-MTO-0270', 'Consumo proyecto B'),
('ENTRADA', 36,  NULL,  94, 100, 3, '2025-09-12 09:35:00', 'OC-2025-0912', 'Recepción material eléctrico'),
('SALIDA',  35,  93, NULL,  20, 4, '2025-09-15 12:10:00', 'REQ-ELE-0140', 'Adecuación oficinas'),
('AJUSTE',  44, 128, NULL,  -1, 2, '2025-09-16 18:30:00', 'AJU-2025-011', 'Ajuste por derrame'),
('SALIDA',  22,   1, NULL,  30, 5, '2025-09-18 08:45:00', 'REQ-MTO-0280', 'Entrega EPP nuevo ingreso'),
('ENTRADA', 42,  NULL, 100, 24, 3, '2025-09-19 09:15:00', 'OC-2025-0919', 'Recepción plomería'),
('SALIDA',  17,  37, NULL,   1, 4, '2025-09-22 15:00:00', 'REQ-HER-0215', 'Herramienta prestada'),
('TRASLADO', 47, 124, 130,  25, 5, '2025-09-24 16:10:00', NULL,           'Desdoblamiento de inventario'),
('ENTRADA', 48,  NULL, 125, 40, 3, '2025-09-25 09:05:00', 'OC-2025-0925', 'Recepción solventes'),
('SALIDA',  40,  98, NULL,  40, 5, '2025-09-26 10:40:00', 'REQ-PLO-0155', 'Reparación de red hidráulica'),
('SALIDA',  30,  12, NULL,  12, 5, '2025-09-27 09:50:00', 'REQ-INS-0200', 'Trabajos de pintura nave 4'),
('ENTRADA', 50,  NULL, 127, 25, 3, '2025-09-29 09:30:00', 'OC-2025-0929', 'Recepción esmalte'),
('SALIDA',  37,  95, NULL,  20, 5, '2025-09-30 11:00:00', 'REQ-ELE-0150', 'Reemplazo luminarias bodega');

-- ============================================================
-- 9. BÚSQUEDAS (métricas con mejora progresiva)
--    Fase 1 (Jul): ~450 s (implantación, usuarios aprendiendo)
--    Fase 2 (Ago): ~200 s (adaptación)
--    Fase 3 (Sep): ~80 s  (uso maduro de la app)
-- ============================================================
INSERT INTO busquedas (usuario_id, producto_id, termino_busqueda, fecha_hora_inicio, fecha_hora_fin, tiempo_busqueda_segundos, ubicacion_encontrada_id, exito) VALUES
-- Fase 1 - Julio
(3,  1, 'Tornillos 1/4',       '2025-07-05 09:10:00', '2025-07-05 09:19:20', 560, 61, TRUE),
(4, 22, 'Guantes',             '2025-07-05 10:05:00', '2025-07-05 10:13:30', 510,  1, TRUE),
(5, 12, 'Desarmador plano',    '2025-07-06 08:40:00', '2025-07-06 08:48:05', 485, 32, TRUE),
(3, 33, 'Cable 12',            '2025-07-07 11:15:00', '2025-07-07 11:23:40', 520, 91, TRUE),
(5, 44, 'Pintura blanca',      '2025-07-08 09:50:00', '2025-07-08 10:00:20', 620,121, TRUE),
(6, 28, 'Cinta industrial',    '2025-07-09 14:30:00', '2025-07-09 14:39:10', 550, 10, TRUE),
(4, 17, 'Taladro',             '2025-07-10 10:00:00', '2025-07-10 10:07:50', 470, 37, TRUE),
(3, 40, 'Codo PVC',            '2025-07-11 08:20:00', '2025-07-11 08:28:40', 520, 98, TRUE),
(5, 24, 'Casco',               '2025-07-12 15:20:00', '2025-07-12 15:29:00', 540,  3, TRUE),
(6, 46, 'Brocha 4',            '2025-07-14 09:05:00', '2025-07-14 09:13:00', 480,123, TRUE),
(3,  4, 'Tornillos 3/8',       '2025-07-15 07:50:00', '2025-07-15 07:59:10', 550, 64, TRUE),
(5, 37, 'Foco LED',            '2025-07-16 11:30:00', '2025-07-16 11:38:00', 480, 95, TRUE),
(4, 26, 'Mascarilla N95',      '2025-07-17 10:15:00', '2025-07-17 10:23:10', 490,  5, TRUE),
(3, 29, 'Cinta aislar',        '2025-07-18 09:25:00', '2025-07-18 09:33:30', 510, 11, TRUE),
(5, 11, 'Martillo',            '2025-07-19 16:40:00', '2025-07-19 16:48:00', 480, 31, TRUE),
(6, 45, 'Pintura roja',        '2025-07-21 08:55:00', '2025-07-21 09:03:30', 510,122, TRUE),
(3, 35, 'Contacto doble',      '2025-07-22 14:10:00', '2025-07-22 14:18:20', 500, 93, TRUE),
(5,  9, 'Remaches',            '2025-07-24 11:20:00', '2025-07-24 11:28:40', 520, 69, TRUE),
(4, 18, 'Esmeriladora',        '2025-07-25 09:30:00', '2025-07-25 09:38:00', 480, 38, TRUE),
(6, 43, 'Llave de paso',       '2025-07-28 10:45:00', '2025-07-28 10:53:30', 510,101, TRUE),

-- Fase 2 - Agosto
(3,  2, 'Tuercas 1/4',         '2025-08-01 09:15:00', '2025-08-01 09:18:30', 210, 62, TRUE),
(5, 23, 'Lentes',              '2025-08-02 10:20:00', '2025-08-02 10:23:50', 230,  2, TRUE),
(4, 13, 'Desarmador Phillips', '2025-08-04 08:00:00', '2025-08-04 08:03:40', 220, 33, TRUE),
(6, 34, 'Cable 14',            '2025-08-05 11:10:00', '2025-08-05 11:13:30', 210, 92, TRUE),
(3, 50, 'Esmalte',             '2025-08-06 15:20:00', '2025-08-06 15:23:40', 220,127, TRUE),
(5, 31, 'Estopa',              '2025-08-07 09:35:00', '2025-08-07 09:38:50', 230, 13, TRUE),
(4, 19, 'Sierra circular',     '2025-08-08 10:10:00', '2025-08-08 10:13:20', 200, 39, TRUE),
(3, 27, 'Careta',              '2025-08-11 08:25:00', '2025-08-11 08:28:40', 220,  6, TRUE),
(6,  6, 'Arandelas 3/8',       '2025-08-12 14:15:00', '2025-08-12 14:18:20', 200, 66, TRUE),
(5, 39, 'Tubo PVC',            '2025-08-13 09:50:00', '2025-08-13 09:53:30', 210, 97, TRUE),
(4, 15, 'Llave 13',            '2025-08-14 16:30:00', '2025-08-14 16:33:20', 200, 35, TRUE),
(3, 48, 'Thinner',             '2025-08-15 09:00:00', '2025-08-15 09:03:40', 220,125, TRUE),
(6, 21, 'Rotomartillo',        '2025-08-18 10:25:00', '2025-08-18 10:29:00', 220, 41, TRUE),
(5, 32, 'Cinta métrica',       '2025-08-19 11:15:00', '2025-08-19 11:18:40', 220, 14, TRUE),
(4, 10, 'Rondanas presión',    '2025-08-20 08:20:00', '2025-08-20 08:23:30', 210, 70, TRUE),
(3, 38, 'Caja eléctrica',      '2025-08-21 15:40:00', '2025-08-21 15:43:50', 230, 96, TRUE),
(5, 42, 'Pegamento PVC',       '2025-08-22 09:10:00', '2025-08-22 09:13:30', 210,100, TRUE),
(6, 14, 'Llave 10',            '2025-08-25 10:05:00', '2025-08-25 10:08:20', 200, 34, TRUE),
(3,  5, 'Tuercas 3/8',         '2025-08-26 08:35:00', '2025-08-26 08:38:50', 230, 65, TRUE),
(4, 49, 'Anticorrosivo',       '2025-08-27 14:50:00', '2025-08-27 14:53:40', 220,126, TRUE),
(5, 36, 'Apagador',            '2025-08-28 09:25:00', '2025-08-28 09:28:30', 210, 94, TRUE),
(6, 20, 'Pistola de calor',    '2025-08-29 11:40:00', '2025-08-29 11:44:10', 250, 40, TRUE),

-- Fase 3 - Septiembre (uso maduro)
(3,  1, 'Tornillos 1/4',       '2025-09-01 09:05:00', '2025-09-01 09:06:25',  85, 61, TRUE),
(5, 22, 'Guantes',             '2025-09-01 10:10:00', '2025-09-01 10:11:20',  80,  1, TRUE),
(4, 28, 'Cinta industrial',    '2025-09-02 08:30:00', '2025-09-02 08:31:25',  85, 10, TRUE),
(6, 44, 'Pintura blanca',      '2025-09-03 11:15:00', '2025-09-03 11:16:35',  95,121, TRUE),
(3, 17, 'Taladro',             '2025-09-04 09:45:00', '2025-09-04 09:46:30',  90, 37, TRUE),
(5, 26, 'Mascarilla N95',      '2025-09-05 10:20:00', '2025-09-05 10:21:15',  75,  5, TRUE),
(4, 37, 'Foco LED',            '2025-09-08 08:10:00', '2025-09-08 08:11:10',  70, 95, TRUE),
(3, 33, 'Cable 12',            '2025-09-09 15:25:00', '2025-09-09 15:26:35',  95, 91, TRUE),
(6, 40, 'Codo PVC',            '2025-09-10 09:00:00', '2025-09-10 09:01:20',  80, 98, TRUE),
(5, 47, 'Rodillo 9',           '2025-09-11 10:40:00', '2025-09-11 10:41:35',  95,124, TRUE),
(3,  9, 'Remaches',            '2025-09-12 08:45:00', '2025-09-12 08:46:35',  95, 69, TRUE),
(4, 12, 'Desarmador plano',    '2025-09-15 09:20:00', '2025-09-15 09:21:10',  70, 32, TRUE),
(6, 45, 'Pintura roja',        '2025-09-16 11:50:00', '2025-09-16 11:52:00',  85,122, TRUE),
(5, 29, 'Cinta aislar',        '2025-09-17 10:30:00', '2025-09-17 10:31:20',  80, 11, TRUE),
(3, 24, 'Casco',               '2025-09-18 08:25:00', '2025-09-18 08:26:15',  75,  3, TRUE),
(4, 11, 'Martillo',            '2025-09-19 09:55:00', '2025-09-19 09:57:00',  85, 31, TRUE),
(6, 35, 'Contacto doble',      '2025-09-22 14:10:00', '2025-09-22 14:11:25',  85, 93, TRUE),
(5, 41, 'Tee PVC',             '2025-09-23 10:00:00', '2025-09-23 10:01:10',  70, 99, TRUE),
(3, 46, 'Brocha 4',            '2025-09-24 11:30:00', '2025-09-24 11:31:30',  90,123, TRUE),
(4, 23, 'Lentes',              '2025-09-25 08:15:00', '2025-09-25 08:16:10',  70,  2, TRUE),
(6, 18, 'Esmeriladora',        '2025-09-26 09:40:00', '2025-09-26 09:41:40',  100,38, TRUE),
(5, 42, 'Pegamento PVC',       '2025-09-29 10:05:00', '2025-09-29 10:06:20',  80,100, TRUE),
(3, 50, 'Esmalte',             '2025-09-30 09:15:00', '2025-09-30 09:16:15',  75,127, TRUE),
(4, 20, 'Pistola de calor',    '2025-09-30 15:50:00', '2025-09-30 15:52:00',  85, 40, TRUE);

-- ============================================================
-- 10. INCIDENCIAS
-- ============================================================
INSERT INTO incidencias (tipo, producto_id, ubicacion_id, usuario_id, fecha, descripcion, resuelta, fecha_resolucion) VALUES
('MAL_UBICADO', 22, 13, 5, '2025-07-12 10:20:00', 'Guantes encontrados en pasillo de insumos en lugar de EPP', TRUE,  '2025-07-12 11:00:00'),
('FALTANTE',     3, 63, 4, '2025-07-20 17:50:00', 'Diferencia de 15 piezas en conteo cíclico',                  TRUE,  '2025-07-21 09:30:00'),
('MAL_UBICADO',  9, 69, 5, '2025-07-25 15:40:00', 'Remaches hallados en ubicación incorrecta',                  TRUE,  '2025-07-25 16:20:00'),
('DANADO',      17, 37, 5, '2025-08-02 11:15:00', 'Taladro con cable dañado, requiere revisión',                TRUE,  '2025-08-05 09:00:00'),
('MAL_UBICADO', 33, 91, 5, '2025-08-13 16:30:00', 'Cable calibre 14 colocado en ubicación de calibre 12',       TRUE,  '2025-08-13 17:15:00'),
('FALTANTE',    45,122, 4, '2025-08-22 18:10:00', 'Faltan 2 cubetas de pintura roja vs. sistema',               TRUE,  '2025-08-25 10:00:00'),
('DANADO',      46,123, 6, '2025-08-27 09:40:00', 'Brochas con cerdas desprendidas, no aptas para uso',         TRUE,  '2025-08-28 08:50:00'),
('MAL_UBICADO', 26,  5, 5, '2025-09-03 10:25:00', 'Mascarillas N95 en ubicación de tapones auditivos',          TRUE,  '2025-09-03 11:00:00'),
('FALTANTE',    44,121, 4, '2025-09-06 17:30:00', 'Pintura blanca con faltante de 1 cubeta',                    TRUE,  '2025-09-08 08:45:00'),
('DANADO',      48,125, 6, '2025-09-15 14:20:00', 'Botella de thinner con fuga, se desecha',                    TRUE,  '2025-09-15 15:10:00'),
('MAL_UBICADO', 47,124, 5, '2025-09-22 11:35:00', 'Rodillos en pasillo 4 en lugar de pasillo 5',                TRUE,  '2025-09-22 12:05:00'),
('OTRO',         5, 65, 4, '2025-09-28 16:50:00', 'Estante B nivel 2 requiere refuerzo estructural',            FALSE, NULL);


-- Total de ubicaciones (debe ser 150)
SELECT COUNT(*) FROM ubicaciones;

-- Tiempo promedio de búsqueda por mes
SELECT DATE_FORMAT(fecha_hora_inicio,'%Y-%m') AS mes,
       ROUND(AVG(tiempo_busqueda_segundos),1) AS promedio_seg
FROM busquedas
GROUP BY mes ORDER BY mes;

-- Productos con stock por debajo del mínimo (sumando ubicaciones)
SELECT p.codigo, p.nombre, p.stock_minimo, IFNULL(SUM(i.cantidad),0) AS stock_total
FROM productos p
LEFT JOIN inventario i ON i.producto_id = p.id
GROUP BY p.id
HAVING stock_total < p.stock_minimo;

-- Movimientos por tipo
SELECT tipo, COUNT(*) AS total, SUM(cantidad) AS piezas
FROM movimientos GROUP BY tipo;
