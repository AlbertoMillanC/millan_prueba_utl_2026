-- Reto 3.1: Arrastre Verde CA->SE.
-- Ratio votos_SE_Verde / votos_CA_Verde por puesto y municipio.
-- Top 5 puestos con mayor arrastre (>1.5).

WITH verde_ca AS (
    SELECT codmun, puesto, SUM(votos) as votos_ca
    FROM resultados_mesa
    WHERE corporacion = 'CA' AND codpar = '5'
    GROUP BY codmun, puesto
),
verde_se AS (
    SELECT codmun, puesto, SUM(votos) as votos_se
    FROM resultados_mesa
    WHERE corporacion = 'SE' AND codpar = '57'
    GROUP BY codmun, puesto
)
SELECT 
    m.nombre AS municipio,
    se.puesto,
    COALESCE(se.votos_se, 0) AS votos_senado_verde,
    COALESCE(ca.votos_ca, 0) AS votos_camara_verde,
    CAST(COALESCE(se.votos_se, 0) AS FLOAT) / NULLIF(ca.votos_ca, 0) AS ratio_arrastre
FROM verde_se se
JOIN verde_ca ca ON se.codmun = ca.codmun AND se.puesto = ca.puesto
JOIN municipios m ON se.codmun = m.codmun
WHERE (CAST(COALESCE(se.votos_se, 0) AS FLOAT) / NULLIF(ca.votos_ca, 0)) > 1.5
ORDER BY ratio_arrastre DESC
LIMIT 5;
