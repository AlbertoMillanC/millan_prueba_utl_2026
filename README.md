# MILLÁN — Prueba Técnica UTL Senado 2026

## Candidato
- **Nombre completo**: Alberto Millán
- **Email**: carlosalbertomillanc@gmail.com
- **URL del repositorio GitHub**: https://github.com/AlbertoMillanC/millan_prueba_utl_2026

## Instalación
Para preparar el entorno de ejecución, instale las dependencias especificadas:

```bash
pip install -r requirements.txt
```

## Pipeline de ejecución
El proyecto cuenta con un proceso de ingeniería de datos (ETL) completamente automatizado y reproducible.

1. **Extracción (Scraping):**
   ```bash
   python scraper/scraper.py
   ```
   *Descarga la información de la API de la Registraduría.*

2. **Transformación y Carga (Base de Datos):**
   ```bash
   python db/etl.py
   ```
   *Convierte los JSON en un modelo relacional y consolida la base de datos `puestos_2026.db`.*
   > **Nota:** La base de datos resultante pesa 480 MB y fue excluida mediante `.gitignore` para cumplir con las políticas de GitHub. Si no desea correr el pipeline desde cero, puede descargar el archivo SQLite desde la pestaña [Releases](../../releases/latest) y colocarlo en la carpeta `db/`.

3. **Análisis y Preparación de Datos:**
   ```bash
   python dashboard/export_data.py
   ```
   *Ejecuta consultas analíticas y exporta los agregados al archivo ligero `data.json`.*

4. **Visualización:**
   Abra el archivo `dashboard/index.html` en Chrome, Firefox o Edge.

## API
- **Patrón de URL**: `https://resultadospreccongreso2026.registraduria.gov.co/json/ACT/CO/XX/YYYYYYY.json` (donde XX es el corporativo y YYYYYYY el ID geográfico).
- **Campos JSON obligatorios mapeados**: `candidato`, `votos`, `partido`, `codpar`, `c`, `v`, `p`, `m`.
- **Nomenclátor**: Se obtiene haciendo un request GET directo al archivo raíz `/nomenclator.json`, el cual contiene la jerarquía completa (País > Departamento > Municipio > Zona > Puesto).
- **Cabeceras HTTP**: No requieren autenticación compleja, pero el scraper envía `User-Agent`, `Accept` y `Origin` para emular una solicitud de navegador válida y evitar bloqueos (403 Forbidden).

## Municipios en la BD
La extracción y análisis se centró en el "Top 4" de Boyacá:
1. **TUNJA** (Capital)
2. **PAIPA** (Ciudad Intermedia)
3. **SOGAMOSO** (Segunda ciudad)
4. **DUITAMA** (Tercera ciudad)

## Hallazgos principales
- **Caudal Electoral**: Tunja y Sogamoso representan la mayor concentración absoluta de sufragios en los cuatro municipios seleccionados, siendo determinantes en el cociente departamental.
- **Liderazgo Senado**: A diferencia de la Cámara de Representantes donde hay mayor variabilidad de movimientos regionales, en el Senado de la República las fuerzas mayoritarias (como el Partido Alianza Verde y el Pacto Histórico) logran consolidar sólidas votaciones a nivel municipal, confirmando el efecto "arrastre".
- **Comportamiento Urbano vs. Rural**: Las zonas densamente pobladas (mesas urbanas) muestran un comportamiento más heterogéneo en los votos de Cámara, mientras que los puestos rurales concentran la votación en líderes locales y regionales específicos (dominancia extrema).

## Bonus implementados
- **Flag `--preflight` en el scraper**: Muestra conteo de mesas sin descargar (`python scraper/scraper.py --preflight`).
- **Dark mode toggle con CSS custom properties**: Completamente implementado y automatizado según preferencias del navegador y botón manual en `index.html`.
- **Botón Exportar CSV/Excel funcional en el dashboard**: Implementado utilizando `ExcelJS` permitiendo exportar múltiples hojas y Data Bars nativos de Excel.
- **3+ índices SQLite con justificación**: Implementados indirectamente al definir Primary Keys (automáticamente indexadas) en el `schema.sql`.
