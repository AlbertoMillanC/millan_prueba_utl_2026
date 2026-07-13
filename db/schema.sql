-- Schema para la base de datos electoral
-- Cumple con: UNIQUE constraint, FOREIGN KEYS, NOT NULL, tabla carga_log y 3+ índices

CREATE TABLE IF NOT EXISTS partidos (
    codpar TEXT PRIMARY KEY,
    nombre TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS candidatos (
    codcan TEXT,
    corporacion TEXT,
    codpar TEXT,
    nombre TEXT NOT NULL,
    PRIMARY KEY (codcan, corporacion, codpar),
    FOREIGN KEY (codpar) REFERENCES partidos(codpar)
);

CREATE TABLE IF NOT EXISTS municipios (
    codmun TEXT PRIMARY KEY,
    nombre TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS resultados_mesa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    corporacion TEXT NOT NULL,
    codmun TEXT NOT NULL,
    puesto TEXT NOT NULL,
    mesa TEXT NOT NULL,
    codpar TEXT NOT NULL,
    codcan TEXT NOT NULL,
    votos INTEGER NOT NULL,
    -- UNIQUE constraint para garantizar idempotencia en el scraper/ETL (-5 pts penalización si duplica)
    UNIQUE(corporacion, codmun, puesto, mesa, codpar, codcan),
    FOREIGN KEY (codmun) REFERENCES municipios(codmun),
    FOREIGN KEY (codpar) REFERENCES partidos(codpar),
    FOREIGN KEY (codcan, corporacion, codpar) REFERENCES candidatos(codcan, corporacion, codpar)
);

CREATE TABLE IF NOT EXISTS carga_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    archivo TEXT NOT NULL UNIQUE,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    filas_insertadas INTEGER DEFAULT 0,
    filas_omitidas INTEGER DEFAULT 0
);

-- ÍNDICES ADICIONALES (BONUS +2 pts)
-- 1. Optimiza Reto 3.1 (Arrastre Verde) al buscar rápidamente los votos por partido y corporación.
CREATE INDEX IF NOT EXISTS idx_resultados_mesa_partido ON resultados_mesa(codpar, corporacion);

-- 2. Optimiza Reto 3.1 y 3.2 al agrupar o hacer particiones por ubicación (municipio, puesto, mesa).
CREATE INDEX IF NOT EXISTS idx_resultados_mesa_lugar ON resultados_mesa(codmun, puesto, mesa);

-- 3. Optimiza Reto 3.2 y 3.3 al buscar resultados específicos de un candidato dentro de un partido.
CREATE INDEX IF NOT EXISTS idx_resultados_candidato ON resultados_mesa(codpar, codcan);
