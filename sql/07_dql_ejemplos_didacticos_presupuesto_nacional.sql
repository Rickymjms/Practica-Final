/*
 * Proyecto Final: Presupuesto Nacional RD
 * Autor: Lic. Manuel Mañana Santana
 *
 * Descripción: Consultas DQL Didácticas para SQL Server.
 * Ejemplos sencillos para estudiantes de Base de Datos I.
 */

USE PresupuestoNacionalRD;
GO

-- 1. Selección simple: Ver los primeros 10 programas
SELECT TOP 10 * FROM dbo.Dim_Programa;
GO

-- 2. Selección con filtro: Ver solo el Tipo de Institución 'Poder Ejecutivo'
SELECT * FROM dbo.Dim_Institucion WHERE Tipo_Institucion = 'Poder Ejecutivo';
GO

-- 3. Uso de Alias: Cambiar nombres de columnas para el reporte
SELECT Capitulo AS [Nombre Institución], Unidad_Ejecutora AS [Unidad] FROM dbo.Dim_Institucion;
GO

-- 4. Ordenamiento: Listar meses en orden inverso
SELECT * FROM dbo.Dim_Tiempo ORDER BY Mes_Imputacion DESC;
GO

-- 5. Agregación básica: ¿Cuánto es el presupuesto inicial total?
SELECT SUM(Presupuesto_Inicial) AS [Presupuesto Total RD] FROM dbo.Fact_Ejecucion_Presupuestaria;
GO

-- 6. Promedio: Monto promedio devengado por transacción
SELECT AVG(Devengado_Aprobado) AS [Promedio Gasto] FROM dbo.Fact_Ejecucion_Presupuestaria;
GO

-- 7. Conteo: ¿Cuántos programas existen?
SELECT COUNT(*) AS [Total Programas] FROM dbo.Dim_Programa;
GO

-- 8. Join Básico: Ver ejecución con nombre de institución
SELECT i.Capitulo, f.Devengado_Aprobado 
FROM dbo.Fact_Ejecucion_Presupuestaria f
JOIN dbo.Dim_Institucion i ON f.ID_Institucion = i.ID_Institucion;
GO

-- 9. Agrupar por: Gasto total por Institución
SELECT i.Capitulo, SUM(f.Devengado_Aprobado) AS [Total Gastado]
FROM dbo.Fact_Ejecucion_Presupuestaria f
JOIN dbo.Dim_Institucion i ON f.ID_Institucion = i.ID_Institucion
GROUP BY i.Capitulo;
GO

-- 10. Filtro en agrupamiento (HAVING): Instituciones con más de 100 millones gastados
SELECT i.Capitulo, SUM(f.Devengado_Aprobado) AS [Total]
FROM dbo.Fact_Ejecucion_Presupuestaria f
JOIN dbo.Dim_Institucion i ON f.ID_Institucion = i.ID_Institucion
GROUP BY i.Capitulo
HAVING SUM(f.Devengado_Aprobado) > 100000000;
GO

-- 11. Búsqueda de texto (LIKE): Programas de Educación
SELECT * FROM dbo.Dim_Programa WHERE Programa LIKE '%educacion%';
GO

-- 12. Valores Únicos: ¿Qué tipos de instituciones hay?
SELECT DISTINCT Tipo_Institucion FROM dbo.Dim_Institucion;
GO

-- 13. Mínimo y Máximo: Rango de presupuestos vigentes
SELECT MIN(Presupuesto_Vigente) AS [Menor], MAX(Presupuesto_Vigente) AS [Mayor] FROM dbo.Fact_Ejecucion_Presupuestaria;
GO

-- 14. Uso de BETWEEN: Ejecuciones en los meses de Enero a Marzo
SELECT * FROM dbo.Dim_Tiempo WHERE Mes_Imputacion BETWEEN 1 AND 3;
GO

-- 15. Combinación de múltiples tablas (JOIN): Reporte Ejecutivo
SELECT TOP 100
    i.Capitulo, 
    i.Tipo_Institucion,
    t.Nombre_Mes, 
    f.Devengado_Aprobado
FROM dbo.Fact_Ejecucion_Presupuestaria f
JOIN dbo.Dim_Institucion i ON f.ID_Institucion = i.ID_Institucion
JOIN dbo.Dim_Tiempo t ON f.ID_Tiempo = t.ID_Tiempo;
GO
