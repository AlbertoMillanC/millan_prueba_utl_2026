# Prueba Técnica UTL 2026

## Descripción del Proyecto
Este repositorio contiene la solución a la prueba técnica, incluyendo el proceso de extracción de datos, creación de la base de datos y el dashboard de visualización.

## Estructura
- **scraper/**: Contiene los scripts en Python usados para consumir la API de la Registraduría y descargar los JSON de las mesas.
- **db/**: Contiene el script `etl.py` encargado del procesamiento de datos. La base de datos resultante (`puestos_2026.db`) se encuentra disponible para su descarga en la sección de "Releases".
- **sql/**: Archivos con las consultas SQL requeridas en la prueba (Top Cámara, Arrastre, etc.).
- **dashboard/**: Contiene el frontend `index.html` y el script `export_data.py` encargado de generar el archivo ligero `data.json` para las gráficas.

## Base de Datos SQLite
Para cumplir con los lineamientos de la prueba técnica, dado que `puestos_2026.db` pesa cerca de 480 MB (superando el límite de 50 MB de GitHub), el archivo fue alojado directamente como un **Release**.

Puede descargar la base de datos pre-cargada y lista para usar desde aquí:
[Descargar puestos_2026.db](../../releases/latest)

Una vez descargada, debe ubicarse dentro de la carpeta `db/`.

## Uso del Dashboard (Resultados)
El dashboard interactivo ya se encuentra completamente generado y listo para su uso. **No es necesario ejecutar ningún script** para visualizar los datos.

Para acceder, simplemente abra el archivo `dashboard/index.html` en cualquier navegador web.

## Memoria Técnica (Código Fuente)
Los scripts en Python se incluyen en este repositorio como evidencia del trabajo de ingeniería de datos realizado (Scraping y ETL).

En caso de que el equipo evaluador desee auditar o reproducir el proceso de extracción desde cero, el orden de ejecución original fue el siguiente:

1. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```

2. Descargar los datos crudos de la API (Scraping):
   ```
   python scraper/scraper.py
   ```

3. Procesar los JSON y armar la base de datos SQLite:
   ```
   python db/etl.py
   ```

4. Exportar el archivo `data.json` que alimenta al dashboard:
   ```
   python dashboard/export_data.py
   ```

---
Elaborado por: Alberto Millán
