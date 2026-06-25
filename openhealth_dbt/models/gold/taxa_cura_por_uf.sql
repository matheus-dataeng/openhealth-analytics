SELECT
    uf,
    ROUND(100.0 * SUM(CASE WHEN evolucao = 'cura' THEN 1 ELSE 0 END) / COUNT(*), 2) AS percentual_cura
FROM {{ ref('silver_dengue') }}
GROUP BY uf
