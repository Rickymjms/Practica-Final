# Documentación del Modelo de Datos (ERD)

Este documento describe la arquitectura del modelo de datos utilizado para el análisis del Presupuesto Nacional de la República Dominicana.

## 🌟 Arquitectura: Esquema en Estrella (Star Schema)

El proyecto utiliza un enfoque de modelado dimensional, ideal para entornos de Inteligencia de Negocios (BI). Esta estructura minimiza la complejidad de las consultas y optimiza el rendimiento para grandes volúmenes de datos financieros.

### 1. Tabla de Hechos (Fact Table)

*   **`Fact_Ejecucion_Presupuestaria`**: Es el núcleo del modelo. Almacena las transacciones financieras y las llaves foráneas que conectan con todas las dimensiones.
    *   *Métricas:* Monto_Vigente, Monto_Devengado, Monto_Pagado.
    *   *Llaves:* ID_Institucion, ID_Geografia, ID_Programa, ID_Objeto_Gasto, ID_Tiempo.

### 2. Dimensiones (Dimension Tables)

Las dimensiones proporcionan el contexto necesario para analizar las métricas de la tabla de hechos:

*   **`Dim_Institucion`**: Clasifica el gasto por la entidad responsable (Capítulos del Gobierno, Instituciones y Unidades Ejecutoras).
*   **`Dim_Geografia`**: Permite segmentar el presupuesto por ubicación física (Regiones, Provincias y Municipios).
*   **`Dim_Programa`**: Define la estructura presupuestaria por programas sociales, proyectos de inversión y actividades administrativas.
*   **`Dim_Objeto_Gasto`**: Clasifica el dinero según su naturaleza económica (Sueldos, Materiales, Maquinaria, Transferencias).
*   **`Dim_Tiempo`**: Facilita el análisis cronológico (Año, Mes, Trimestre, Semestre).

## 📊 Beneficios del Diseño

1.  **Simplicidad:** Las consultas SQL para generar reportes son más sencillas de escribir y entender.
2.  **Rendimiento:** Reduce el número de `JOINs` necesarios en comparación con un modelo altamente normalizado (copo de nieve).
3.  **Escalabilidad:** Es fácil añadir nuevas métricas o dimensiones sin alterar la estructura básica del modelo.
4.  **Integración con Power BI:** Power BI está optimizado nativamente para trabajar con esquemas en estrella, lo que resulta en dashboards más rápidos y dinámicos.

---
**Diseñado por:** Lic. Manuel Mañana Santana
