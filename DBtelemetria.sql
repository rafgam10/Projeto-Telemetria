-- CREATE DATABASE IF NOT EXISTS DBTelemetria;
-- USE DBTelemetria;

-- -- Empresas
-- CREATE TABLE IF NOT EXISTS Empresas (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     cnpj VARCHAR(18) NOT NULL,
--     nome VARCHAR(100) NOT NULL
-- );

-- -- Veículos
-- CREATE TABLE IF NOT EXISTS Veiculos (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     placa VARCHAR(20) NOT NULL,             -- Novo
--     frota VARCHAR(50),                      -- Novo
--     marca VARCHAR(50),                      -- Novo
--     modelo VARCHAR(50),                     -- Novo
--     data_inicial DATE,                      -- (F)
--     data_final DATE,                        -- (G)
--     distancia_viagem DECIMAL(10,2),         -- (I)
--     velocidade_maxima DECIMAL(5,2),         -- (M)
--     velocidade_media DECIMAL(5,2),          -- (N)
--     litros_consumidos DECIMAL(10,2),        -- (P)
--     consumo_medio DECIMAL(5,2),             -- (Q)
--     tempo_marcha_lenta TIME,                -- (T)
--     empresa_id INT,
--     FOREIGN KEY (empresa_id) REFERENCES Empresas(id)
-- );

-- -- Motoristas
-- CREATE TABLE IF NOT EXISTS Motoristas (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     nome VARCHAR(100) NOT NULL,             -- (A)
--     data_inicial DATE,                      -- Novo
--     data_final DATE,                        -- Novo
--     veiculo_id INT,                         -- (AI)
--     empresa_id INT,                         -- Novo
--     distancia_total DECIMAL(10,2),          -- (F)
--     marcha_lenta_total TIME,                -- (J)
--     consumo_total DECIMAL(10,2),            -- (AN)
--     consumo_medio DECIMAL(5,2),             -- (AO)
--     avaliacao DECIMAL(3,2),  -- Novo campo: avaliação do motorista (ex: 4.75)
--     FOREIGN KEY (veiculo_id) REFERENCES Veiculos(id),
--     FOREIGN KEY (empresa_id) REFERENCES Empresas(id)
-- );

-- -- Metas de Consumo
-- CREATE TABLE IF NOT EXISTS MetasConsumo (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     empresa_id INT NOT NULL,
--     marca VARCHAR(50) NOT NULL,
--     modelo VARCHAR(50) NOT NULL,
--     meta_km_por_litro DECIMAL(5,2) NOT NULL,
--     UNIQUE KEY (empresa_id, marca, modelo),
--     FOREIGN KEY (empresa_id) REFERENCES Empresas(id)
-- );

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
    placa VARCHAR(20) NOT NULL,
    frota VARCHAR(50),
    marca VARCHAR(50),
    modelo VARCHAR(50),
    data_inicial DATE,
    data_final DATE,
    distancia_viagem DECIMAL(10,2),
    velocidade_maxima DECIMAL(5,2),
    velocidade_media DECIMAL(5,2),
    litros_consumidos DECIMAL(10,2),
    consumo_medio DECIMAL(5,2),
    tempo_marcha_lenta TIME,
    empresa_id INT,
    FOREIGN KEY (empresa_id) REFERENCES Empresas(id) ON DELETE CASCADE
);

-- Motoristas
CREATE TABLE IF NOT EXISTS Motoristas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    data_inicial DATE,
    data_final DATE,
    veiculo_id INT,
    empresa_id INT,
    distancia_total DECIMAL(10,2),
    marcha_lenta_total TIME,
    consumo_total DECIMAL(10,2),
    consumo_medio DECIMAL(5,2),
    avaliacao DECIMAL(3,2),
    FOREIGN KEY (veiculo_id) REFERENCES Veiculos(id) ON DELETE SET NULL,
    FOREIGN KEY (empresa_id) REFERENCES Empresas(id) ON DELETE CASCADE
);

-- Metas de Consumo
CREATE TABLE IF NOT EXISTS MetasConsumo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empresa_id INT NOT NULL,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    meta_km_por_litro DECIMAL(5,2) NOT NULL,
    UNIQUE KEY (empresa_id, marca, modelo),
    FOREIGN KEY (empresa_id) REFERENCES Empresas(id) ON DELETE CASCADE
);

------------------------------------------------------------------------

INSERT INTO Empresas (cnpj, nome) VALUES

