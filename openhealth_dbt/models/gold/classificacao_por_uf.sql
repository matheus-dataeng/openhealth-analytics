SELECT
	uf,
    classificacao_final,
    ROUND(
        100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY uf),
        2
    ) AS porcentagem
FROM {{ref ('silver_dengue')}}
GROUP BY uf, classificacao_final
ORDER BY uf, porcentagem DESC