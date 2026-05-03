# Trazabilidad de Datos (Data Lineage) - Presupuesto Nacional RD

Este documento describe el flujo de la información desde los datasets públicos originales hasta los activos finales (Base de Datos, Dashboard y Power BI).

## 1. Resumen del Flujo

```text
datos/originales/*.csv (DIGEPRES)
        |
        v
Limpieza, normalización y unificación (Python/Pandas)
        |
        v
datos/limpios/Dim_*.csv y Fact_*.csv
        |
        v
sql/02_dml_presupuesto_nacional.sql (Carga Real)
        |
        v
SQL Server Database: PresupuestoNacionalRD
        |
        +--> sql/03_dql_presupuesto_nacional.sql (25 Consultas)
        +--> dashboard/Dashboard_PresupuestoNacionalRD.html
        +--> powerbi/PresupuestoNacionalRD_PowerBI_Unificado.csv
```

## 2. Orígenes Originales

| Archivo Original | Significado de Negocio | Destino en el Modelo |
| --- | --- | --- |
| `ejecucion-de-los-gastos-por-institucion.csv` | Gasto detallado por estructura organizacional y programática (2017-2025). | `Fact_Ejecucion`, `Dim_Institucion`, `Dim_Programa`, `Dim_Tiempo` |
| `ejecucion-de-los-gastos-por-funcion.csv` | Gasto clasificado por finalidad y función de estado. | Mapeo funcional en `Dim_Programa` |
| `gastos institucionales por concepto.csv` | Clasificación económica del gasto y aplicaciones financieras (2024-2025). | `Fact_Ejecucion` (Apps Financieras), `Dim_Objeto_Gasto` |

## 3. Reglas de Transformación Aplicadas

| Regla | Descripción |
| --- | --- |
| Unificación de Tipos | Integración de registros de "Gasto" y "Aplicaciones Financieras" en una sola tabla de hechos. |
| Mapeo Jerárquico | Creación de jerarquías funcionales (Finalidad > Función > Sub-Función) basadas en descripciones de programas. |
| Normalización de Nombres | Limpieza de caracteres especiales (BOM) y estandarización de nombres de Ministerios y Capítulos. |
| Conversión de Escala | Los montos originales en RD$ se mantienen íntegros en SQL, pero se resumen en Millones (MM) para el Dashboard. |
| Claves Sustitutas | Generación de IDs enteros autoincrementales para optimizar los Joins en SQL Server. |

## 4. Salidas Derivadas

*   **Script Maestro:** Orquestación total del despliegue en un solo comando.
*   **Resumen JSON:** `datos/resumen_dashboard.json` para acceso rápido a KPIs globales.
*   **CSV Unificado:** Optimizado con 16 columnas para análisis multidimensional en Power BI.

---
**Autor:** Lic. Manuel Mañana Santana
**Proyecto:** Análisis del Presupuesto Nacional RD (2017-2025)
