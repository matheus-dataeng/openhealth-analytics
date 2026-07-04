SELECT
    TO_CHAR(den.data_notificacao, 'YYYY-MM') AS ano_mes,
    den.uf,
    COUNT(*) AS total_casos,

    CAST(ROUND(AVG(cli.temperatura_media_c)::NUMERIC, 2) AS DOUBLE PRECISION) AS temperatura_media_c,

    CAST(ROUND(AVG(cli.temperatura_max_c)::NUMERIC, 2)AS DOUBLE PRECISION) AS temperatura_max_c,

    CAST(ROUND(AVG(cli.temperatura_min_c)::NUMERIC, 2) AS DOUBLE PRECISION) AS temperatura_min_c,

    CAST(ROUND(SUM(cli.precipitacao_total_mm)::NUMERIC, 2) AS DOUBLE PRECISION) AS precipitacao_total_mm,

    CAST(ROUND(AVG(cli.umidade_media_pct)::NUMERIC, 2)AS DOUBLE PRECISION) AS umidade_media_pct

FROM {{ ref('silver_dengue') }} AS den
LEFT JOIN {{ ref('silver_clima') }} AS cli
    ON den.uf = cli.uf
   AND DATE_TRUNC('month', den.data_notificacao) = DATE_TRUNC('month', cli.data)

GROUP BY
    TO_CHAR(den.data_notificacao, 'YYYY-MM'),
    den.uf

ORDER BY
    ano_mes,
    den.uf