# Diccionario de Datos: Presupuesto Nacional RD
**Autor:** Lic. Manuel Mañana Santana
**Fuente:** Dirección General de Presupuesto (DIGEPRES)

Este diccionario técnico define la estructura analítica utilizada para el análisis de la ejecución presupuestaria de la República Dominicana, siguiendo los estándares oficiales de clasificación.

## 📈 Tabla de Hechos: `Fact_Ejecucion_Presupuestaria`
Centraliza las métricas financieras vinculadas a las dimensiones descriptivas.

| Columna | Tipo de Dato | Descripción |
| --- | --- | --- |
| `ID_Ejecucion` | BIGINT (PK) | Identificador único de la línea de ejecución. |
| `ID_Institucion` | INT (FK) | Vínculo con la jerarquía institucional. |
| `ID_Geografia` | INT (FK) | Vínculo con la ubicación geográfica. |
| `ID_Programa` | INT (FK) | Vínculo con la estructura programática. |
| `ID_Objeto_Gasto` | INT (FK) | Vínculo con el clasificador del objeto de gasto. |
| `ID_Tiempo` | INT (FK) | Vínculo con el periodo fiscal. |
| `Presupuesto_Inicial` | MONEY | Monto aprobado por ley al inicio del año. |
| `Presupuesto_Vigente` | MONEY | Monto actual después de modificaciones y transferencias. |
| `Devengado_Aprobado` | MONEY | Monto cuya obligación de pago ha sido reconocida. |

## 🏢 Dimensión: `Dim_Institucion`
Contiene la clasificación institucional del sector público no financiero.

| Columna | Tipo de Dato | Descripción |
| --- | --- | --- |
| `ID_Institucion` | INT (PK) | Identificador de la entidad. |
| `Seccion_Institucional`| VARCHAR(255)| Categoría superior (Administración Central, Descentralizadas, etc.). |
| `Capitulo` | VARCHAR(255) | Ministerio o ente de máximo nivel. |
| `SubCapitulo` | VARCHAR(255) | Dependencia directa del capítulo. |
| `Unidad_Ejecutora` | VARCHAR(255) | Entidad específica responsable de ejecutar los fondos. |

## 📍 Dimensión: `Dim_Geografia`
Jerarquía de ubicación de la inversión y el gasto.

| Columna | Tipo de Dato | Descripción |
| --- | --- | --- |
| `ID_Geografia` | INT (PK) | Identificador de ubicación. |
| `Region` | VARCHAR(100) | Macro-regiones oficiales (Cibao Norte, Sur, etc.). |
| `Provincia` | VARCHAR(100) | División política de segundo nivel. |
| `Municipio` | VARCHAR(100) | División política de tercer nivel. |

## 🛠️ Dimensión: `Dim_Programa`
Clasificación funcional y programática del gasto.

| Columna | Tipo de Dato | Descripción |
| --- | --- | --- |
| `ID_Programa` | INT (PK) | Identificador del programa. |
| `Finalidad` | VARCHAR(100) | Propósito macro (Servicios Sociales, Económicos, etc.). |
| `Funcion` | VARCHAR(100) | Función específica dentro de la finalidad. |
| `Programa` | VARCHAR(255) | Nombre del programa presupuestario. |
| `Actividad_Obra` | VARCHAR(255) | Tarea o infraestructura específica. |

## 💰 Dimensión: `Dim_Objeto_Gasto`
Detalle técnico de qué se está comprando o pagando.

| Columna | Tipo de Dato | Descripción |
| --- | --- | --- |
| `ID_Objeto_Gasto` | INT (PK) | Identificador del objeto de gasto. |
| `Tipo_Presupuesto` | VARCHAR(50) | Clasifica entre "Gasto" y "Aplicación Financiera". |
| `Fuente_Financiamiento`| VARCHAR(100)| Origen de los fondos (Interna, Externa, Propios). |
| `Concepto` | VARCHAR(255) | Agrupación técnica (Remuneraciones, Obras, etc.). |
| `Detalle_Gasto` | VARCHAR(255) | Descripción atómica del insumo o servicio. |

## 📅 Dimensión: `Dim_Tiempo`
| Columna | Tipo de Dato | Descripción |
| --- | --- | --- |
| `ID_Tiempo` | INT (PK) | Identificador temporal. |
| `Periodo_Anio` | INT | Año fiscal (2017-2025). |
| `Mes_Imputacion` | INT | Número del mes (1-12). |
| `Nombre_Mes` | VARCHAR(20) | Nombre del mes en español e inglés (vía UI). |

---
**Documento mantenido por:** Lic. Manuel Mañana Santana
**Estatus:** Validado contra Diccionario de Datos DIGEPRES.
