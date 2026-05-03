# Documentación del Modelo de Datos (ERD)

Este documento describe la arquitectura del modelo de datos utilizado para el análisis del Presupuesto Nacional de la República Dominicana.

## 🌟 Arquitectura: Esquema en Estrella / Copo de Nieve (Hybrid Schema)

El proyecto utiliza un enfoque de modelado dimensional, ideal para entornos de Inteligencia de Negocios (BI). El modelo ha sido expandido para incluir niveles jerárquicos más profundos (Organismos y Geografía normalizada).

### 1. Tabla de Hechos (Fact Table)

*   **`EjecucionPresupuestaria`**: Es el núcleo del modelo. Almacena las transacciones financieras y las llaves foráneas que conectan con todas las dimensiones.
    *   *Métricas:* `EjecucionPresupuestaria_PresupuestoInicial`, `EjecucionPresupuestaria_PresupuestoVigente`, `EjecucionPresupuestaria_DevengadoAprobado`.
    *   *Llaves Foráneas:* Institucion_ID, Programa_ID, ObjetoGasto_ID, Periodo_ID, FuenteFinanciamiento_ID, Provincia_ID.

### 2. Dimensiones (Dimension Tables)

Las dimensiones proporcionan el contexto necesario para analizar las métricas de la tabla de hechos:

*   **`Organismo`**: (Nueva) Nivel superior que agrupa a las instituciones (Poder Ejecutivo, Poder Legislativo, etc.).
*   **`Institucion`**: Clasifica el gasto por la entidad responsable (Capítulos del Gobierno, Instituciones y Unidades Ejecutoras).
*   **`Geografía (País -> Región -> Provincia)`**: Jerarquía normalizada para segmentar el presupuesto por ubicación física según la planificación nacional.
*   **`Programa`**: Define la estructura presupuestaria por programas sociales, proyectos de inversión y actividades administrativas.
*   **`ObjetoGasto`**: Clasifica el dinero según su naturaleza económica (Sueldos, Materiales, Maquinaria, Transferencias).
*   **`Periodo`**: Facilita el análisis cronológico por año y mes.
*   **`FuenteFinanciamiento`**: (Nueva) Identifica el origen de los fondos (Recursos Propios, Crédito Externo, Tesoro Nacional, etc.).

## 📊 Beneficios del Diseño

1.  **Trazabilidad:** La inclusión de Organismos y Fuentes de Financiamiento permite un análisis más detallado exigido por las normas de transparencia.
2.  **Rendimiento:** Índices optimizados en la tabla de hechos para mejorar el tiempo de respuesta en consultas de agregación.
3.  **Normalización Geográfica:** Permite reportes agregados por Región o País sin redundancia de datos.
4.  **Integración con Power BI:** El modelo sigue las mejores prácticas de modelado dimensional para herramientas de BI modernos.

---
**Diseñado por:** Lic. Manuel Mañana Santana
