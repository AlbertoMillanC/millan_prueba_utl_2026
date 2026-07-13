import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

DB_PATH = 'db/puestos_2026.db'
OUT_PATH = 'viz/heatmap_municipios.png'

def main():
    conn = sqlite3.connect(DB_PATH)
    
    # 1. Encontrar top 8 candidatos CA a nivel global
    top8_query = '''
        SELECT c.codcan, c.nombre
        FROM resultados_mesa r
        JOIN candidatos c ON r.codcan = c.codcan AND r.corporacion = c.corporacion AND r.codpar = c.codpar
        WHERE r.corporacion = 'CA'
        GROUP BY c.codcan, c.nombre
        ORDER BY SUM(r.votos) DESC
        LIMIT 8
    '''
    top8_df = pd.read_sql(top8_query, conn)
    top8_cands = top8_df['nombre'].tolist()
    
    # 2. Votos totales por municipio en CA (para el denominador del %)
    totales_query = '''
        SELECT m.nombre as municipio, SUM(r.votos) as total_mun
        FROM resultados_mesa r
        JOIN municipios m ON r.codmun = m.codmun
        WHERE r.corporacion = 'CA'
        GROUP BY m.nombre
    '''
    totales_df = pd.read_sql(totales_query, conn)
    
    # 3. Votos de los top 8 por municipio
    votos_query = '''
        SELECT c.nombre as candidato, m.nombre as municipio, SUM(r.votos) as votos
        FROM resultados_mesa r
        JOIN candidatos c ON r.codcan = c.codcan AND r.corporacion = c.corporacion AND r.codpar = c.codpar
        JOIN municipios m ON r.codmun = m.codmun
        WHERE r.corporacion = 'CA'
    '''
    # We load all votes and filter in pandas, or just filter in SQL
    votos_df = pd.read_sql(votos_query + f" AND c.nombre IN ({','.join(['?']*8)}) GROUP BY c.nombre, m.nombre", conn, params=top8_cands)
    
    # Merge and calculate %
    df = pd.merge(votos_df, totales_df, on='municipio')
    df['porcentaje'] = (df['votos'] / df['total_mun']) * 100
    
    # Pivot for heatmap: index=candidato, columns=municipio, values=porcentaje
    pivot_df = df.pivot(index='candidato', columns='municipio', values='porcentaje').fillna(0)
    
    # Reordenar las filas para que coincidan con el top global (orden descendente)
    pivot_df = pivot_df.reindex(top8_cands)
    
    # Plot
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot_df, annot=True, fmt=".1f", cmap="YlGnBu", cbar_kws={'label': '% de Votos del Municipio'})
    plt.title('Top 8 Candidatos Cámara: % de Votos por Municipio')
    plt.ylabel('Candidato')
    plt.xlabel('Municipio')
    plt.tight_layout()
    plt.savefig(OUT_PATH)
    print(f"Heatmap guardado en {OUT_PATH}")

if __name__ == '__main__':
    main()
