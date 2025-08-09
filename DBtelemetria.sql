-- CREATE DATABASE IF NOT EXISTS DBTelemetria;
-- USE DBTelemetria;

-- -- Empresas
-- CREATE TABLE IF NOT EXISTS Empresas (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     cnpj VARCHAR(18) NOT NULL,
--     nome VARCHAR(100) NOT NULL
-- );

-- CREATE TABLE IF NOT EXISTS Importacoes(
-- 	-- ID(PK) da Importações
-- 	id INT auto_increment primary key,
-- 	-- Datas da importação
-- 	data_inicial DATE,
-- 	data_final DATE,
-- 	-- ID da empresa de importação
-- 	empresa_id INT,
-- 	-- Deleta os registros com relação ao id da empresa
-- 	FOREIGN KEY (empresa_id) references Empresas(id) ON DELETE CASCADE
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

-- Tabela de Importações.
CREATE TABLE IF NOT EXISTS Importacoes(
	
	-- ID(PK) da Importações
	id INT auto_increment primary key,
	
	-- Datas da importação
	data_inicial DATE,
	data_final DATE,
	
	-- Itens inseridos
	qtd_itens INT,
	
	-- ID da empresa de importação
	empresa_id INT,

	-- Deleta os registros com relação ao id da empresa
	FOREIGN KEY (empresa_id) references Empresas(id) ON DELETE CASCADE
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
    importacao_id INT,
    FOREIGN KEY (empresa_id) REFERENCES Empresas(id) ON DELETE CASCADE,
    FOREIGN KEY (importacao_id) REFERENCES Importacoes(id) ON DELETE CASCADE;
);

-- Motoristas
CREATE TABLE IF NOT EXISTS Motoristas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    data_inicial DATE,
    data_final DATE,
    veiculo_id INT,
    empresa_id INT,
    importacao_id INT,
    distancia_total DECIMAL(10,2),
    marcha_lenta_total TIME,
    consumo_total DECIMAL(10,2),
    consumo_medio DECIMAL(5,2),
    avaliacao DECIMAL(3,2),
    FOREIGN KEY (veiculo_id) REFERENCES Veiculos(id) ON DELETE SET NULL,
    FOREIGN KEY (empresa_id) REFERENCES Empresas(id) ON DELETE CASCADE,
    FOREIGN KEY (importacao_id) REFERENCES Importacoes(id) ON DELETE CASCADE;
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

