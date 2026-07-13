# Prueba Técnica UTL 2026 - Alberto Millán

¡Bienvenido al repositorio de la solución de la prueba técnica! 

Este proyecto implementa un pipeline completo de extracción, transformación y carga (ETL), seguido de la generación de un Dashboard analítico moderno para la visualización de datos electorales.

## 🚀 Arquitectura del Proyecto

1. **Scraping (Extracción):** Scripts asíncronos (`scraper.py`) para consumir la API JSON cruda de la Registraduría (Nomenclátor departamental y miles de mesas a nivel municipal).
2. **Procesamiento y Base de Datos (ETL):** Script (`etl.py`) para parsear la estructura jerárquica de JSONs, aplanar la información y cargarla en una base de datos relacional robusta (SQLite3).
3. **Análisis de Datos:** Consultas SQL avanzadas para obtener insights como el Top 10 de Cámara, líderes al Senado, y el efecto de "arrastre" del Partido Alianza Verde.
4. **Exportación (Data Preparation):** Script (`export_data.py`) que condensa los resultados de la DB en un archivo ultra ligero `data.json` para consumo del Frontend.
5. **Dashboard Interactivo:** Interfaz gráfica web moderna (`index.html`) con diseño responsivo, gráficas interactivas (Chart.js), selectores de municipio, barras de datos CSS y exportación a Excel multi-hojas nativa.

## 🗄️ Base de Datos (SQLite)

> **⚠️ AVISO IMPORTANTE SOBRE LA BASE DE DATOS**
> Debido a que la base de datos resultante (`puestos_2026.db`) tiene un tamaño aproximado de 480 MB (lo cual supera el límite de 50 MB / 100 MB de GitHub), ha sido excluida del control de versiones mediante `.gitignore` cumpliendo con las instrucciones de la prueba.

Puedes descargar la base de datos pre-cargada y lista para usar desde los **Releases** de este repositorio.

🔗 **[Descargar puestos_2026.db desde GitHub Releases](../../releases/latest)**

*(Una vez descargada, colócala dentro de la carpeta `db/` para que los scripts locales puedan consultarla).*

## 💻 Instrucciones de Ejecución Local

Si deseas correr el proceso desde cero (descargar datos, crear DB e inyectar al dashboard):

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Ejecutar el Scraper (descarga los JSON):**
   ```bash
   python scraper/scraper.py
   ```
3. **Ejecutar el ETL (Crea la base de datos SQLite):**
   ```bash
   python db/etl.py
   ```
4. **Generar el JSON para el Dashboard:**
   ```bash
   python dashboard/export_data.py
   ```
5. **Visualizar:**
   Abre el archivo `dashboard/index.html` en cualquier navegador web.

---
**Elaborado por:** Alberto Millán
