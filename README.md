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

Puedes descargar la base de datos pre-cargada y lista para usar desde aquí:
[Descargar puestos_2026.db](../../releases/latest)

Una vez descargada, debe ubicarse dentro de la carpeta `db/`.

## Instrucciones para ejecución local
Para correr el proyecto desde cero:

1. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```

2. Descargar los datos (Scraping):
   ```
   python scraper/scraper.py
   ```

3. Procesar los JSON y armar la base de datos:
   ```
   python db/etl.py
   ```

4. Generar los datos para el dashboard:
   ```
   python dashboard/export_data.py
   ```

5. Ver el Dashboard:
   Abrir el archivo `dashboard/index.html` en el navegador web.

---
Elaborado por: Alberto Millán
