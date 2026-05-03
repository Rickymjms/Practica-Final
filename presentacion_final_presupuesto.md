# Presentación Final: Presupuesto Nacional RD
**Autor:** Lic. Manuel Mañana Santana
**Institución:** Universidad Autónoma de Santo Domingo (UASD)
**Maestría:** Ciencias de Datos e Inteligencia Artificial

---

## Diapositiva 1: Portada
- **Título:** Análisis de la Ejecución Presupuestaria de la República Dominicana
- **Subtítulo:** Implementación de Almacén de Datos (Star Schema) en SQL Server
- **Presentado por:** Lic. Manuel Mañana Santana
- **Fecha:** Mayo 2026

---

## Diapositiva 2: Contexto y Objetivos
- **Problema:** Fragmentación de datos públicos y dificultad para auditar la inversión estatal en tiempo real.
- **Objetivo:** Construir una solución de BI robusta que permita analizar el presupuesto por institución, programa y ubicación geográfica.

---

## Diapositiva 3: El Dataset
- **Fuente:** Portal de Datos Abiertos de la República Dominicana (DIGEPRES).
- **Contenido:** Ejecución de gastos por institución, función y ubicación (2025).
- **Proceso ETL:** Limpieza de nulos, normalización de nombres y conversión de tipos financieros.

---

## Diapositiva 4: Modelo de Datos (Star Schema)
- **Tabla de Hechos:** `Fact_Ejecucion_Presupuestaria`.
- **Dimensiones:** `Dim_Institucion`, `Dim_Geografia`, `Dim_Programa`, `Dim_Objeto_Gasto`, `Dim_Tiempo`.
- **Normalización:** Cumplimiento estricto de la 3ra Forma Normal (3FN).

---

## Diapositiva 5: Implementación Técnica (SQL Server)
- **T-SQL Avanzado:** Uso de `IDENTITY`, `CHECK`, `UNIQUE` e Índices Clustered/Non-Clustered.
- **Vistas Analíticas:** Capa semántica para simplificar el acceso a Power BI.
- **Consultas DQL:** 25 consultas analíticas que extraen indicadores críticos.

---

## Diapositiva 6: Programación y Automatización
- **Stored Procedures:** Generación de resúmenes institucionales automáticos.
- **Triggers:** Auditoría de cambios financieros y validación de integridad de negocio.

---

## Diapositiva 7: Dashboard y Visualización
- **HTML Dashboard:** Vista rápida web interactiva.
- **Power BI:** Mapas de calor, KPIs de ejecución YTD y tendencias mensuales.

---

## Diapositiva 8: Hallazgos Principales
- **Eficiencia:** Identificación de ministerios con baja ejecución en el primer semestre.
- **Geografía:** Disparidad de inversión pública entre regiones del Cibao y el Sur.
- **Composición:** Análisis del peso de los gastos corrientes frente a la inversión de capital.

---

## Diapositiva 9: Conclusiones
- La arquitectura en estrella es ideal para la transparencia gubernamental.
- La integración de SQL Server con herramientas de BI potencia la toma de decisiones.
- El uso de Agentes de IA aceleró el proceso de ingeniería manteniendo altos estándares.

---

## Diapositiva 10: Gracias
- **Preguntas?**
- **Contacto:** Lic. Manuel Mañana Santana
- **LinkedIn:** www.linkedin.com/in/manuelmañana
