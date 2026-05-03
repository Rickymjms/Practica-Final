# Guía Técnica para Power BI: Análisis del Presupuesto Nacional RD

Esta guía describe el procedimiento para replicar el análisis avanzado de ejecución presupuestaria en Power BI, alineado con las métricas y visualizaciones del dashboard interactivo `Dashboard_PresupuestoNacionalRD.html`.

## 📂 Origen de Datos Recomendado

Para una carga rápida y consistente con el dashboard, utilice el archivo unificado:
*   **Ruta:** `powerbi/PresupuestoNacionalRD_PowerBI_Unificado.csv`
*   **Contenido:** 246,000+ registros que integran Gastos y Aplicaciones Financieras (2017-2025).

## 🛠️ Configuración de Columnas y Tipos

Asegúrese de configurar los siguientes tipos de datos tras la importación:
*   **Tiempo_Anio:** Número entero (No resumir).
*   **EjecucionPresupuestaria_PresupuestoInicial, EjecucionPresupuestaria_PresupuestoVigente, EjecucionPresupuestaria_DevengadoAprobado:** Moneda (RD$).
*   **Seccion_Institucional, Finalidad, Funcion, Sub_Funcion:** Texto / Categoría.

## 📊 Medidas DAX Esenciales (KPIs)

Cree las siguientes medidas para habilitar el análisis de prioridad y variación:

```DAX
-- 1. Totales Base
Total Inicial = SUM('PresupuestoNacionalRD'[EjecucionPresupuestaria_PresupuestoInicial])
Total Vigente = SUM('PresupuestoNacionalRD'[EjecucionPresupuestaria_PresupuestoVigente])
Total Devengado = SUM('PresupuestoNacionalRD'[EjecucionPresupuestaria_DevengadoAprobado])

-- 2. Análisis de Eficiencia
% Ejecución = DIVIDE([Total Devengado], [Total Vigente], 0)

-- 3. Análisis de Variación (Modificaciones Presupuestarias)
Variación Absoluta = [Total Vigente] - [Total Inicial]
% Variación = DIVIDE([Variación Absoluta], [Total Inicial], 0)

-- 4. Etiqueta Dinámica de Variación
Estado Variación = IF([Variación Absoluta] >= 0, "Aumento Presupuestario", "Disminución Presupuestaria")
```

## 🖼️ Estructura del Reporte (Sugerida)

Para mantener la paridad con el Dashboard HTML, organice su reporte en:

### 1. Panel de Filtros (Slicers)
*   **Año Fiscal:** `Tiempo_Anio` (Lista o Menú desplegable).
*   **Sección:** `Seccion_Institucional`.
*   **Jerarquía Funcional:** `Finalidad` > `Funcion` > `Sub_Funcion`.
*   **Jerarquía Organizacional:** `Institucion_Capitulo` > `Institucion_SubCapitulo`.

### 2. Tarjetas de Indicadores (KPIs)
*   Incluya 5 tarjetas principales: **Inicial**, **Vigente**, **Devengado**, **% Ejecución** y **Variación Absoluta**.

### 3. Visualizaciones de Prioridad (Tablas y Gráficos)
*   **Top 10 Prioridad Alta:** Tabla con `Funcion`, `Sub_Funcion` y `[Total Vigente]`, ordenada de mayor a menor.
*   **Análisis de Distribución:** Gráfico de columnas apiladas con Eje: `Funcion`, Leyenda: `Sub_Funcion`, Valores: `[Total Vigente]`.
*   **Gráficos de Variación:** Dos gráficos de barras horizontales mostrando el **Top 5 Aumentos** y **Top 5 Disminuciones** por `Institucion_Capitulo`.

## 🔗 Consistencia con el Dashboard HTML
El archivo `dashboard/Dashboard_PresupuestoNacionalRD.html` utiliza los mismos cálculos de esta guía. Si las sumas en Power BI difieren, verifique que el filtro de **Tipo de Presupuesto** esté considerando tanto "Gasto" como "Aplicaciones Financieras" según el análisis deseado.

---
**Autor:** Lic. Manuel Mañana Santana
**Estatus:** Versión 3.0 - Sincronizada con Dashboard Final.
