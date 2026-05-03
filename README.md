# Proyecto Final - Base de Datos I: Análisis del Presupuesto Nacional de la República Dominicana

## 📌 Información General
* **Institución:** Universidad Autónoma de Santo Domingo (UASD)
* **Programa:** Maestría en Ciencias de Datos e Inteligencia Artificial
* **Asignatura:** INF-8235-C2 - Base de Datos I
* **Autor:** Lic. Manuel Mañana Santana
* **LinkedIn:** [www.linkedin.com/in/manuelmañana](https://www.linkedin.com/in/manuelmañana)
* **Tutor:** (Como indicado en el programa)
* **Fecha de Entrega:** 2 de mayo del 2026
* **Fecha de Presentación:** 3 de mayo del 2026

## 🎯 Descripción del Proyecto
Este proyecto integrador pone en práctica todos los conocimientos adquiridos en modelado, diseño, implementación y análisis de bases de datos. Se fundamenta en la resolución de un problema real mediante el uso de datos abiertos proporcionados por el Gobierno Dominicano, enfocándose específicamente en el **Presupuesto Nacional de la República Dominicana**.

A través de este proyecto se aplica el ciclo de vida completo de los datos: desde la extracción y normalización de datasets, diseño conceptual (DER), lógico y físico, hasta la implementación en un motor relacional (**SQL Server**). Asimismo, se desarrollan procedimientos almacenados, disparadores (triggers), vistas analíticas, y se acompaña de un dashboard funcional para el análisis visual.

## 🗂️ Estructura del Repositorio

El repositorio sigue las mejores prácticas y estándares de organización de proyectos de ingeniería de datos (Guía 2.0):

* `datos/` : Contiene los datasets originales en `originales/` y las versiones normalizadas en `limpios/`.
* `dashboard/` : Archivos y recursos relacionados con la construcción del Dashboard HTML interactivo.
* `diagramas/` : Modelos de bases de datos (Conceptual, Lógico y Físico) en formato Mermaid (.mmd) y SVG.
* `docs/` : Documentación técnica, guías de configuración y diccionarios de datos.
* `documento/` : Informe final formal del proyecto (`informe_final_presupuesto.md`).
* `evidencias/` : Capturas de pantalla de la ejecución de scripts y resultados de consultas.
* `herramientas/` : Scripts de limpieza de datos en Python y utilidades.
* `powerbi/` : Archivo unificado para visualización en Power BI y guía técnica.
* `sql/` : Scripts de base de datos T-SQL (SQL Server):
  * `00_ejecutar_en_orden_sqlcmd.sql`: Guía de ejecución.
  * `01_ddl_presupuesto_nacional.sql`: Definición de estructura (Tablas, PK, FK, Constraints, Índices, Vistas).
  * `02_dml_presupuesto_nacional.sql`: Carga de datos reales y actualizaciones.
  * `03_dql_presupuesto_nacional.sql`: 25 consultas complejas analíticas.
  * `04_programacion_sp_triggers_presupuesto_nacional.sql`: Stored Procedures y Triggers.
  * `05_script_maestro_completo_presupuesto_nacional.sql`: Orquestador único.

## ⚙️ Tecnologías Utilizadas
* **Motor de Base de Datos:** Microsoft SQL Server
* **Modelado:** Mermaid.js / MySQL Workbench (Exportación T-SQL)
* **Análisis Exploratorio:** Python / Pandas
* **Visualización de Datos:** Power BI / HTML / CSS / JS
* **Entorno:** Windows 10/11

## 🚀 Instrucciones de Ejecución
1. Instalar y configurar **SQL Server** y **SSMS**.
2. Clonar el repositorio y configurar el archivo `.env.local` basado en `.env.example`.
3. Ejecutar el script maestro `sql/05_script_maestro_completo_presupuesto_nacional.sql`.
4. Verificar la carga con `sql/06_verificacion_demo_presupuesto_nacional.sql`.
*   Abrir el dashboard HTML en `dashboard/Dashboard_PresupuestoNacionalRD.html` o el archivo Power BI.


## 📄 Requerimientos Cumplidos
1. **Análisis del Dataset:** Perfilado y limpieza profunda.
2. **Modelado de Datos:** Esquema en Estrella (Star Schema) normalizado (3FN).
3. **T-SQL Robusto:** Uso de PK, FK, UNIQUE, CHECK, DEFAULT, Índices y Vistas.
4. **Carga Real:** Inserción de datos atómicos desde los archivos limpios.
5. **DQL Analítico:** 25 consultas abarcando agregaciones, joins y subconsultas.
6. **Programación DB:** Mínimo 5 Stored Procedures y Triggers de Auditoría/Validación.
7. **Visualización:** Dashboard con KPIs críticos y análisis visual.

---
*“Los datos son el nuevo lenguaje del mundo, y nosotros tenemos las herramientas para interpretarlo y transformarlo en conocimiento.”*
**- Lic. Manuel Mañana Santana**
