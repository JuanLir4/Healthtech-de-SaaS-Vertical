-- =====================================================
-- TRANSFORMAÇÃO: STAGING → MODELO FINAL
-- =====================================================

-- (opcional, mas recomendado para reexecução)
-- Limpa dados anteriores mantendo estrutura
TRUNCATE TABLE despesas_agregadas;
TRUNCATE TABLE despesas_consolidadas;
TRUNCATE TABLE operadoras CASCADE;


-- =====================================================
-- 1. OPERADORAS
-- - Limpeza de CNPJ e CEP
-- - Padronização de UF
-- - Tratamento de múltiplos formatos de data
-- =====================================================

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
    REGEXP_REPLACE(cnpj, '[^0-9]', '', 'g')                    AS cnpj,
    razao_social,
    nome_fantasia,
    modalidade,
    logradouro,
    numero,
    complemento,
    bairro,
    cidade,
    UPPER(uf)                                                  AS uf,
    REGEXP_REPLACE(cep, '[^0-9]', '', 'g')                     AS cep,
    ddd,
    telefone,
    fax,
    endereco_eletronico,
    representante,
    cargo_representante,
    regiao_comercializacao,
    CASE
        WHEN data_registro_ans ~ '^\d{2}/\d{2}/\d{4}$'
            THEN TO_DATE(data_registro_ans, 'DD/MM/YYYY')
        WHEN data_registro_ans ~ '^\d{4}-\d{2}-\d{2}$'
            THEN TO_DATE(data_registro_ans, 'YYYY-MM-DD')
        ELSE NULL
    END                                                        AS data_registro_ans
FROM stg_operadoras
WHERE
    cnpj IS NOT NULL
    AND razao_social IS NOT NULL;


-- =====================================================
-- 2. DESPESAS CONSOLIDADAS
-- - Conversão de tipos
-- - Validação de valor monetário
-- - Associação via registro ANS
-- =====================================================

INSERT INTO despesas_consolidadas (
    operadora_id,
    ano,
    trimestre,
    cd_conta_contabil,
    descricao,
    valor_despesa
)
SELECT
    o.id                                                       AS operadora_id,
    CAST(s.ano AS INT)                                        AS ano,
    CAST(s.trimestre AS INT)                                  AS trimestre,
    s.cd_conta_contabil,
    s.descricao,
    CAST(REPLACE(s.valor_despesa, ',', '.') AS DECIMAL(15,2)) AS valor_despesa
FROM stg_despesas_consolidadas s
JOIN operadoras o
  ON o.registro_operadora = s.reg_ans
WHERE
    s.valor_despesa ~ '^[0-9,\.]+$';


-- =====================================================
-- 3. DESPESAS AGREGADAS
-- - Associação por razão social
-- - Padronização de UF
-- =====================================================

INSERT INTO despesas_agregadas (
    operadora_id,
    uf,
    valor_total
)
SELECT
    o.id                                                       AS operadora_id,
    UPPER(s.uf)                                               AS uf,
    CAST(REPLACE(s.valor_despesa, ',', '.') AS DECIMAL(15,2)) AS valor_total
FROM stg_despesas_agregadas s
JOIN operadoras o
  ON o.razao_social = s.razao_social;
