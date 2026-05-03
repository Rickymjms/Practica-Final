/*
 * Proyecto Final: Presupuesto Nacional RD
 * Autor: Lic. Manuel Mañana Santana
 *
 * Descripción: Script de Verificación de Carga de Datos para SQL Server.
 * Muestra el conteo de registros en cada tabla para validar el éxito del DML.
 */

USE PresupuestoNacionalRD;
GO

SELECT 'Resumen de Carga de Datos' AS 'Reporte';
GO

SELECT 'Dim_Institucion' AS Tabla, COUNT(*) AS Total FROM dbo.Dim_Institucion
UNION ALL
SELECT 'Dim_Programa', COUNT(*) FROM dbo.Dim_Programa
UNION ALL
SELECT 'Dim_Objeto_Gasto', COUNT(*) FROM dbo.Dim_Objeto_Gasto
UNION ALL
SELECT 'Dim_Tiempo', COUNT(*) FROM dbo.Dim_Tiempo
UNION ALL
SELECT 'Fact_Ejecucion_Presupuestaria', COUNT(*) FROM dbo.Fact_Ejecucion_Presupuestaria;
GO

-- Mostrar una muestra de la tabla de hechos combinada
SELECT TOP 10
    i.Capitulo, 
    i.Tipo_Institucion,
    p.Programa, 
    og.Auxiliar, 
    f.Devengado_Aprobado
FROM dbo.Fact_Ejecucion_Presupuestaria f
JOIN dbo.Dim_Institucion i ON f.ID_Institucion = i.ID_Institucion
JOIN dbo.Dim_Programa p ON f.ID_Programa = p.ID_Programa
JOIN dbo.Dim_Objeto_Gasto og ON f.ID_Objeto_Gasto = og.ID_Objeto_Gasto;
GO
