# Notas de Rendimiento - Presupuesto Nacional RD

Este documento detalla las decisiones de diseño orientadas a la optimización del rendimiento en la base de datos de Presupuesto Nacional.

## 1. Objetivos de Rendimiento

La base de datos está diseñada para responder de manera eficiente a:
*   Consultas analíticas por Año Fiscal (2017-2025).
*   Agregaciones masivas sobre 12.8 billones de pesos dominicanos.
*   Filtrado jerárquico por estructura funcional y organizacional.
*   Soporte para reportes de BI de alta concurrencia.

## 2. Estrategia de Modelado

Se implementó un **Esquema en Estrella (Star Schema)**:
*   **Hechos Atómicos:** La tabla `Fact_Ejecucion_Presupuestaria` almacena las métricas monetarias en su nivel más bajo de detalle.
*   **Normalización 3FN:** Las dimensiones reducen la redundancia de texto (ej. nombres de ministerios se guardan una vez).
*   **Integridad:** El uso de claves foráneas asegura que no existan huérfanos, optimizando el motor de ejecución de Joins de SQL Server.

## 3. Optimización mediante Índices

Se crearon índices estratégicos en la tabla de hechos (~246k registros):

| Índice | Propósito |
| --- | --- |
| `IDX_Fact_Institucion` | Acelera el filtrado por Ministerios y Capítulos. |
| `IDX_Fact_Tiempo` | Optimiza las comparaciones anuales y mensuales. |
| `IDX_Fact_Geografia` | Mejora el rendimiento de reportes por Provincias y Municipios. |
| `IDX_ObjGasto_Codigos`| Acelera la búsqueda por tipo de presupuesto (Gasto vs Apps). |

## 4. Vistas Analíticas (Materialización Lógica)

Se incluyeron vistas que pre-calculan lógica compleja:
*   `View_Resumen_Institucion_Anio`: Calcula el % de ejecución dinámicamente.
*   `View_Distribucion_Geografica`: Centraliza los totales por región para mapas.

## 5. Escalabilidad

Aunque el volumen actual es de ~246,000 registros, la arquitectura soporta crecimiento mediante:
*   **Particionamiento:** Recomendado si el histórico supera los 10 años.
*   **Compresión de Datos:** Útil para las columnas de moneda en la tabla de hechos.
*   **Filtrado por ID:** El dashboard y Power BI filtran por llaves enteras (PK/FK), lo cual es más rápido que filtrar por cadenas de texto.

---
**Autor:** Lic. Manuel Mañana Santana
**Estatus:** Validado para carga de datos reales (Mayo 2026).
