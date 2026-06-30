SELECT
    ibge.regiao,
    COUNT(*) AS total_casos
FROM {{ ref('silver_dengue') }} AS den
LEFT JOIN {{ ref('silver_ibge') }} AS ibge
    ON CAST(den.cod_municipio_residencia AS BIGINT)::text = LEFT(ibge.cod_municipio::text, 6)
GROUP BY ibge.regiao
ORDER BY total_casos DESC