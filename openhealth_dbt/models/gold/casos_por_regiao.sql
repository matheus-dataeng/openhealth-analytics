SELECT
    reg.regiao,
    COUNT(*) AS total_casos
FROM {{ ref('silver_dengue') }} AS den
LEFT JOIN {{ ref('silver_regiao') }} AS reg
    ON CAST(den.cod_municipio_residencia AS BIGINT)::text = LEFT(reg.cod_municipio::text, 6)
GROUP BY reg.regiao
ORDER BY total_casos DESC