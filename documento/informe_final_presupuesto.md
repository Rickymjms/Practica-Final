# Proyecto Final: Análisis de la Ejecución del Presupuesto Nacional RD

Universidad Autónoma de Santo Domingo (UASD)
Maestría en Ciencias de Datos e Inteligencia Artificial
Asignatura: Base de Datos I - INF-8235-C2
Estudiante: **Lic. Manuel Mañana Santana**
Tema: Modelado, implementación y análisis de datos abiertos de la Ejecución Presupuestaria
Fecha de entrega: 2 de mayo de 2026
Fecha de presentación: 3 de mayo de 2026

---

**Autor:** Lic. Manuel Mañana Santana
**LinkedIn:** [www.linkedin.com/in/manuelmañana](https://www.linkedin.com/in/manuelmañana)

---

## 1. Introducción
Este proyecto integra datos del Presupuesto Nacional de la República Dominicana para analizar la ejecución financiera (Devengado vs Presupuesto Vigente) por dimensiones clave como Institución, Programa, Objeto de Gasto, Geografía y Tiempo. El objetivo es proporcionar una herramienta robusta de Inteligencia de Negocios para la transparencia y el análisis de la inversión pública.

## 2. Análisis del Dataset
El proyecto se basa en los datos abiertos de la ejecución presupuestaria del Gobierno de la República Dominicana del año 2025. Los conjuntos de datos originales fueron extraídos en formatos CSV y Excel, requiriendo un proceso de perfilado para identificar cardinalidad, tipos de datos y problemas de calidad.

### Variables Principales
- **Financieras:** Presupuesto Inicial, Presupuesto Vigente, Devengado Aprobado.
- **Institucionales:** Capítulos, Subcapítulos, Unidades Ejecutoras.
- **Geográficas:** Región, Provincia, Municipio.
- **Programáticas:** Programas, Proyectos, Actividades.

### Limpieza y Preparación
- **Estandarización:** Se convirtieron los archivos a UTF-8 y se normalizaron nombres de instituciones y provincias.
- **Deduplicación:** Eliminación de registros redundantes en las dimensiones.
- **Transformación:** Conversión de campos de texto a valores numéricos y fechas válidas para SQL Server.
- **Rutas:** Los datos originales se conservan en `datos/originales/` y los procesados en `datos/limpios/`.

## 3. Modelado de Datos
Se implementó un **Esquema en Estrella (Star Schema)** para optimizar el rendimiento de las consultas analíticas.

- **Modelo Conceptual:** Entidades principales y sus relaciones de negocio.
- **Modelo Lógico:** Definición de tablas con PK, FK y relaciones 1:N.
- **Modelo Físico:** Implementación detallada con tipos de datos de SQL Server, restricciones (`CHECK`, `UNIQUE`, `DEFAULT`) e índices.

## 4. Normalización
El diseño de la base de datos sigue los principios de normalización:
- **1FN:** Valores atómicos en todas las celdas.
- **2FN:** Eliminación de dependencias parciales (uso de llaves primarias en dimensiones).
- **3FN:** Eliminación de dependencias transitivas (la geografía se jerarquiza correctamente).

## 5. Implementación en SQL Server (T-SQL)
La base de datos se denomina `PresupuestoNacionalRD`. La implementación se orquesta mediante los siguientes scripts:
1. `00_ejecutar_en_orden_sqlcmd.sql`: Guía de despliegue.
2. `01_ddl_presupuesto_nacional.sql`: Creación de la estructura, tablas y vistas.
3. `02_dml_presupuesto_nacional.sql`: Carga masiva de datos y actualizaciones de clasificación.
4. `03_dql_presupuesto_nacional.sql`: Repositorio de 25 consultas analíticas avanzadas.
5. `04_programacion_sp_triggers_presupuesto_nacional.sql`: Stored Procedures y Triggers de auditoría.
6. `05_script_maestro_completo_presupuesto_nacional.sql`: Script único de ejecución.

## 6. Programación y Lógica de Negocio
- **Stored Procedures:** Reportes de resumen anual, top N de instituciones y consultas por tipo de gasto.
- **Triggers:**
    - `TR_Auditoria_Ejecucion`: Registra cambios en los montos devengados para trazabilidad.
    - `TR_Validacion_Montos`: Impide la inserción de presupuestos negativos.
    - `TR_Historico_Institucion`: Guarda versiones anteriores de nombres de instituciones.

## 7. Dashboard y Visualización
Se desarrollaron dos soluciones de visualización:
1. **Dashboard HTML Interactivo:** Ubicado en `dashboard/Dashboard_PresupuestoNacionalRD.html`, permite una visualización rápida de KPIs (Inicial vs Vigente), análisis de prioridad por Función/Sub-Función y gráficos de variación presupuestaria.
2. **Power BI:** Ubicado en `powerbi/`, incluye un archivo unificado y una guía técnica para replicar el análisis de tendencias, mapas de calor y medidas DAX avanzadas.

## 8. Resumen de Activos Digitales
- **Resumen JSON:** `datos/resumen_dashboard.json` consolidando los 12.8 billones de pesos para acceso rápido.
- **CSV Unificado:** `powerbi/PresupuestoNacionalRD_PowerBI_Unificado.csv` con 246,000 registros enriquecidos.
- **Documentación:** Manuales de inicio rápido, notas de rendimiento y trazabilidad en la carpeta `docs/`.

## 9. Hallazgos Principales
- Se identificó que el presupuesto nacional consolidado (2017-2025) asciende a más de **RD$ 12.8 Trillones**, con una ejecución promedio superior al 88%.
- Las instituciones del Poder Ejecutivo concentran el grueso del presupuesto vigente.
- La ejecución muestra un crecimiento sostenido año tras año, pasando de ~860 mil millones en 2017 a más de 2 billones en 2025.

## 9. Uso de IA (Gemini CLI)
Este proyecto fue desarrollado siguiendo la **Guía de Configuración 2.0**, orquestado por **Gemini CLI**. Se utilizaron sub-agentes para la generación de scripts SQL, limpieza de datos y creación del dashboard, asegurando un estándar de calidad senior en toda la entrega.

## 10. Conclusiones
La estructura en estrella implementada permite una navegación fluida por los datos del presupuesto nacional. La integración de T-SQL avanzado y herramientas de visualización garantiza que el proyecto no sea solo un repositorio de datos, sino un sistema de soporte a la decisión efectivo.

## 11. Inventario de Archivos
- `sql/`: Scripts de base de datos.
- `datos/`: Datasets originales y limpios.
- `diagramas/`: Modelos Conceptual, Lógico y Físico (.mmd, .svg).
- `dashboard/`: Código fuente del tablero web.
- `powerbi/`: Recursos de BI.
- `documento/`: Este informe final.

---
**Lic. Manuel Mañana Santana**  
Maestría en Ciencias de Datos e IA, UASD.
[www.linkedin.com/in/manuelmañana](https://www.linkedin.com/in/manuelmañana)
