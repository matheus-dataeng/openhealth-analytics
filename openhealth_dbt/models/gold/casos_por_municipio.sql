SELECT
    LEFT(reg.cod_municipio::text, 6) AS cod_municipio,
    reg.uf,
    reg.nome_municipio,
    reg.nome_estado,
    reg.regiao,
    COUNT(*) AS total_casos,
    pop.populacao,
    ROUND((COUNT(*) * 100000.0 / NULLIF(pop.populacao, 0))::NUMERIC, 2) AS incidencia_por_100k_hab
FROM {{ ref('silver_dengue') }} den
LEFT JOIN {{ ref('silver_regiao') }} reg
    ON CAST(den.cod_municipio_residencia AS BIGINT)::text = LEFT(reg.cod_municipio::text, 6)
LEFT JOIN {{ ref('silver_populacao') }} pop
    ON LEFT(reg.cod_municipio::text, 6) = LEFT(pop.cod_municipio::text, 6)
GROUP BY
    LEFT(reg.cod_municipio::text, 6),
    reg.nome_municipio,
    reg.uf,
    reg.nome_estado,
    reg.regiao,
    pop.populacao
ORDER BY total_casos DESC