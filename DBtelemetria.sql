CREATE DATABASE IF NOT EXISTS DBTelemetria;
USE DBTelemetria;

-- Empresas
CREATE TABLE IF NOT EXISTS Empresas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cnpj VARCHAR(18) NOT NULL,
    nome VARCHAR(100) NOT NULL
);

-- Veículos
CREATE TABLE IF NOT EXISTS Veiculos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    placa VARCHAR(20) NOT NULL,             -- Novo
    frota VARCHAR(50),                      -- Novo
    marca VARCHAR(50),                      -- Novo
    modelo VARCHAR(50),                     -- Novo
    data_inicial DATE,                      -- (F)
    data_final DATE,                        -- (G)
    distancia_viagem DECIMAL(10,2),         -- (I)
    velocidade_maxima DECIMAL(5,2),         -- (M)
    velocidade_media DECIMAL(5,2),          -- (N)
    litros_consumidos DECIMAL(10,2),        -- (P)
    consumo_medio DECIMAL(5,2),             -- (Q)
    tempo_marcha_lenta TIME,                -- (T)
    empresa_id INT,
    FOREIGN KEY (empresa_id) REFERENCES Empresas(id)
);

-- Motoristas
CREATE TABLE IF NOT EXISTS Motoristas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,             -- (A)
    data_inicial DATE,                      -- Novo
    data_final DATE,                        -- Novo
    veiculo_id INT,                         -- (AI)
    empresa_id INT,                         -- Novo
    distancia_total DECIMAL(10,2),          -- (F)
    marcha_lenta_total TIME,                -- (J)
    consumo_total DECIMAL(10,2),            -- (AN)
    consumo_medio DECIMAL(5,2),             -- (AO)
    FOREIGN KEY (veiculo_id) REFERENCES Veiculos(id),
    FOREIGN KEY (empresa_id) REFERENCES Empresas(id)
);

-- Metas de Consumo
CREATE TABLE IF NOT EXISTS MetasConsumo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empresa_id INT NOT NULL,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    meta_km_por_litro DECIMAL(5,2) NOT NULL,
    UNIQUE KEY (empresa_id, marca, modelo),
    FOREIGN KEY (empresa_id) REFERENCES Empresas(id)
);


------------------------------------------------------------------------

-- Inserção de Empresas
INSERT INTO Empresas (id, cnpj, nome) VALUES (1, '36.578.291/0001-47', 'Azevedo e Filhos Transportes');
INSERT INTO Empresas (id, cnpj, nome) VALUES (2, '46.971.503/0001-05', 'Silveira Transportes');
INSERT INTO Empresas (id, cnpj, nome) VALUES (3, '86.349.205/0001-00', 'Santos Transportes');

