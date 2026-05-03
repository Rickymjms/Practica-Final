# Guion de Demo - Análisis del Presupuesto Nacional RD

Este guion sirve de apoyo para la presentación en vivo del proyecto final ante evaluadores o interesados.

## 1. Apertura
"Buenos días/tardes. Esta presentación muestra una solución integral de ingeniería de datos aplicada al **Presupuesto Nacional de la República Dominicana (2017-2025)**."

"El objetivo principal fue transformar datasets masivos y dispersos de la DIGEPRES en un ecosistema analítico robusto, utilizando un motor relacional de alto rendimiento (**SQL Server**) y visualizaciones interactivas."

## 2. Estructura y Trazabilidad del Proyecto
Mostrar la carpeta raíz del proyecto:
*   `datos/originales/`: Evidencia de las fuentes primarias.
*   `datos/limpios/`: Resultados del proceso de normalización.
*   `sql/`: Corazón de la lógica relacional y de negocio.
*   `diagramas/`: Modelado arquitectónico (Conceptual, Lógico y Físico).
*   `dashboard/`: Interfaz interactiva para toma de decisiones.

> *"Garantizamos la trazabilidad absoluta: los datos originales permanecen inalterados (read-only), mientras que las capas de limpieza y carga SQL aseguran que el motor trabaje con información íntegra y optimizada."*

## 3. El Modelo de Datos (Esquema en Estrella)
Abrir el archivo: `diagramas/03_modelo_fisico.svg` o el archivo Mermaid.
*   **Dimensiones:** Institución, Programa, Geografía, Objeto de Gasto y Tiempo.
*   **Tabla de Hechos:** `Fact_Ejecucion_Presupuestaria` (Centraliza las métricas de Presupuesto Inicial, Vigente y Devengado).

> *"Implementamos un Esquema en Estrella normalizado en 3FN, lo que nos permite realizar Joins de alta velocidad y soportar agregaciones sobre los 12.8 billones de pesos que componen el dataset."*

## 4. Implementación SQL Server
Ejecutar el Script Maestro o mostrar el archivo: `sql/05_script_maestro_completo_presupuesto_nacional.sql`.
*   Explique que el script orquesta el DDL (Estructura) y el DML (Carga de ~246,000 registros).

**Validación de Carga:**
Ejecutar: `sql/06_verificacion_demo_presupuesto_nacional.sql`.
*   Muestre los conteos de registros para confirmar que la base de datos es funcional.

## 5. Consultas Analíticas (DQL)
Abrir: `sql/03_dql_presupuesto_nacional.sql`.
*   Destaque ejemplos de: Agregaciones por Ministerio, Ranking de Provincias con mayor gasto, y el cálculo de la eficiencia del gasto (% Ejecución).

## 6. Lógica de Programación (SP y Triggers)
Muestre el archivo: `sql/04_programacion_sp_triggers_presupuesto_nacional.sql`.
*   **Stored Procedures:** Para inserciones controladas y reportes rápidos por año.
*   **Triggers:** Auditoría automática de cambios en montos devengados y validación de integridad (evitar montos negativos).

## 7. Visualización: Dashboard Interactivo
Abrir: `dashboard/Dashboard_PresupuestoNacionalRD.html`.
*   Muestre los **5 KPIs Principales** (Inicial vs Vigente).
*   Demuestre la utilidad de los filtros jerárquicos (**Función > Sub-Función**).
*   Destaque las tablas de **Prioridad de Gasto** (donde el estado pone el dinero vs áreas de menor presupuesto).

## 8. Conclusión y Hallazgos
"A través de este sistema, hemos logrado:"
1.  Unificar **Gasto Corriente** y **Aplicaciones Financieras**.
2.  Mapear la jerarquía funcional del estado dominicano de forma atómica.
3.  Proporcionar una herramienta que permite detectar variaciones presupuestarias críticas en tiempo real.

> *"En conclusión, este proyecto convierte datos abiertos gubernamentales en inteligencia financiera auditable y lista para la rendición de cuentas."*

---
**Autor:** Lic. Manuel Mañana Santana
**Fecha:** Mayo 2026
