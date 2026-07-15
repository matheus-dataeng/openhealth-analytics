SELECT
    CAST(data AS DATE) AS data,
    uf,
    ROUND(CAST(precipitacao_total_mm AS NUMERIC), 2) AS precipitacao_total_mm,
    ROUND(CAST(temperatura_media_c AS NUMERIC), 2) AS temperatura_media_c,
    ROUND(CAST(temperatura_max_c AS NUMERIC), 2) AS temperatura_max_c,
    ROUND(CAST(temperatura_min_c AS NUMERIC), 2) AS temperatura_min_c,
    ROUND(CAST(umidade_media_pct AS NUMERIC), 2) AS umidade_media_pct
FROM {{ ref('stg_raw_clima') }}
WHERE
    temperatura_media_c < 60
    AND temperatura_media_c > -10
    AND umidade_media_pct BETWEEN 0 AND 100