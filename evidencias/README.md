# Guía de Evidencias y Capturas de Pantalla

Para completar la entrega académica, el estudiante (Manuel) debe documentar el funcionamiento del sistema mediante capturas de pantalla organizadas.

## 📸 Checklist de Capturas Requeridas

### 1. Base de Datos en MySQL
- [ ] **Estructura de Tablas:** Captura del explorador de objetos mostrando todas las tablas (Fact y Dim).
- [ ] **Script DDL Exitoso:** Captura de la consola o log de salida tras ejecutar `01_DDL_PresupuestoNacionalRD.sql`.
- [ ] **Constraints:** Captura mostrando las llaves primarias y foráneas configuradas.

### 2. Carga y Consultas
- [ ] **Conteo de Registros:** Resultado de un `SELECT COUNT(*)` en la tabla `Fact_Ejecucion_Presupuestaria` (debe haber datos cargados).
- [ ] **Consultas Analíticas:** Al menos 5 capturas de resultados de las consultas incluidas en `03_DQL_25_Consultas_PresupuestoNacionalRD.sql`.
- [ ] **Uso de JOINs:** Una captura que muestre una consulta uniendo la tabla de hechos con al menos 2 dimensiones.

### 3. Programación (Stored Procedures & Triggers)
- [ ] **Ejecución de SP:** Resultado de llamar a un procedimiento almacenado (ej: `CALL SP_Resumen_Ejecucion()`).
- [ ] **Prueba de Trigger:** Captura de la tabla de auditoría después de realizar un `UPDATE` en un monto presupuestario.

### 4. Visualización (Power BI)
- [ ] **Vista de Modelo:** Captura del diagrama de relaciones en Power BI (Esquema en Estrella).
- [ ] **Dashboard Principal:** Vista general del reporte con los KPIs de Total Devengado y % de Ejecución.
- [ ] **Análisis Geográfico:** Captura del mapa interactivo funcionando.
- [ ] **Filtros Dinámicos:** Captura mostrando cómo cambian los datos al seleccionar un año o una institución específica.

## 📁 Instrucciones de Guardado
Guarde todas las imágenes en esta carpeta (`evidencias/`) con nombres descriptivos (ej: `01_tablas_mysql.png`, `02_dashboard_principal.png`).

---
**Preparado para:** Lic. Manuel Mañana Santana
