# Diccionario de Datos: Presupuesto Nacional RD
**Autor:** Lic. Manuel Mañana Santana
**Fuente:** Dirección General de Presupuesto (DIGEPRES)

Este diccionario técnico define la estructura analítica utilizada para el análisis de la ejecución presupuestaria de la República Dominicana, sincronizado con la implementación física en SQL Server.

## 📈 Tabla de Hechos: `EjecucionPresupuestaria`
Centraliza las métricas financieras vinculadas a las dimensiones descriptivas.

| Columna | Tipo de Dato | Descripción |
| --- | --- | --- |
| `EjecucionPresupuestaria_ID` | INT (PK) | Identificador único (IDENTITY). |
| `EjecucionPresupuestaria_InstitucionID` | INT (FK) | Vínculo con la dimensión Institución. |
| `EjecucionPresupuestaria_ProgramaID` | INT (FK) | Vínculo con la dimensión Programa. |
| `EjecucionPresupuestaria_ObjetoGastoID` | INT (FK) | Vínculo con la dimensión ObjetoGasto. |
| `EjecucionPresupuestaria_PeriodoID` | INT (FK) | Vínculo con la dimensión Periodo. |
| `EjecucionPresupuestaria_FuenteFinanciamientoID` | INT (FK) | Vínculo con la dimensión FuenteFinanciamiento. |
| `EjecucionPresupuestaria_ProvinciaID` | INT (FK) | Vínculo con la dimensión Provincia (Geografía). |
| `EjecucionPresupuestaria_PresupuestoInicial` | DECIMAL(18,2) | Monto aprobado por ley al inicio del año. |
| `EjecucionPresupuestaria_PresupuestoVigente` | DECIMAL(18,2) | Monto actual después de modificaciones. |
| `EjecucionPresupuestaria_DevengadoAprobado` | DECIMAL(18,2) | Monto cuya obligación de pago ha sido reconocida. |

## 🏛️ Dimensión: `Organismo`
Nivel superior de agrupación institucional.

| Columna | Tipo de Dato | Descripción |
| --- | --- | --- |
| `Organismo_ID` | INT (PK) | Identificador único. |
| `Organismo_Codigo` | VARCHAR(10) | Código oficial del organismo. |
| `Organismo_Nombre` | VARCHAR(255) | Nombre (Poder Ejecutivo, Legislativo, etc.). |

## 🏢 Dimensión: `Institucion`
Contiene la clasificación institucional detallada.

| Columna | Tipo de Dato | Descripción |
| --- | --- | --- |
| `Institucion_ID` | INT (PK) | Identificador único. |
| `Institucion_OrganismoID` | INT (FK) | Relación con la tabla Organismo. |
| `Institucion_CodigoCapitulo` | VARCHAR(10) | Código del Capítulo. |
| `Institucion_Capitulo` | VARCHAR(255) | Nombre del Ministerio o Ente. |
| `Institucion_UnidadEjecutora` | VARCHAR(255) | Entidad específica responsable de los fondos. |
| `Institucion_TipoInstitucion` | VARCHAR(100) | Clasificación (Gobierno Central, Descentralizada, etc.). |

## 📍 Dimensión: `Geografía (Pais, Region, Provincia)`
Jerarquía normalizada de ubicación.

| Tabla | Columna | Descripción |
| --- | --- | --- |
| `Pais` | `Pais_Nombre` | República Dominicana (u otros). |
| `Region` | `Region_Nombre` | Macro-regiones (Cibao, Sur, Este, etc.). |
| `Provincia` | `Provincia_Nombre` | Provincias y Distrito Nacional. |

## 🛠️ Dimensión: `Programa`
Clasificación funcional y programática del gasto.

| Columna | Tipo de Dato | Descripción |
| --- | --- | --- |
| `Programa_ID` | INT (PK) | Identificador único. |
| `Programa_CodigoPrograma` | VARCHAR(20) | Código del Programa Presupuestario. |
| `Programa_Nombre` | VARCHAR(255) | Descripción del Programa. |
| `Programa_Actividad` | VARCHAR(255) | Actividad o tarea específica. |

## 💰 Dimensión: `ObjetoGasto`
Detalle económico de la naturaleza del gasto.

| Columna | Tipo de Dato | Descripción |
| --- | --- | --- |
| `ObjetoGasto_ID` | INT (PK) | Identificador único. |
| `ObjetoGasto_Tipo` | VARCHAR(100) | Clasificación macro (Sueldos, Obras, etc.). |
| `ObjetoGasto_Concepto` | VARCHAR(100) | Agrupación técnica. |
| `ObjetoGasto_Auxiliar` | VARCHAR(255) | Descripción atómica del gasto. |

## 📅 Dimensión: `Periodo`
| Columna | Tipo de Dato | Descripción |
| --- | --- | --- |
| `Periodo_ID` | INT (PK) | Identificador único. |
| `Periodo_Anio` | INT | Año fiscal (2017-2025). |
| `Periodo_Mes` | INT | Número del mes (1-12). |
| `Periodo_NombreMes` | VARCHAR(20) | Nombre del mes en español. |

## 💳 Dimensión: `FuenteFinanciamiento`
| Columna | Tipo de Dato | Descripción |
| --- | --- | --- |
| `FuenteFinanciamiento_ID` | INT (PK) | Identificador único. |
| `FuenteFinanciamiento_Codigo` | VARCHAR(10) | Código de la fuente. |
| `FuenteFinanciamiento_Descripcion` | VARCHAR(255) | Tesoro Nacional, Crédito Externo, etc. |

---
**Documento mantenido por:** Lic. Manuel Mañana Santana
**Estatus:** Sincronizado con DDL v2.0.
