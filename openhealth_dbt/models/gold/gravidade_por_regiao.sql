SELECT
    ibge.regiao,
    COUNT(*) AS total_casos,
    SUM(CASE WHEN d.classificacao_final = 'dengue grave' THEN 1 ELSE 0 END) AS casos_dengue_grave,
    ROUND(100.0 * SUM(CASE WHEN den.classificacao_final = 'dengue grave' THEN 1 ELSE 0 END) / COUNT(*), 2) AS percentual_dengue_grave
FROM {{ ref('silver_dengue') }} AS den
LEFT JOIN {{ ref('silver_ibge') }} AS ibge
    ON CAST(den.cod_municipio_residencia AS BIGINT)::text = LEFT(ibge.cod_municipio::text, 6)
GROUP BY ibge.regiao
ORDER BY percentual_dengue_grave DESC