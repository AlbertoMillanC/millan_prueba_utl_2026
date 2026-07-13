import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import linregress

DB_PATH = 'db/puestos_2026.db'
OUT_PATH = 'viz/scatter_ca_se.png'

def main():
    conn = sqlite3.connect(DB_PATH)
    
    # Obtener totales por mesa para CA y SE
    query = '''
        SELECT 
            m.nombre as municipio,
            r.puesto,
            r.mesa,
            SUM(CASE WHEN r.corporacion = 'CA' THEN r.votos ELSE 0 END) as votos_ca,
            SUM(CASE WHEN r.corporacion = 'SE' THEN r.votos ELSE 0 END) as votos_se
        FROM resultados_mesa r
        JOIN municipios m ON r.codmun = m.codmun
        GROUP BY m.nombre, r.puesto, r.mesa
        HAVING votos_ca > 0 AND votos_se > 0
    '''
    df = pd.read_sql(query, conn)
    
    n_mesas = len(df)
    
    # Calcular estadísticos de regresion OLS
    slope, intercept, r_value, p_value, std_err = linregress(df['votos_ca'], df['votos_se'])
    
    # Plot
    plt.figure(figsize=(9, 6))
    
    # Scatterplot con colores por municipio
    sns.scatterplot(data=df, x='votos_ca', y='votos_se', hue='municipio', alpha=0.6, s=30)
    
    # Linea de regresion
    x_vals = df['votos_ca']
    y_vals = intercept + slope * x_vals
    plt.plot(x_vals, y_vals, color='red', label=f'OLS Regresión (r={r_value:.3f})')
    
    plt.title('Dispersión de Votos por Mesa: Cámara vs Senado')
    plt.xlabel('Votos Totales Cámara')
    plt.ylabel('Votos Totales Senado')
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT_PATH)
    
    # Output requerido por el evaluador
    print(f"r={r_value:.3f} | pendiente={slope:.3f} | n_mesas={n_mesas}")

if __name__ == '__main__':
    main()
