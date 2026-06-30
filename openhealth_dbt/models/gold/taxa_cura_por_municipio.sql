SELECT
    ibge.nome_municipio,
    ibge.uf,
    COUNT(*) AS total_casos,
    ROUND(100.0 * SUM(CASE WHEN den.evolucao = 'cura' THEN 1 ELSE 0 END) / COUNT(*), 2) AS percentual_cura
FROM {{ ref('silver_dengue') }} AS den
LEFT JOIN {{ ref('silver_ibge') }} AS ibge
    ON CAST(den.cod_municipio_residencia AS BIGINT)::text = LEFT(ibge.cod_municipio::text, 6)
GROUP BY ibge.nome_municipio, ibge.uf
ORDER BY percentual_cura DESC