-- Inserção de Veículos
INSERT INTO Veiculos (id, placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES (1, 'RZE-0172', 'F-111', 'Volkswagen', 'Constellation 24.280', '2024-01-01', '2024-06-01', 877.05, 109.27, 73.01, 158.88, 4.6, '01:23:45', 1);
INSERT INTO Veiculos (id, placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES (2, 'ZAA-4445', 'F-112', 'Volkswagen', 'Constellation 24.280', '2024-01-01', '2024-06-01', 514.89, 106.7, 84.76, 173.83, 4.47, '01:23:45', 1);
INSERT INTO Veiculos (id, placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES (3, 'UIG-7979', 'F-113', 'Volkswagen', 'Constellation 24.280', '2024-01-01', '2024-06-01', 880.6, 104.75, 83.85, 59.78, 2.63, '01:23:45', 1);
INSERT INTO Veiculos (id, placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES (4, 'OYX-2865', 'F-121', 'Scania', 'R 450', '2024-01-01', '2024-06-01', 522.24, 116.05, 77.11, 193.9, 4.24, '01:23:45', 1);
INSERT INTO Veiculos (id, placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES (5, 'MQQ-6608', 'F-122', 'Scania', 'R 450', '2024-01-01', '2024-06-01', 501.39, 97.86, 64.62, 103.03, 3.2, '01:23:45', 1);
INSERT INTO Veiculos (id, placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES (6, 'XDE-5073', 'F-123', 'Scania', 'R 450', '2024-01-01', '2024-06-01', 206.18, 90.27, 65.64, 144.61, 3.49, '01:23:45', 1);
INSERT INTO Veiculos (id, placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES (7, 'CCM-8859', 'F-131', 'Iveco', 'Hi-Way', '2024-01-01', '2024-06-01', 638.43, 110.59, 66.37, 140.12, 2.61, '01:23:45', 1);
INSERT INTO Veiculos (id, placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES (8, 'KQU-3298', 'F-132', 'Iveco', 'Hi-Way', '2024-01-01', '2024-06-01', 999.33, 99.98, 74.03, 102.16, 4.12, '01:23:45', 1);
INSERT INTO Veiculos (id, placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES (9, 'PNQ-4518', 'F-133', 'Iveco', 'Hi-Way', '2024-01-01', '2024-06-01', 958.03, 82.15, 76.57, 179.26, 2.77, '01:23:45', 1);
INSERT INTO Veiculos (id, placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES (10, 'JSF-8053', 'F-141', 'DAF', 'XF 105', '2024-01-01', '2024-06-01', 1199.55, 117.28, 87.39, 171.54, 4.59, '01:23:45', 1);
INSERT INTO Veiculos (id, placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES (11, 'YUC-5252', 'F-142', 'DAF', 'XF 105', '2024-01-01', '2024-06-01', 275.49, 107.8, 73.08, 76.35, 3.63, '01:23:45', 1);
INSERT INTO Veiculos (id, placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES (12, 'GVA-2691', 'F-143', 'DAF', 'XF 105', '2024-01-01', '2024-06-01', 1155.11, 111.28, 85.04, 55.8, 4.43, '01:23:45', 1);
INSERT INTO Veiculos (id, placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES (13, 'XEG-2471', 'F-211', 'Mercedes-Benz', 'Actros 2651', '2024-01-01', '2024-06-01', 435.3, 99.56, 65.98, 165.72, 5.03, '01:23:45', 2);
INSERT INTO Veiculos (id, placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES (14, 'RFR-1850', 'F-212', 'Mercedes-Benz', 'Actros 2651', '2024-01-01', '2024-06-01', 754.05, 102.34, 81.56, 174.53, 4.28, '01:23:45', 2);
INSERT INTO Veiculos (id, placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES (15, 'FGM-5651', 'F-213', 'Mercedes-Benz', 'Actros 2651', '2024-01-01', '2024-06-01', 885.11, 108.73, 82.41, 125.2, 3.41, '01:23:45', 2);
INSERT INTO Veiculos (id, placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES (16, 'BOD-2247', 'F-221', 'DAF', 'XF 105', '2024-01-01', '2024-06-01', 995.39, 86.81, 74.86, 96.73, 4.26, '01:23:45', 2);
INSERT INTO Veiculos (id, placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES (17, 'DCN-9237', 'F-222', 'DAF', 'XF 105', '2024-01-01', '2024-06-01', 707.93, 114.76, 80.89, 179.94, 2.93, '01:23:45', 2);
INSERT INTO Veiculos (id, placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES (18, 'ZEA-7524', 'F-223', 'DAF', 'XF 105', '2024-01-01', '2024-06-01', 415.99, 93.6, 70.35, 55.59, 5.45, '01:23:45', 2);
INSERT INTO Veiculos (id, placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES (19, 'XEU-1092', 'F-231', 'Iveco', 'Hi-Way', '2024-01-01', '2024-06-01', 832.53, 115.79, 74.36, 136.7, 4.49, '01:23:45', 2);
INSERT INTO Veiculos (id, placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES (20, 'TOR-9461', 'F-232', 'Iveco', 'Hi-Way', '2024-01-01', '2024-06-01', 572.73, 90.38, 72.58, 175.15, 5.04, '01:23:45', 2);
INSERT INTO Veiculos (id, placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES (21, 'WYA-0327', 'F-233', 'Iveco', 'Hi-Way', '2024-01-01', '2024-06-01', 443.34, 111.0, 77.34, 96.17, 4.11, '01:23:45', 2);
INSERT INTO Veiculos (id, placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES (22, 'RLN-8529', 'F-241', 'Volkswagen', 'Constellation 24.280', '2024-01-01', '2024-06-01', 815.8, 119.79, 83.1, 71.92, 4.51, '01:23:45', 2);
INSERT INTO Veiculos (id, placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES (23, 'TJP-8709', 'F-242', 'Volkswagen', 'Constellation 24.280', '2024-01-01', '2024-06-01', 364.99, 112.96, 71.3, 72.48, 5.01, '01:23:45', 2);
INSERT INTO Veiculos (id, placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES (24, 'GMJ-4236', 'F-243', 'Volkswagen', 'Constellation 24.280', '2024-01-01', '2024-06-01', 846.16, 97.6, 60.91, 131.92, 5.44, '01:23:45', 2);
INSERT INTO Veiculos (id, placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES (25, 'BYO-4564', 'F-311', 'Mercedes-Benz', 'Actros 2651', '2024-01-01', '2024-06-01', 253.49, 85.02, 75.16, 149.51, 5.13, '01:23:45', 3);
INSERT INTO Veiculos (id, placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES (26, 'IFG-8924', 'F-312', 'Mercedes-Benz', 'Actros 2651', '2024-01-01', '2024-06-01', 723.78, 112.41, 71.4, 132.39, 2.57, '01:23:45', 3);
INSERT INTO Veiculos (id, placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES (27, 'NQE-0692', 'F-313', 'Mercedes-Benz', 'Actros 2651', '2024-01-01', '2024-06-01', 507.46, 111.92, 60.05, 57.01, 5.41, '01:23:45', 3);
INSERT INTO Veiculos (id, placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES (28, 'BQT-7178', 'F-321', 'DAF', 'XF 105', '2024-01-01', '2024-06-01', 643.87, 96.81, 60.6, 130.47, 5.31, '01:23:45', 3);
INSERT INTO Veiculos (id, placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES (29, 'KVS-7344', 'F-322', 'DAF', 'XF 105', '2024-01-01', '2024-06-01', 231.15, 85.05, 85.08, 166.97, 3.11, '01:23:45', 3);
INSERT INTO Veiculos (id, placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES (30, 'SJG-1843', 'F-323', 'DAF', 'XF 105', '2024-01-01', '2024-06-01', 804.27, 117.1, 71.65, 85.15, 4.14, '01:23:45', 3);
INSERT INTO Veiculos (id, placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES (31, 'TJX-2338', 'F-331', 'Iveco', 'Hi-Way', '2024-01-01', '2024-06-01', 337.98, 112.08, 76.55, 57.88, 4.37, '01:23:45', 3);
INSERT INTO Veiculos (id, placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES (32, 'EHC-6023', 'F-332', 'Iveco', 'Hi-Way', '2024-01-01', '2024-06-01', 775.27, 101.78, 75.57, 144.39, 4.54, '01:23:45', 3);
INSERT INTO Veiculos (id, placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES (33, 'UMK-7158', 'F-333', 'Iveco', 'Hi-Way', '2024-01-01', '2024-06-01', 564.73, 108.71, 73.68, 86.71, 3.22, '01:23:45', 3);
INSERT INTO Veiculos (id, placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES (34, 'RID-7720', 'F-341', 'Scania', 'R 450', '2024-01-01', '2024-06-01', 846.26, 92.16, 62.95, 93.09, 2.6, '01:23:45', 3);
INSERT INTO Veiculos (id, placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES (35, 'CXW-0868', 'F-342', 'Scania', 'R 450', '2024-01-01', '2024-06-01', 1102.27, 101.3, 64.4, 121.81, 2.55, '01:23:45', 3);
INSERT INTO Veiculos (id, placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES (36, 'MLJ-9773', 'F-343', 'Scania', 'R 450', '2024-01-01', '2024-06-01', 265.1, 113.39, 75.03, 111.33, 3.15, '01:23:45', 3);

-- Inserção de Motoristas
INSERT INTO Motoristas (id, nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio) VALUES (1, 'Benício Ferreira', '2024-01-01', '2024-06-01', 1, 1, 2650.96, '12:34:56', 915.25, 4.7);
INSERT INTO Motoristas (id, nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio) VALUES (2, 'Breno da Paz', '2024-01-01', '2024-06-01', 2, 1, 10327.67, '12:34:56', 2289.14, 3.11);
INSERT INTO Motoristas (id, nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio) VALUES (3, 'Ana Vitória Pinto', '2024-01-01', '2024-06-01', 3, 1, 10666.24, '12:34:56', 838.66, 2.87);
INSERT INTO Motoristas (id, nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio) VALUES (4, 'Otávio Santos', '2024-01-01', '2024-06-01', 4, 1, 6644.12, '12:34:56', 1012.8, 2.87);
INSERT INTO Motoristas (id, nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio) VALUES (5, 'Vitor Gabriel Rodrigues', '2024-01-01', '2024-06-01', 5, 1, 10932.72, '12:34:56', 2389.84, 2.83);
INSERT INTO Motoristas (id, nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio) VALUES (6, 'Isaac Farias', '2024-01-01', '2024-06-01', 6, 1, 10972.15, '12:34:56', 1937.07, 2.56);
INSERT INTO Motoristas (id, nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio) VALUES (7, 'Igor da Paz', '2024-01-01', '2024-06-01', 7, 1, 9177.56, '12:34:56', 1508.97, 4.03);
INSERT INTO Motoristas (id, nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio) VALUES (8, 'Noah Melo', '2024-01-01', '2024-06-01', 8, 1, 6888.73, '12:34:56', 1523.85, 3.96);
INSERT INTO Motoristas (id, nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio) VALUES (9, 'Ana Beatriz Santos', '2024-01-01', '2024-06-01', 9, 1, 9852.41, '12:34:56', 1620.55, 3.0);
INSERT INTO Motoristas (id, nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio) VALUES (10, 'Yuri das Neves', '2024-01-01', '2024-06-01', 10, 1, 5214.5, '12:34:56', 903.87, 2.54);
INSERT INTO Motoristas (id, nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio) VALUES (11, 'Calebe Dias', '2024-01-01', '2024-06-01', 11, 1, 3072.19, '12:34:56', 2263.25, 4.55);
INSERT INTO Motoristas (id, nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio) VALUES (12, 'Heloísa Sales', '2024-01-01', '2024-06-01', 12, 1, 3468.11, '12:34:56', 1962.1, 4.37);
INSERT INTO Motoristas (id, nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio) VALUES (13, 'Isabella Silva', '2024-01-01', '2024-06-01', 13, 2, 3986.91, '12:34:56', 2048.97, 3.36);
INSERT INTO Motoristas (id, nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio) VALUES (14, 'Otávio Rezende', '2024-01-01', '2024-06-01', 14, 2, 10612.67, '12:34:56', 2396.11, 3.09);
INSERT INTO Motoristas (id, nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio) VALUES (15, 'Dr. Daniel Sales', '2024-01-01', '2024-06-01', 15, 2, 10116.52, '12:34:56', 1434.51, 3.0);
INSERT INTO Motoristas (id, nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio) VALUES (16, 'Maria Farias', '2024-01-01', '2024-06-01', 16, 2, 11293.72, '12:34:56', 1592.19, 4.21);
INSERT INTO Motoristas (id, nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio) VALUES (17, 'Bianca Caldeira', '2024-01-01', '2024-06-01', 17, 2, 7215.34, '12:34:56', 1074.15, 5.4);
INSERT INTO Motoristas (id, nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio) VALUES (18, 'Amanda Viana', '2024-01-01', '2024-06-01', 18, 2, 4166.8, '12:34:56', 1305.12, 5.21);
INSERT INTO Motoristas (id, nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio) VALUES (19, 'Yago Cardoso', '2024-01-01', '2024-06-01', 19, 2, 8386.76, '12:34:56', 1816.73, 5.47);
INSERT INTO Motoristas (id, nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio) VALUES (20, 'João Gabriel Carvalho', '2024-01-01', '2024-06-01', 20, 2, 3478.93, '12:34:56', 2125.3, 4.67);
INSERT INTO Motoristas (id, nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio) VALUES (21, 'Ryan Ramos', '2024-01-01', '2024-06-01', 21, 2, 8987.98, '12:34:56', 1122.67, 3.81);
INSERT INTO Motoristas (id, nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio) VALUES (22, 'Ana Carolina Rocha', '2024-01-01', '2024-06-01', 22, 2, 7507.8, '12:34:56', 1976.21, 3.58);
INSERT INTO Motoristas (id, nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio) VALUES (23, 'Enrico Moura', '2024-01-01', '2024-06-01', 23, 2, 2698.3, '12:34:56', 1640.39, 5.47);
INSERT INTO Motoristas (id, nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio) VALUES (24, 'Bryan Porto', '2024-01-01', '2024-06-01', 24, 2, 3683.97, '12:34:56', 1128.18, 5.37);
INSERT INTO Motoristas (id, nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio) VALUES (25, 'Dr. Diogo Caldeira', '2024-01-01', '2024-06-01', 25, 3, 9486.21, '12:34:56', 1500.47, 4.42);
INSERT INTO Motoristas (id, nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio) VALUES (26, 'Dr. Rafael Azevedo', '2024-01-01', '2024-06-01', 26, 3, 2047.46, '12:34:56', 2259.08, 4.91);
INSERT INTO Motoristas (id, nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio) VALUES (27, 'Benício Novaes', '2024-01-01', '2024-06-01', 27, 3, 8279.6, '12:34:56', 2013.96, 4.93);
INSERT INTO Motoristas (id, nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio) VALUES (28, 'Caio Barros', '2024-01-01', '2024-06-01', 28, 3, 7558.39, '12:34:56', 1105.63, 3.05);
INSERT INTO Motoristas (id, nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio) VALUES (29, 'Vinicius Silveira', '2024-01-01', '2024-06-01', 29, 3, 6457.98, '12:34:56', 1097.57, 4.24);
INSERT INTO Motoristas (id, nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio) VALUES (30, 'Joaquim Fogaça', '2024-01-01', '2024-06-01', 30, 3, 5576.82, '12:34:56', 2369.42, 4.46);
INSERT INTO Motoristas (id, nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio) VALUES (31, 'Agatha Sales', '2024-01-01', '2024-06-01', 31, 3, 6013.01, '12:34:56', 977.25, 3.97);
INSERT INTO Motoristas (id, nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio) VALUES (32, 'Caio Oliveira', '2024-01-01', '2024-06-01', 32, 3, 6780.97, '12:34:56', 1683.81, 5.22);
INSERT INTO Motoristas (id, nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio) VALUES (33, 'João Guilherme Silva', '2024-01-01', '2024-06-01', 33, 3, 7326.87, '12:34:56', 1645.65, 4.96);
INSERT INTO Motoristas (id, nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio) VALUES (34, 'Alexandre Gonçalves', '2024-01-01', '2024-06-01', 34, 3, 5706.18, '12:34:56', 1428.71, 5.29);
INSERT INTO Motoristas (id, nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio) VALUES (35, 'Ana Carolina Ribeiro', '2024-01-01', '2024-06-01', 35, 3, 9294.71, '12:34:56', 1820.88, 5.03);
INSERT INTO Motoristas (id, nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio) VALUES (36, 'Dr. Anthony Ferreira', '2024-01-01', '2024-06-01', 36, 3, 10393.41, '12:34:56', 1279.35, 4.24);

-- Inserção de Metas de Consumo
INSERT INTO MetasConsumo (id, empresa_id, marca, modelo, meta_km_por_litro) VALUES (1, 1, 'Volkswagen', 'Constellation 24.280', 5.75);
INSERT INTO MetasConsumo (id, empresa_id, marca, modelo, meta_km_por_litro) VALUES (2, 1, 'Scania', 'R 450', 3.96);
INSERT INTO MetasConsumo (id, empresa_id, marca, modelo, meta_km_por_litro) VALUES (3, 1, 'Iveco', 'Hi-Way', 3.32);
INSERT INTO MetasConsumo (id, empresa_id, marca, modelo, meta_km_por_litro) VALUES (4, 1, 'DAF', 'XF 105', 3.79);
INSERT INTO MetasConsumo (id, empresa_id, marca, modelo, meta_km_por_litro) VALUES (5, 2, 'Mercedes-Benz', 'Actros 2651', 5.47);
INSERT INTO MetasConsumo (id, empresa_id, marca, modelo, meta_km_por_litro) VALUES (6, 2, 'DAF', 'XF 105', 3.8);
INSERT INTO MetasConsumo (id, empresa_id, marca, modelo, meta_km_por_litro) VALUES (7, 2, 'Iveco', 'Hi-Way', 5.0);
INSERT INTO MetasConsumo (id, empresa_id, marca, modelo, meta_km_por_litro) VALUES (8, 2, 'Volkswagen', 'Constellation 24.280', 4.44);
INSERT INTO MetasConsumo (id, empresa_id, marca, modelo, meta_km_por_litro) VALUES (9, 3, 'Mercedes-Benz', 'Actros 2651', 5.78);
INSERT INTO MetasConsumo (id, empresa_id, marca, modelo, meta_km_por_litro) VALUES (10, 3, 'DAF', 'XF 105', 5.96);
INSERT INTO MetasConsumo (id, empresa_id, marca, modelo, meta_km_por_litro) VALUES (11, 3, 'Iveco', 'Hi-Way', 5.68);
INSERT INTO MetasConsumo (id, empresa_id, marca, modelo, meta_km_por_litro) VALUES (12, 3, 'Scania', 'R 450', 4.53);