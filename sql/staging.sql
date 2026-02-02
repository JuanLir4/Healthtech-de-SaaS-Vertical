-- vamos usar uma tabela staging para ajudar na importação entre csv para as tabelas finais
-- uma para cada tabela criada

CREATE TABLE stg_operadoras (
    registro_operadora TEXT,
    cnpj TEXT,
    razao_social TEXT,
    nome_fantasia TEXT,
    modalidade TEXT,
    logradouro TEXT,
    numero TEXT,
    complemento TEXT,
    bairro TEXT,
    cidade TEXT,
    uf TEXT,
    cep TEXT,
    ddd TEXT,
    telefone TEXT,
    fax TEXT,
    endereco_eletronico TEXT,
    representante TEXT,
    cargo_representante TEXT,
    regiao_comercializacao TEXT,
    data_registro_ans TEXT
);



CREATE TABLE stg_despesas_consolidadas (
    ano TEXT,
    trimestre TEXT,
    reg_ans TEXT,
    cd_conta_contabil TEXT,
    descricao TEXT,
    valor_despesa TEXT
);


CREATE TABLE stg_despesas_agregadas (
    razao_social TEXT,
    uf TEXT,
    valor_despesa TEXT
);

-- vou usar esse arquivo para carregar os csvs para staging tbm:


COPY stg_operadoras
FROM 'data/arquivosDescomp/Relatorio_cadop.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';


COPY stg_despesas_consolidadas
FROM 'data/arquivosDescomp/despesas_agregadas.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';


COPY stg_despesas_agregadas
FROM 'data/arquivosDescomp/resultado_final.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';
