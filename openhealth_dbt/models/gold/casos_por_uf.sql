SELECT
    uf,
    COUNT(*) AS total_casos
FROM {{ ref('silver_dengue') }}
GROUP BY uf