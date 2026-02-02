INSERT INTO operadoras (
    registro_operadora,
    cnpj,
    razao_social,
    nome_fantasia,
    modalidade,
    logradouro,
    numero,
    complemento,
    bairro,
    cidade,
    uf,
    cep,
    ddd,
    telefone,
    fax,
    endereco_eletronico,
    representante,
    cargo_representante,
    regiao_comercializacao,
    data_registro_ans
)
SELECT
    registro_operadora,
    REGEXP_REPLACE(cnpj, '[^0-9]', '', 'g'),
    razao_social,
    nome_fantasia,
    modalidade,
    logradouro,
    numero,
    complemento,
    bairro,
    cidade,
    UPPER(uf),
    REGEXP_REPLACE(cep, '[^0-9]', '', 'g'),
    ddd,
    telefone,
    fax,
    endereco_eletronico,
    representante,
    cargo_representante,
    regiao_comercializacao,
    TO_DATE(data_registro_ans, 'DD/MM/YYYY')
FROM stg_operadoras
WHERE
    cnpj IS NOT NULL
    AND razao_social IS NOT NULL;



INSERT INTO despesas_consolidadas (
    operadora_id,
    ano,
    trimestre,
    cd_conta_contabil,
    descricao,
    valor_despesa
)
SELECT
    o.id,
    CAST(s.ano AS INT),
    CAST(s.trimestre AS INT),
    s.cd_conta_contabil,
    s.descricao,
    CAST(REPLACE(s.valor_despesa, ',', '.') AS DECIMAL(15,2))
FROM stg_despesas_consolidadas s
JOIN operadoras o
  ON o.registro_operadora = s.reg_ans
WHERE
    s.valor_despesa ~ '^[0-9,\.]+$';


INSERT INTO despesas_agregadas (operadora_id, uf, valor_total)
SELECT
    o.id,
    UPPER(s.uf),
    CAST(REPLACE(s.valor_despesa, ',', '.') AS DECIMAL(15,2))
FROM stg_despesas_agregadas s
JOIN operadoras o
  ON o.razao_social = s.razao_social;
