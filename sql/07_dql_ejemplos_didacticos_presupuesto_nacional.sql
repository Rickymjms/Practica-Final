/*
 * Proyecto Final: Presupuesto Nacional RD
 * Autor: Lic. Manuel Mañana Santana
 *
 * Descripción: Consultas DQL Didácticas para SQL Server.
 * Ejemplos sencillos para estudiantes de Base de Datos I.
 * Aplicando nuevas normas de nomenclatura.
 */

USE PresupuestoNacionalRD;
GO

-- 1. Selección simple: Ver los primeros 10 programas
SELECT TOP 10 * FROM dbo.Programa;
GO

-- 2. Selección con filtro: Ver solo el Tipo de Institución 'Poder Ejecutivo'
SELECT * FROM dbo.Institucion WHERE Institucion_TipoInstitucion = 'Poder Ejecutivo';
GO

-- 3. Uso de Alias: Cambiar nombres de columnas para el reporte
SELECT Institucion_Capitulo AS [Nombre Institución], Institucion_UnidadEjecutora AS [Unidad] FROM dbo.Institucion;
GO

-- 4. Ordenamiento: Listar meses en orden inverso
SELECT * FROM dbo.Tiempo ORDER BY Tiempo_Mes DESC;
GO

-- 5. Agregación básica: ¿Cuánto es el presupuesto inicial total?
SELECT SUM(EjecucionPresupuestaria_PresupuestoInicial) AS [Presupuesto Total RD] FROM dbo.EjecucionPresupuestaria;
GO

-- 6. Promedio: Monto promedio devengado por transacción
SELECT AVG(EjecucionPresupuestaria_DevengadoAprobado) AS [Promedio Gasto] FROM dbo.EjecucionPresupuestaria;
GO

-- 7. Conteo: ¿Cuántos programas existen?
SELECT COUNT(*) AS [Total Programas] FROM dbo.Programa;
GO

-- 8. Join Básico: Ver ejecución con nombre de institución
SELECT i.Institucion_Capitulo, f.EjecucionPresupuestaria_DevengadoAprobado 
FROM dbo.EjecucionPresupuestaria f
JOIN dbo.Institucion i ON f.EjecucionPresupuestaria_InstitucionID = i.Institucion_ID;
GO

-- 9. Agrupar por: Gasto total por Institución
SELECT i.Institucion_Capitulo, SUM(f.EjecucionPresupuestaria_DevengadoAprobado) AS [Total Gastado]
FROM dbo.EjecucionPresupuestaria f
JOIN dbo.Institucion i ON f.EjecucionPresupuestaria_InstitucionID = i.Institucion_ID
GROUP BY i.Institucion_Capitulo;
GO

-- 10. Filtro en agrupamiento (HAVING): Instituciones con más de 100 millones gastados
SELECT i.Institucion_Capitulo, SUM(f.EjecucionPresupuestaria_DevengadoAprobado) AS [Total]
FROM dbo.EjecucionPresupuestaria f
JOIN dbo.Institucion i ON f.EjecucionPresupuestaria_InstitucionID = i.Institucion_ID
GROUP BY i.Institucion_Capitulo
HAVING SUM(f.EjecucionPresupuestaria_DevengadoAprobado) > 100000000;
GO

-- 11. Búsqueda de texto (LIKE): Programas de Educación
SELECT * FROM dbo.Programa WHERE Programa_Nombre LIKE '%educacion%';
GO

-- 12. Valores Únicos: ¿Qué tipos de instituciones hay?
SELECT DISTINCT Institucion_TipoInstitucion FROM dbo.Institucion;
GO

-- 13. Mínimo y Máximo: Rango de presupuestos vigentes
SELECT MIN(EjecucionPresupuestaria_PresupuestoVigente) AS [Menor], MAX(EjecucionPresupuestaria_PresupuestoVigente) AS [Mayor] FROM dbo.EjecucionPresupuestaria;
GO

-- 14. Uso de BETWEEN: Ejecuciones en los meses de Enero a Marzo
SELECT * FROM dbo.Tiempo WHERE Tiempo_Mes BETWEEN 1 AND 3;
GO

-- 15. Combinación de múltiples tablas (JOIN): Reporte Ejecutivo
SELECT TOP 100
    i.Institucion_Capitulo, 
    i.Institucion_TipoInstitucion,
    t.Tiempo_NombreMes, 
    f.EjecucionPresupuestaria_DevengadoAprobado
FROM dbo.EjecucionPresupuestaria f
JOIN dbo.Institucion i ON f.EjecucionPresupuestaria_InstitucionID = i.Institucion_ID
JOIN dbo.Tiempo t ON f.EjecucionPresupuestaria_TiempoID = t.Tiempo_ID;
GO
