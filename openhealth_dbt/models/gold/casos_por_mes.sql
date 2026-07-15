SELECT
    TO_CHAR(data_notificacao, 'MM') AS mes,
    COUNT(*) AS total_casos
FROM {{ref ('silver_dengue')}}
GROUP BY TO_CHAR(data_notificacao, 'MM')
ORDER BY mes