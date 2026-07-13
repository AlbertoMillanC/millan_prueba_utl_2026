-- Reto 3.3: Atribucion deterministica
-- Top 5 candidatos por atribución SE consolidada.
-- Formula: A_ij = (votos_cand / votos_partido) x votos_SE_partido

WITH partido_nombre_base AS (
    SELECT 
        codpar,
        -- Normalizar nombre para poder cruzar CA y SE
        REPLACE(REPLACE(nombre, ' (CA)', ''), ' (SE)', '') as nombre_base
    FROM partidos
),
votos_ca_partido AS (
    SELECT 
        pb.nombre_base,
        SUM(r.votos) as votos_totales_ca
    FROM resultados_mesa r
    JOIN partido_nombre_base pb ON r.codpar = pb.codpar
    WHERE r.corporacion = 'CA'
    GROUP BY pb.nombre_base
),
votos_se_partido AS (
    SELECT 
        pb.nombre_base,
        SUM(r.votos) as votos_totales_se
    FROM resultados_mesa r
    JOIN partido_nombre_base pb ON r.codpar = pb.codpar
    WHERE r.corporacion = 'SE'
    GROUP BY pb.nombre_base
),
votos_candidato_ca AS (
    SELECT 
        c.codcan,
        c.nombre as candidato,
        pb.nombre_base,
        SUM(r.votos) as votos_cand
    FROM resultados_mesa r
    JOIN candidatos c ON r.codcan = c.codcan AND r.corporacion = c.corporacion AND r.codpar = c.codpar
    JOIN partido_nombre_base pb ON r.codpar = pb.codpar
    WHERE r.corporacion = 'CA'
    GROUP BY c.codcan, c.nombre, pb.nombre_base
)
SELECT 
    c.candidato,
    c.nombre_base AS partido,
    c.votos_cand,
    pca.votos_totales_ca AS votos_partido,
    pse.votos_totales_se AS votos_SE_partido,
    (CAST(c.votos_cand AS FLOAT) / NULLIF(pca.votos_totales_ca, 0)) * pse.votos_totales_se AS atribucion_se
FROM votos_candidato_ca c
JOIN votos_ca_partido pca ON c.nombre_base = pca.nombre_base
JOIN votos_se_partido pse ON c.nombre_base = pse.nombre_base
ORDER BY atribucion_se DESC
LIMIT 5;
