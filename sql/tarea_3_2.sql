-- Reto 3.2: Mesas donde un candidato concentra >60% de los votos de su partido (indicador de maquinaria). 
-- Top 10 mesas más anómalas.

WITH total_partido_mesa AS (
    SELECT 
        corporacion, codmun, puesto, mesa, codpar, SUM(votos) as total_votos_partido
    FROM resultados_mesa
    GROUP BY corporacion, codmun, puesto, mesa, codpar
    HAVING SUM(votos) > 10 -- Evitar mesas con muy pocos votos donde un solo voto es 100%
),
candidato_mesa AS (
    SELECT 
        r.corporacion, r.codmun, r.puesto, r.mesa, r.codpar, r.codcan, c.nombre as candidato, r.votos
    FROM resultados_mesa r
    JOIN candidatos c ON r.codcan = c.codcan AND r.corporacion = c.corporacion AND r.codpar = c.codpar
)
SELECT 
    m.nombre AS municipio,
    c.corporacion,
    c.puesto,
    c.mesa,
    p.nombre AS partido,
    c.candidato,
    c.votos AS votos_candidato,
    t.total_votos_partido,
    CAST(c.votos AS FLOAT) / t.total_votos_partido AS porcentaje_dominancia
FROM candidato_mesa c
JOIN total_partido_mesa t ON c.corporacion = t.corporacion AND c.codmun = t.codmun AND c.puesto = t.puesto AND c.mesa = t.mesa AND c.codpar = t.codpar
JOIN municipios m ON c.codmun = m.codmun
JOIN partidos p ON c.codpar = p.codpar
WHERE (CAST(c.votos AS FLOAT) / t.total_votos_partido) > 0.60
ORDER BY porcentaje_dominancia DESC, c.votos DESC
LIMIT 10;
