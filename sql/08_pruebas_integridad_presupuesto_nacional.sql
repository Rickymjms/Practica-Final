/*
 * Proyecto Final: Presupuesto Nacional RD
 * Autor: Lic. Manuel Mañana Santana
 *
 * Descripción: Pruebas de Integridad de Datos para SQL Server.
 * Detecta valores nulos, huérfanos y datos inconsistentes.
 */

USE PresupuestoNacionalRD;
GO

-- 1. Verificar Nulos en Claves Primarias
SELECT 'Buscando PKs nulas en Dim_Institucion...' AS Test;
SELECT * FROM dbo.Dim_Institucion WHERE ID_Institucion IS NULL;

SELECT 'Buscando PKs nulas en Fact_Ejecucion...' AS Test;
SELECT * FROM dbo.Fact_Ejecucion_Presupuestaria WHERE ID_Ejecucion IS NULL;
GO

-- 2. Verificar Registros Huérfanos (Integridad Referencial)
SELECT 'Buscando ejecuciones sin institución válida...' AS Test;
SELECT f.* FROM dbo.Fact_Ejecucion_Presupuestaria f
LEFT JOIN dbo.Dim_Institucion i ON f.ID_Institucion = i.ID_Institucion
WHERE i.ID_Institucion IS NULL;

SELECT 'Buscando ejecuciones sin tiempo válido...' AS Test;
SELECT f.* FROM dbo.Fact_Ejecucion_Presupuestaria f
LEFT JOIN dbo.Dim_Tiempo t ON f.ID_Tiempo = t.ID_Tiempo
WHERE t.ID_Tiempo IS NULL;
GO

-- 3. Verificar Inconsistencias Numéricas
SELECT 'Buscando montos negativos en presupuestos...' AS Test;
SELECT * FROM dbo.Fact_Ejecucion_Presupuestaria 
WHERE Presupuesto_Inicial < 0 OR Presupuesto_Vigente < 0 OR Devengado_Aprobado < 0;

SELECT 'Buscando devengado mayor que presupuesto vigente (Alerta)...' AS Test;
SELECT * FROM dbo.Fact_Ejecucion_Presupuestaria 
WHERE Devengado_Aprobado > Presupuesto_Vigente;
GO

-- 4. Verificar Duplicados en Dimensiones (Basado en códigos de negocio)
SELECT 'Buscando códigos de institución duplicados...' AS Test;
SELECT Cod_Capitulo, Cod_SubCapitulo, Cod_Unidad_Ejecutora, COUNT(*) 
FROM dbo.Dim_Institucion 
GROUP BY Cod_Capitulo, Cod_SubCapitulo, Cod_Unidad_Ejecutora 
HAVING COUNT(*) > 1;
GO

SELECT 'Pruebas de integridad finalizadas.' AS Mensaje;
GO
