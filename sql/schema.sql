-- dados cadastrais das operadoras:
CREATE TABLE operadoras (
    id SERIAL PRIMARY KEY,
    registro_operadora VARCHAR(20) UNIQUE,
    cnpj VARCHAR(14) UNIQUE NOT NULL,
    razao_social VARCHAR(255) NOT NULL,
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(100),
    logradouro VARCHAR(255),
    numero VARCHAR(20),
    complemento VARCHAR(255),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    uf CHAR(2),
    cep VARCHAR(8),
    ddd VARCHAR(3),
    telefone VARCHAR(20),
    fax VARCHAR(20),
    endereco_eletronico VARCHAR(255),
    representante VARCHAR(255),
    cargo_representante VARCHAR(100),
    regiao_comercializacao VARCHAR(100),
    data_registro_ans DATE
);

CREATE INDEX idx_operadoras_uf ON operadoras (uf);


-- tabela de despesas consolidadas:
CREATE TABLE despesas_consolidadas (
    id SERIAL PRIMARY KEY,
    operadora_id INT NOT NULL REFERENCES operadoras(id),
    ano INT NOT NULL,
    trimestre INT CHECK (trimestre BETWEEN 1 AND 4),
    cd_conta_contabil VARCHAR(50),
    descricao TEXT,
    valor_despesa DECIMAL(15,2) NOT NULL
);

CREATE INDEX idx_despesas_operadora ON despesas_consolidadas (operadora_id);
CREATE INDEX idx_despesas_tempo ON despesas_consolidadas (ano, trimestre);


-- tabela de despesas agregadas:
CREATE TABLE despesas_agregadas (
    operadora_id INT REFERENCES operadoras(id),
    uf CHAR(2),
    valor_total DECIMAL(15,2),
    PRIMARY KEY (operadora_id, uf)
);

-- abondagem normalizada separadas o que faz mais sentido para organização e analise
