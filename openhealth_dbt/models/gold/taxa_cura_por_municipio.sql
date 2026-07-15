SELECT
    reg.nome_municipio,
    reg.uf,
    COUNT(*) AS total_casos,
    ROUND(100.0 * SUM(CASE WHEN den.evolucao = 'cura' THEN 1 ELSE 0 END) / COUNT(*), 2) AS percentual_cura
FROM {{ ref('silver_dengue') }} AS den
LEFT JOIN {{ ref('silver_regiao') }} AS reg
    ON CAST(den.cod_municipio_residencia AS BIGINT)::text = LEFT(reg.cod_municipio::text, 6)
GROUP BY reg.nome_municipio, reg.uf
ORDER BY percentual_cura DESC