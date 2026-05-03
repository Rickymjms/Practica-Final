/*
 * Proyecto Final: Presupuesto Nacional RD
 * Autor: Lic. Manuel Mañana Santana
 *
 * Descripción: Script de Verificación de Carga de Datos para SQL Server.
 * Muestra el conteo de registros en cada tabla para validar el éxito del DML.
 * Aplicando nuevas normas de nomenclatura.
 */

USE PresupuestoNacionalRD;
GO

SELECT 'Resumen de Carga de Datos' AS 'Reporte';
GO

SELECT 'Institucion' AS Tabla, COUNT(*) AS Total FROM dbo.Institucion
UNION ALL
SELECT 'Programa', COUNT(*) FROM dbo.Programa
UNION ALL
SELECT 'ObjetoGasto', COUNT(*) FROM dbo.ObjetoGasto
UNION ALL
SELECT 'Tiempo', COUNT(*) FROM dbo.Tiempo
UNION ALL
SELECT 'Organismo', COUNT(*) FROM dbo.Organismo
UNION ALL
SELECT 'FuenteFinanciamiento', COUNT(*) FROM dbo.FuenteFinanciamiento
UNION ALL
SELECT 'Geografia', COUNT(*) FROM dbo.Geografia
UNION ALL
SELECT 'EjecucionPresupuestaria', COUNT(*) FROM dbo.EjecucionPresupuestaria;
GO

-- Mostrar una muestra de la tabla de hechos combinada con las nuevas dimensiones
SELECT TOP 10
    i.Institucion_Capitulo, 
    i.Institucion_TipoInstitucion,
    p.Programa_Nombre, 
    og.ObjetoGasto_Auxiliar, 
    f.EjecucionPresupuestaria_DevengadoAprobado,
    o.Organismo_Nombre,
    ff.FuenteFinanciamiento_Descripcion
FROM dbo.EjecucionPresupuestaria f
JOIN dbo.Institucion i ON f.EjecucionPresupuestaria_InstitucionID = i.Institucion_ID
JOIN dbo.Programa p ON f.EjecucionPresupuestaria_ProgramaID = p.Programa_ID
JOIN dbo.ObjetoGasto og ON f.EjecucionPresupuestaria_ObjetoGastoID = og.ObjetoGasto_ID
LEFT JOIN dbo.Organismo o ON i.Institucion_OrganismoID = o.Organismo_ID
LEFT JOIN dbo.FuenteFinanciamiento ff ON f.EjecucionPresupuestaria_FuenteFinanciamientoID = ff.FuenteFinanciamiento_ID;
GO