('12.345.678/0001-01', 'Transportes Rapido'),
('23.456.789/0001-02', 'Logistica Nacional'),
('34.567.890/0001-03', 'Cargas Pesadas e Cia');

INSERT INTO Veiculos (placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES

('ABC1D23', 'Frota A', 'Volvo', 'FH 540', '2023-06-02', '2023-06-08', 3850.50, 98.75, 72.30, 385.25, 10.00, '05:30:00', 1),
('DEF4G56', 'Frota A', 'Volvo', 'FM 420', '2023-06-02', '2023-06-08', 4200.75, 95.20, 68.45, 420.30, 9.99, '04:45:00', 1),
('GHI7J89', 'Frota B', 'Scania', 'R 450', '2023-06-02', '2023-06-08', 4500.25, 102.30, 75.60, 425.50, 10.59, '06:15:00', 1),
('JKL1M23', 'Frota B', 'Mercedes', 'Actros 2651', '2023-06-02', '2023-06-08', 5100.80, 97.45, 70.20, 500.75, 10.20, '05:50:00', 1),
('MNO4P56', 'Frota C', 'Ford', 'Cargo 2429', '2023-06-02', '2023-06-08', 3250.30, 92.10, 65.80, 350.40, 9.29, '03:30:00', 1),


('PQR7S89', 'Frota X', 'Volvo', 'FH 460', '2023-06-02', '2023-06-08', 4800.60, 99.80, 73.25, 450.90, 10.64, '07:10:00', 2),
('STU1V23', 'Frota X', 'Scania', 'G 410', '2023-06-02', '2023-06-08', 4400.40, 96.50, 69.80, 415.60, 10.58, '06:25:00', 2),
('VWX4Y56', 'Frota Y', 'Mercedes', 'Axor 2545', '2023-06-02', '2023-06-08', 3950.75, 94.20, 67.40, 390.30, 10.13, '05:15:00', 2),
('YZA7B89', 'Frota Y', 'DAF', 'XF 480', '2023-06-02', '2023-06-08', 5200.90, 98.60, 71.90, 475.80, 10.93, '07:00:00', 2),
('BCD1E23', 'Frota Z', 'Iveco', 'Hi-Way 460', '2023-06-02', '2023-06-08', 3800.20, 93.75, 66.50, 400.25, 9.50, '04:50:00', 2),


('EFG4H56', 'Frota Pesada 1', 'Scania', 'S 730', '2023-06-02', '2023-06-08', 5000.75, 105.40, 77.20, 455.60, 10.97, '08:20:00', 3),
('HIJ7K89', 'Frota Pesada 1', 'Volvo', 'FH16 750', '2023-06-02', '2023-06-08', 5200.30, 108.20, 78.60, 470.75, 11.05, '09:15:00', 3),
('LMN1O23', 'Frota Pesada 2', 'Mercedes', 'Actros 2663', '2023-06-02', '2023-06-08', 4600.40, 101.50, 74.30, 430.90, 10.67, '07:30:00', 3),
('OPQ4R56', 'Frota Pesada 2', 'MAN', 'TGX 40.640', '2023-06-02', '2023-06-08', 4300.60, 99.30, 72.80, 410.40, 10.49, '06:45:00', 3),
('RST7U89', 'Frota Leve', 'Volkswagen', 'Constellation 24.250', '2023-06-02', '2023-06-08', 2900.80, 92.80, 66.20, 310.60, 9.35, '04:00:00', 3);

INSERT INTO Motoristas (nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio, avaliacao) VALUES

('João Silva', '2023-06-02', '2023-06-08', 1, 1, 3850.50, '05:30:00', 385.25, 10.00, 4.75),
('Carlos Oliveira', '2023-06-02', '2023-06-08', 2, 1, 4200.75, '04:45:00', 420.30, 9.99, 4.50),
('Mário Santos', '2023-06-02', '2023-06-08', 3, 1, 4500.25, '06:15:00', 425.50, 10.59, 4.80),
('Pedro Costa', '2023-06-02', '2023-06-08', 4, 1, 5100.80, '05:50:00', 500.75, 10.20, 4.25),
('Lucas Pereira', '2023-06-02', '2023-06-08', 5, 1, 3250.30, '03:30:00', 350.40, 9.29, 4.60),


('Antônio Rodrigues', '2023-06-02', '2023-06-08', 6, 2, 4800.60, '07:10:00', 450.90, 10.64, 4.90),
('Francisco Almeida', '2023-06-02', '2023-06-08', 7, 2, 4400.40, '06:25:00', 415.60, 10.58, 4.65),
('Ricardo Nunes', '2023-06-02', '2023-06-08', 8, 2, 3950.75, '05:15:00', 390.30, 10.13, 4.30),
('Eduardo Souza', '2023-06-02', '2023-06-08', 9, 2, 5200.90, '07:00:00', 475.80, 10.93, 4.85),
('Marcos Lima', '2023-06-02', '2023-06-08', 10, 2, 3800.20, '04:50:00', 400.25, 9.50, 4.40),


('Roberto Fernandes', '2023-06-02', '2023-06-08', 11, 3, 5000.75, '08:20:00', 455.60, 10.97, 4.95),
('Paulo Gonçalves', '2023-06-02', '2023-06-08', 12, 3, 5200.30, '09:15:00', 470.75, 11.05, 4.70),
('José Carvalho', '2023-06-02', '2023-06-08', 13, 3, 4600.40, '07:30:00', 430.90, 10.67, 4.55),
('Daniel Martins', '2023-06-02', '2023-06-08', 14, 3, 4300.60, '06:45:00', 410.40, 10.49, 4.80),
('Fernando Ribeiro', '2023-06-02', '2023-06-08', 15, 3, 2900.80, '04:00:00', 310.60, 9.35, 4.35);

INSERT INTO MetasConsumo (empresa_id, marca, modelo, meta_km_por_litro) VALUES

(1, 'Volvo', 'FH 540', 10.50),
(1, 'Volvo', 'FM 420', 10.00),
(1, 'Scania', 'R 450', 10.80),
(1, 'Mercedes', 'Actros 2651', 10.20),
(1, 'Ford', 'Cargo 2429', 9.50),

(2, 'Volvo', 'FH 460', 11.00),
(2, 'Scania', 'G 410', 10.60),
(2, 'Mercedes', 'Axor 2545', 10.40),
(2, 'DAF', 'XF 480', 11.20),
(2, 'Iveco', 'Hi-Way 460', 10.00),

(3, 'Scania', 'S 730', 11.50),
(3, 'Volvo', 'FH16 750', 11.80),
(3, 'Mercedes', 'Actros 2663', 11.20),
(3, 'MAN', 'TGX 40.640', 11.00),
(3, 'Volkswagen', 'Constellation 24.250', 10.00);

-- Semana 2: 2023-06-09 a 2023-06-15 (com variações mais acentuadas)
INSERT INTO Veiculos (placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES
('ABC1D23', 'Frota A', 'Volvo', 'FH 540', '2023-06-09', '2023-06-15', 4200.75, 105.20, 68.40, 400.25, 10.50, '08:45:00', 1),  -- Maior velocidade, mais marcha lenta
('DEF4G56', 'Frota A', 'Volvo', 'FM 420', '2023-06-09', '2023-06-15', 3800.60, 92.30, 62.10, 420.50, 9.04, '03:15:00', 1),    -- Consumo piorado
('GHI7J89', 'Frota B', 'Scania', 'R 450', '2023-06-09', '2023-06-15', 4800.20, 98.50, 72.30, 410.80, 11.69, '04:30:00', 1),   -- Melhor consumo
('JKL1M23', 'Frota B', 'Mercedes', 'Actros 2651', '2023-06-09', '2023-06-15', 3500.40, 94.20, 65.80, 380.60, 9.20, '07:20:00', 1), -- Distância reduzida
('MNO4P56', 'Frota C', 'Ford', 'Cargo 2429', '2023-06-09', '2023-06-15', 4100.30, 97.80, 70.40, 390.20, 10.51, '02:45:00', 1),  -- Melhor performance

('PQR7S89', 'Frota X', 'Volvo', 'FH 460', '2023-06-09', '2023-06-15', 5100.40, 103.50, 75.20, 490.60, 10.40, '09:30:00', 2),   -- Alta distância
('STU1V23', 'Frota X', 'Scania', 'G 410', '2023-06-09', '2023-06-15', 3600.80, 89.20, 60.40, 400.30, 9.00, '05:45:00', 2),      -- Baixa performance
('VWX4Y56', 'Frota Y', 'Mercedes', 'Axor 2545', '2023-06-09', '2023-06-15', 4300.60, 96.80, 70.60, 380.40, 11.30, '03:15:00', 2), -- Excelente consumo
('YZA7B89', 'Frota Y', 'DAF', 'XF 480', '2023-06-09', '2023-06-15', 4700.20, 99.60, 73.40, 420.80, 11.16, '06:20:00', 2),      -- Boa performance
('BCD1E23', 'Frota Z', 'Iveco', 'Hi-Way 460', '2023-06-09', '2023-06-15', 3200.40, 90.50, 63.20, 360.40, 8.88, '08:10:00', 2), -- Pior consumo

('EFG4H56', 'Frota Pesada 1', 'Scania', 'S 730', '2023-06-09', '2023-06-15', 5500.60, 108.40, 80.20, 480.60, 11.44, '10:45:00', 3), -- Alta performance
('HIJ7K89', 'Frota Pesada 1', 'Volvo', 'FH16 750', '2023-06-09', '2023-06-15', 4800.40, 102.60, 75.80, 460.20, 10.43, '08:30:00', 3), -- Consumo reduzido
('LMN1O23', 'Frota Pesada 2', 'Mercedes', 'Actros 2663', '2023-06-09', '2023-06-15', 3900.80, 95.40, 68.20, 400.60, 9.74, '05:15:00', 3), -- Distância menor
('OPQ4R56', 'Frota Pesada 2', 'MAN', 'TGX 40.640', '2023-06-09', '2023-06-15', 5100.20, 101.80, 76.40, 440.80, 11.56, '04:45:00', 3),  -- Melhor consumo
('RST7U89', 'Frota Leve', 'Volkswagen', 'Constellation 24.250', '2023-06-09', '2023-06-15', 2700.60, 88.40, 62.80, 320.40, 8.43, '06:30:00', 3); -- Pior cenário

-- Motoristas correspondentes para a Semana 2
INSERT INTO Motoristas (nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio, avaliacao) VALUES
('João Silva', '2023-06-09', '2023-06-15', 16, 1, 4200.75, '08:45:00', 400.25, 10.50, 4.60),  -- Marcha lenta aumentada
('Carlos Oliveira', '2023-06-09', '2023-06-15', 17, 1, 3800.60, '03:15:00', 420.50, 9.04, 3.80),  -- Avaliação reduzida
('Mário Santos', '2023-06-09', '2023-06-15', 18, 1, 4800.20, '04:30:00', 410.80, 11.69, 4.90),   -- Excelente desempenho
('Pedro Costa', '2023-06-09', '2023-06-15', 19, 1, 3500.40, '07:20:00', 380.60, 9.20, 4.20),    -- Performance regular
('Lucas Pereira', '2023-06-09', '2023-06-15', 20, 1, 4100.30, '02:45:00', 390.20, 10.51, 4.70),  -- Bom desempenho

('Antônio Rodrigues', '2023-06-09', '2023-06-15', 21, 2, 5100.40, '09:30:00', 490.60, 10.40, 4.85),  -- Alta distância
('Francisco Almeida', '2023-06-09', '2023-06-15', 22, 2, 3600.80, '05:45:00', 400.30, 9.00, 3.90),  -- Baixa performance
('Ricardo Nunes', '2023-06-09', '2023-06-15', 23, 2, 4300.60, '03:15:00', 380.40, 11.30, 5.00),     -- Melhor motorista
('Eduardo Souza', '2023-06-09', '2023-06-15', 24, 2, 4700.20, '06:20:00', 420.80, 11.16, 4.95),     -- Ótimo desempenho
('Marcos Lima', '2023-06-09', '2023-06-15', 25, 2, 3200.40, '08:10:00', 360.40, 8.88, 3.75),        -- Pior desempenho

('Roberto Fernandes', '2023-06-09', '2023-06-15', 26, 3, 5500.60, '10:45:00', 480.60, 11.44, 5.00),  -- Melhor em tudo
('Paulo Gonçalves', '2023-06-09', '2023-06-15', 27, 3, 4800.40, '08:30:00', 460.20, 10.43, 4.60),   -- Regular
('José Carvalho', '2023-06-09', '2023-06-15', 28, 3, 3900.80, '05:15:00', 400.60, 9.74, 4.30),      -- Performance média
('Daniel Martins', '2023-06-09', '2023-06-15', 29, 3, 5100.20, '04:45:00', 440.80, 11.56, 4.95),    -- Excelente consumo
('Fernando Ribeiro', '2023-06-09', '2023-06-15', 30, 3, 2700.60, '06:30:00', 320.40, 8.43, 3.50);  -- Pior avaliação

INSERT INTO Veiculos (placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES
('ABC1D23', 'Frota A', 'Volvo', 'FH 540', '2023-06-16', '2023-06-22', 3800.20, 97.50, 65.30, 370.40, 10.26, '04:30:00', 1),  -- Melhorou marcha lenta
('DEF4G56', 'Frota A', 'Volvo', 'FM 420', '2023-06-16', '2023-06-22', 4100.60, 95.80, 70.20, 390.80, 10.50, '06:15:00', 1),   -- Melhorou consumo
('GHI7J89', 'Frota B', 'Scania', 'R 450', '2023-06-16', '2023-06-22', 3500.40, 92.40, 64.20, 380.60, 9.20, '08:20:00', 1),    -- Piorou desempenho
('JKL1M23', 'Frota B', 'Mercedes', 'Actros 2651', '2023-06-16', '2023-06-22', 4800.80, 100.60, 74.80, 440.20, 10.91, '03:45:00', 1), -- Melhorou
('MNO4P56', 'Frota C', 'Ford', 'Cargo 2429', '2023-06-16', '2023-06-22', 2900.60, 88.20, 61.50, 330.40, 8.78, '07:15:00', 1), -- Pior cenário

('PQR7S89', 'Frota X', 'Volvo', 'FH 460', '2023-06-16', '2023-06-22', 4400.20, 98.40, 72.60, 410.60, 10.71, '05:30:00', 2),   -- Normalizado
('STU1V23', 'Frota X', 'Scania', 'G 410', '2023-06-16', '2023-06-22', 5100.40, 104.20, 77.30, 460.40, 11.07, '04:15:00', 2),  -- Excelente
('VWX4Y56', 'Frota Y', 'Mercedes', 'Axor 2545', '2023-06-16', '2023-06-22', 3600.80, 91.20, 65.40, 390.20, 9.23, '08:45:00', 2), -- Piorou
('YZA7B89', 'Frota Y', 'DAF', 'XF 480', '2023-06-16', '2023-06-22', 3900.60, 94.60, 68.20, 360.80, 10.80, '05:15:00', 2),     -- Redução distância
('BCD1E23', 'Frota Z', 'Iveco', 'Hi-Way 460', '2023-06-16', '2023-06-22', 4700.40, 99.80, 73.60, 430.60, 10.91, '03:30:00', 2), -- Melhorou

('EFG4H56', 'Frota Pesada 1', 'Scania', 'S 730', '2023-06-16', '2023-06-22', 4900.20, 103.80, 76.40, 440.20, 11.13, '07:45:00', 3), -- Normal
('HIJ7K89', 'Frota Pesada 1', 'Volvo', 'FH16 750', '2023-06-16', '2023-06-22', 4100.60, 97.20, 71.20, 390.40, 10.51, '05:30:00', 3), -- Redução
('LMN1O23', 'Frota Pesada 2', 'Mercedes', 'Actros 2663', '2023-06-16', '2023-06-22', 5300.40, 106.80, 79.20, 470.60, 11.25, '04:00:00', 3), -- Melhor
('OPQ4R56', 'Frota Pesada 2', 'MAN', 'TGX 40.640', '2023-06-16', '2023-06-22', 3500.80, 92.40, 66.20, 370.40, 9.45, '09:15:00', 3),  -- Pior
('RST7U89', 'Frota Leve', 'Volkswagen', 'Constellation 24.250', '2023-06-16', '2023-06-22', 4500.60, 98.60, 72.40, 410.20, 10.97, '02:45:00', 3); -- Melhorou muito

-- Motoristas correspondentes para a Semana 3
INSERT INTO Motoristas (nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio, avaliacao) VALUES
('João Silva', '2023-06-16', '2023-06-22', 31, 1, 3800.20, '04:30:00', 370.40, 10.26, 4.75),
('Carlos Oliveira', '2023-06-16', '2023-06-22', 32, 1, 4100.60, '06:15:00', 390.80, 10.50, 4.50),
('Mário Santos', '2023-06-16', '2023-06-22', 33, 1, 3500.40, '08:20:00', 380.60, 9.20, 4.00),
('Pedro Costa', '2023-06-16', '2023-06-22', 34, 1, 4800.80, '03:45:00', 440.20, 10.91, 4.80),
('Lucas Pereira', '2023-06-16', '2023-06-22', 35, 1, 2900.60, '07:15:00', 330.40, 8.78, 3.60),

('Antônio Rodrigues', '2023-06-16', '2023-06-22', 36, 2, 4400.20, '05:30:00', 410.60, 10.71, 4.70),
('Francisco Almeida', '2023-06-16', '2023-06-22', 37, 2, 5100.40, '04:15:00', 460.40, 11.07, 5.00),
('Ricardo Nunes', '2023-06-16', '2023-06-22', 38, 2, 3600.80, '08:45:00', 390.20, 9.23, 4.20),
('Eduardo Souza', '2023-06-16', '2023-06-22', 39, 2, 3900.60, '05:15:00', 360.80, 10.80, 4.85),
('Marcos Lima', '2023-06-16', '2023-06-22', 40, 2, 4700.40, '03:30:00', 430.60, 10.91, 4.65),

('Roberto Fernandes', '2023-06-16', '2023-06-22', 41, 3, 4900.20, '07:45:00', 440.20, 11.13, 4.95),
('Paulo Gonçalves', '2023-06-16', '2023-06-22', 42, 3, 4100.60, '05:30:00', 390.40, 10.51, 4.55),
('José Carvalho', '2023-06-16', '2023-06-22', 43, 3, 5300.40, '04:00:00', 470.60, 11.25, 5.00),
('Daniel Martins', '2023-06-16', '2023-06-22', 44, 3, 3500.80, '09:15:00', 370.40, 9.45, 4.10),
('Fernando Ribeiro', '2023-06-16', '2023-06-22', 45, 3, 4500.60, '02:45:00', 410.20, 10.97, 4.80);

INSERT INTO Veiculos (placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES

('ABC1D23', 'Frota A', 'Volvo', 'FH 540', '2023-06-23', '2023-06-29', 4500.60, 107.80, 78.20, 405.40, 11.10, '03:15:00', 1),  -- Melhor desempenho
('DEF4G56', 'Frota A', 'Volvo', 'FM 420', '2023-06-23', '2023-06-29', 3200.40, 89.50, 60.80, 390.20, 8.20, '10:30:00', 1),    -- Pior consumo
('GHI7J89', 'Frota B', 'Scania', 'R 450', '2023-06-23', '2023-06-29', 5100.80, 103.40, 76.50, 430.60, 11.84, '02:45:00', 1),  -- Excelente semana
('JKL1M23', 'Frota B', 'Mercedes', 'Actros 2651', '2023-06-23', '2023-06-29', 2800.20, 85.20, 58.60, 320.40, 8.74, '09:45:00', 1), -- Problemas mecânicos?
('MNO4P56', 'Frota C', 'Ford', 'Cargo 2429', '2023-06-23', '2023-06-29', 4700.40, 99.60, 73.80, 420.80, 11.17, '04:15:00', 1),  -- Melhorou muito

('PQR7S89', 'Frota X', 'Volvo', 'FH 460', '2023-06-23', '2023-06-29', 3900.60, 93.40, 67.20, 410.40, 9.51, '07:45:00', 2),     -- Performance média
('STU1V23', 'Frota X', 'Scania', 'G 410', '2023-06-23', '2023-06-29', 5400.20, 108.60, 80.10, 470.20, 11.48, '01:30:00', 2),  -- Recorde de distância
('VWX4Y56', 'Frota Y', 'Mercedes', 'Axor 2545', '2023-06-23', '2023-06-29', 2500.80, 82.40, 56.20, 300.60, 8.32, '12:15:00', 2), -- Problemas graves
('YZA7B89', 'Frota Y', 'DAF', 'XF 480', '2023-06-23', '2023-06-29', 4300.40, 97.80, 71.40, 380.20, 11.31, '03:00:00', 2),     -- Bom desempenho
('BCD1E23', 'Frota Z', 'Iveco', 'Hi-Way 460', '2023-06-23', '2023-06-29', 3600.60, 90.80, 64.60, 420.40, 8.56, '08:30:00', 2), -- Consumo ruim

('EFG4H56', 'Frota Pesada 1', 'Scania', 'S 730', '2023-06-23', '2023-06-29', 5800.40, 112.40, 83.20, 500.60, 11.59, '05:45:00', 3), -- Velocidade máxima alta
('HIJ7K89', 'Frota Pesada 1', 'Volvo', 'FH16 750', '2023-06-23', '2023-06-29', 4950.60, 104.20, 77.60, 430.40, 11.50, '04:00:00', 3), -- Boa performance
('LMN1O23', 'Frota Pesada 2', 'Mercedes', 'Actros 2663', '2023-06-23', '2023-06-29', 4100.80, 96.20, 70.40, 420.60, 9.75, '06:15:00', 3), -- Regular
('OPQ4R56', 'Frota Pesada 2', 'MAN', 'TGX 40.640', '2023-06-23', '2023-06-29', 3300.40, 88.60, 62.40, 360.20, 9.16, '10:00:00', 3), -- Baixa performance
('RST7U89', 'Frota Leve', 'Volkswagen', 'Constellation 24.250', '2023-06-23', '2023-06-29', 4900.20, 100.40, 74.60, 430.80, 11.37, '02:15:00', 3); -- Excelente semana

-- Motoristas correspondentes para a Semana 4
INSERT INTO Motoristas (nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio, avaliacao) VALUES

('João Silva', '2023-06-23', '2023-06-29', 46, 1, 4500.60, '03:15:00', 405.40, 11.10, 5.00),
('Carlos Oliveira', '2023-06-23', '2023-06-29', 47, 1, 3200.40, '10:30:00', 390.20, 8.20, 3.20),
('Mário Santos', '2023-06-23', '2023-06-29', 48, 1, 5100.80, '02:45:00', 430.60, 11.84, 5.00),
('Pedro Costa', '2023-06-23', '2023-06-29', 49, 1, 2800.20, '09:45:00', 320.40, 8.74, 3.00),
('Lucas Pereira', '2023-06-23', '2023-06-29', 50, 1, 4700.40, '04:15:00', 420.80, 11.17, 4.90),

('Antônio Rodrigues', '2023-06-23', '2023-06-29', 51, 2, 3900.60, '07:45:00', 410.40, 9.51, 4.30),
('Francisco Almeida', '2023-06-23', '2023-06-29', 52, 2, 5400.20, '01:30:00', 470.20, 11.48, 5.00),
('Ricardo Nunes', '2023-06-23', '2023-06-29', 53, 2, 2500.80, '12:15:00', 300.60, 8.32, 2.80),
('Eduardo Souza', '2023-06-23', '2023-06-29', 54, 2, 4300.40, '03:00:00', 380.20, 11.31, 5.00),
('Marcos Lima', '2023-06-23', '2023-06-29', 55, 2, 3600.60, '08:30:00', 420.40, 8.56, 3.50),

('Roberto Fernandes', '2023-06-23', '2023-06-29', 56, 3, 5800.40, '05:45:00', 500.60, 11.59, 5.00),
('Paulo Gonçalves', '2023-06-23', '2023-06-29', 57, 3, 4950.60, '04:00:00', 430.40, 11.50, 4.95),
('José Carvalho', '2023-06-23', '2023-06-29', 58, 3, 4100.80, '06:15:00', 420.60, 9.75, 4.20),
('Daniel Martins', '2023-06-23', '2023-06-29', 59, 3, 3300.40, '10:00:00', 360.20, 9.16, 3.80),
('Fernando Ribeiro', '2023-06-23', '2023-06-29', 60, 3, 4900.20, '02:15:00', 430.80, 11.37, 4.95);

INSERT INTO Veiculos (placa, frota, marca, modelo, data_inicial, data_final, distancia_viagem, velocidade_maxima, velocidade_media, litros_consumidos, consumo_medio, tempo_marcha_lenta, empresa_id) VALUES

('ABC1D23', 'Frota A', 'Volvo', 'FH 540', '2023-06-30', '2023-07-06', 4100.40, 98.60, 72.40, 380.60, 10.77, '04:30:00', 1),  -- Normalizado
('DEF4G56', 'Frota A', 'Volvo', 'FM 420', '2023-06-30', '2023-07-06', 3800.80, 94.20, 68.60, 370.40, 10.26, '05:45:00', 1),  -- Recuperação
('GHI7J89', 'Frota B', 'Scania', 'R 450', '2023-06-30', '2023-07-06', 3400.60, 90.80, 65.20, 320.80, 10.60, '07:15:00', 1),  -- Queda performance
('JKL1M23', 'Frota B', 'Mercedes', 'Actros 2651', '2023-06-30', '2023-07-06', 5000.20, 101.20, 75.80, 450.60, 11.09, '03:00:00', 1), -- Excelente
('MNO4P56', 'Frota C', 'Ford', 'Cargo 2429', '2023-06-30', '2023-07-06', 2900.40, 87.60, 61.80, 310.20, 9.35, '08:45:00', 1), -- Problemas novamente

('PQR7S89', 'Frota X', 'Volvo', 'FH 460', '2023-06-30', '2023-07-06', 4600.60, 100.40, 74.20, 420.40, 10.94, '04:00:00', 2), -- Bom desempenho
('STU1V23', 'Frota X', 'Scania', 'G 410', '2023-06-30', '2023-07-06', 5200.40, 106.80, 79.00, 460.80, 11.28, '02:30:00', 2),  -- Mantém bom nível
('VWX4Y56', 'Frota Y', 'Mercedes', 'Axor 2545', '2023-06-30', '2023-07-06', 4800.20, 99.20, 73.60, 430.60, 11.14, '03:45:00', 2), -- Melhoria radical
('YZA7B89', 'Frota Y', 'DAF', 'XF 480', '2023-06-30', '2023-07-06', 3500.80, 92.40, 66.80, 340.20, 10.29, '06:30:00', 2),    -- Queda
('BCD1E23', 'Frota Z', 'Iveco', 'Hi-Way 460', '2023-06-30', '2023-07-06', 4200.60, 96.80, 71.20, 390.40, 10.76, '04:15:00', 2), -- Melhorou

('EFG4H56', 'Frota Pesada 1', 'Scania', 'S 730', '2023-06-30', '2023-07-06', 5100.20, 105.60, 78.40, 450.20, 11.33, '04:45:00', 3), -- Continua bom
('HIJ7K89', 'Frota Pesada 1', 'Volvo', 'FH16 750', '2023-06-30', '2023-07-06', 4300.40, 98.20, 72.80, 390.60, 11.01, '05:15:00', 3), -- Normal
('LMN1O23', 'Frota Pesada 2', 'Mercedes', 'Actros 2663', '2023-06-30', '2023-07-06', 4700.60, 102.40, 76.20, 420.80, 11.16, '03:30:00', 3), -- Melhorou
('OPQ4R56', 'Frota Pesada 2', 'MAN', 'TGX 40.640', '2023-06-30', '2023-07-06', 3900.80, 94.60, 69.40, 370.20, 10.54, '07:00:00', 3), -- Recuperação
('RST7U89', 'Frota Leve', 'Volkswagen', 'Constellation 24.250', '2023-06-30', '2023-07-06', 3100.40, 90.20, 64.60, 290.40, 10.68, '05:45:00', 3); -- Redução

-- Motoristas correspondentes para a Semana 5
INSERT INTO Motoristas (nome, data_inicial, data_final, veiculo_id, empresa_id, distancia_total, marcha_lenta_total, consumo_total, consumo_medio, avaliacao) VALUES

('João Silva', '2023-06-30', '2023-07-06', 61, 1, 4100.40, '04:30:00', 380.60, 10.77, 4.80),
('Carlos Oliveira', '2023-06-30', '2023-07-06', 62, 1, 3800.80, '05:45:00', 370.40, 10.26, 4.50),
('Mário Santos', '2023-06-30', '2023-07-06', 63, 1, 3400.60, '07:15:00', 320.80, 10.60, 4.20),
('Pedro Costa', '2023-06-30', '2023-07-06', 64, 1, 5000.20, '03:00:00', 450.60, 11.09, 5.00),
('Lucas Pereira', '2023-06-30', '2023-07-06', 65, 1, 2900.40, '08:45:00', 310.20, 9.35, 3.80),

('Antônio Rodrigues', '2023-06-30', '2023-07-06', 66, 2, 4600.60, '04:00:00', 420.40, 10.94, 4.90),
('Francisco Almeida', '2023-06-30', '2023-07-06', 67, 2, 5200.40, '02:30:00', 460.80, 11.28, 5.00),
('Ricardo Nunes', '2023-06-30', '2023-07-06', 68, 2, 4800.20, '03:45:00', 430.60, 11.14, 4.95),
('Eduardo Souza', '2023-06-30', '2023-07-06', 69, 2, 3500.80, '06:30:00', 340.20, 10.29, 4.60),
('Marcos Lima', '2023-06-30', '2023-07-06', 70, 2, 4200.60, '04:15:00', 390.40, 10.76, 4.70),

('Roberto Fernandes', '2023-06-30', '2023-07-06', 71, 3, 5100.20, '04:45:00', 450.20, 11.33, 5.00),
('Paulo Gonçalves', '2023-06-30', '2023-07-06', 72, 3, 4300.40, '05:15:00', 390.60, 11.01, 4.85),
('José Carvalho', '2023-06-30', '2023-07-06', 73, 3, 4700.60, '03:30:00', 420.80, 11.16, 4.95),
('Daniel Martins', '2023-06-30', '2023-07-06', 74, 3, 3900.80, '07:00:00', 370.20, 10.54, 4.50),
('Fernando Ribeiro', '2023-06-30', '2023-07-06', 75, 3, 3100.40, '05:45:00', 290.40, 10.68, 4.65);