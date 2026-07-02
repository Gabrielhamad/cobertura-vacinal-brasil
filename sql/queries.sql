-- ============================================
-- Análise de Cobertura Vacinal - Queries SQL
-- ============================================

-- Query 1: Variação ano a ano por estado (window function LAG)
SELECT
    uf,
    vacina,
    ano,
    cobertura,
    LAG(cobertura) OVER (PARTITION BY uf, vacina ORDER BY ano) AS cobertura_ano_anterior,
    ROUND(cobertura - LAG(cobertura) OVER (PARTITION BY uf, vacina ORDER BY ano), 2) AS variacao_absoluta
FROM cobertura_vacinal
ORDER BY uf, vacina, ano;


-- Query 2: Ranking de estados por queda de cobertura entre 2019 e 2022 (CTE + RANK)
WITH variacao_por_estado AS (
    SELECT
        uf,
        AVG(CASE WHEN ano = 2019 THEN cobertura END) AS cobertura_2019,
        AVG(CASE WHEN ano = 2022 THEN cobertura END) AS cobertura_2022
    FROM cobertura_vacinal
    WHERE ano IN (2019, 2022)
    GROUP BY uf
)
SELECT
    uf,
    ROUND(cobertura_2019, 2) AS cobertura_2019,
    ROUND(cobertura_2022, 2) AS cobertura_2022,
    ROUND(cobertura_2022 - cobertura_2019, 2) AS variacao,
    RANK() OVER (ORDER BY (cobertura_2022 - cobertura_2019) ASC) AS ranking_queda
FROM variacao_por_estado
ORDER BY ranking_queda;


-- Query 3: Média móvel de 3 anos, cobertura nacional por vacina
SELECT
    vacina,
    ano,
    ROUND(AVG(cobertura), 2) AS cobertura_media_nacional,
    ROUND(AVG(AVG(cobertura)) OVER (
        PARTITION BY vacina 
        ORDER BY ano 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS media_movel_3_anos
FROM cobertura_vacinal
GROUP BY vacina, ano
ORDER BY vacina, ano;