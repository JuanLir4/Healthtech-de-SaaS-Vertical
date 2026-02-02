-- =====================================================
-- QUERY 1
-- 5 operadoras com maior crescimento percentual
-- entre o primeiro e o último trimestre analisado
-- =====================================================

WITH despesas_trimestre AS (
    SELECT
        operadora_id,
        (ano * 10 + trimestre) AS periodo,
        SUM(valor_despesa) AS total
    FROM despesas_consolidadas
    GROUP BY operadora_id, ano, trimestre
),
primeiro_ultimo AS (
    SELECT
        operadora_id,
        FIRST_VALUE(total) OVER w AS primeiro_valor,
        LAST_VALUE(total) OVER w AS ultimo_valor
    FROM despesas_trimestre
    WINDOW w AS (
        PARTITION BY operadora_id
        ORDER BY periodo
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    )
)
SELECT
    o.razao_social,
    ROUND(
        ((ultimo_valor - primeiro_valor) / primeiro_valor) * 100,
        2
    ) AS crescimento_percentual
FROM primeiro_ultimo pu
JOIN operadoras o ON o.id = pu.operadora_id
WHERE primeiro_valor > 0
GROUP BY o.razao_social, primeiro_valor, ultimo_valor
ORDER BY crescimento_percentual DESC
LIMIT 5;



-- =====================================================
-- QUERY 2
-- Distribuição de despesas por UF
-- + média de despesas por operadora
-- =====================================================

SELECT
    o.uf,
    SUM(d.valor_despesa) AS total_despesas,
    AVG(d.valor_despesa) AS media_por_operadora
FROM despesas_consolidadas d
JOIN operadoras o ON o.id = d.operadora_id
GROUP BY o.uf
ORDER BY total_despesas DESC
LIMIT 5;



-- =====================================================
-- QUERY 3
-- Operadoras acima da média geral
-- em pelo menos 2 dos 3 trimestres
-- =====================================================

WITH media_geral AS (
    SELECT AVG(valor_despesa) AS media
    FROM despesas_consolidadas
),
acima_media AS (
    SELECT
        operadora_id,
        ano,
        trimestre,
        SUM(valor_despesa) AS total
    FROM despesas_consolidadas
    GROUP BY operadora_id, ano, trimestre
),
contagem AS (
    SELECT
        a.operadora_id,
        COUNT(*) AS trimestres_acima
    FROM acima_media a
    CROSS JOIN media_geral m
    WHERE a.total > m.media
    GROUP BY a.operadora_id
)
SELECT COUNT(*) AS total_operadoras
FROM contagem
WHERE trimestres_acima >= 2;
