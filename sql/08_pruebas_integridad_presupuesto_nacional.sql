/*
 * Proyecto Final: Presupuesto Nacional RD
 * Autor: Lic. Manuel Mañana Santana
 *
 * Descripción: Pruebas de Integridad de Datos para SQL Server.
 * Detecta valores nulos, huérfanos y datos inconsistentes.
 * Aplicando nuevas normas de nomenclatura.
 */

USE PresupuestoNacionalRD;
GO

-- 1. Verificar Nulos en Claves Primarias
SELECT 'Buscando PKs nulas en Institucion...' AS Test;
SELECT * FROM dbo.Institucion WHERE Institucion_ID IS NULL;

SELECT 'Buscando PKs nulas en EjecucionPresupuestaria...' AS Test;
SELECT * FROM dbo.EjecucionPresupuestaria WHERE EjecucionPresupuestaria_ID IS NULL;
GO

-- 2. Verificar Registros Huérfanos (Integridad Referencial)
SELECT 'Buscando ejecuciones sin institución válida...' AS Test;
SELECT f.* FROM dbo.EjecucionPresupuestaria f
LEFT JOIN dbo.Institucion i ON f.EjecucionPresupuestaria_InstitucionID = i.Institucion_ID
WHERE i.Institucion_ID IS NULL;

SELECT 'Buscando ejecuciones sin tiempo válido...' AS Test;
SELECT f.* FROM dbo.EjecucionPresupuestaria f
LEFT JOIN dbo.Tiempo t ON f.EjecucionPresupuestaria_TiempoID = t.Tiempo_ID
WHERE t.Tiempo_ID IS NULL;
GO

-- 3. Verificar Inconsistencias Numéricas
SELECT 'Buscando montos negativos en presupuestos...' AS Test;
SELECT * FROM dbo.EjecucionPresupuestaria 
WHERE EjecucionPresupuestaria_PresupuestoInicial < 0 
   OR EjecucionPresupuestaria_PresupuestoVigente < 0 
   OR EjecucionPresupuestaria_DevengadoAprobado < 0;

SELECT 'Buscando devengado mayor que presupuesto vigente (Alerta)...' AS Test;
SELECT * FROM dbo.EjecucionPresupuestaria 
WHERE EjecucionPresupuestaria_DevengadoAprobado > EjecucionPresupuestaria_PresupuestoVigente;
GO

-- 4. Verificar Duplicados en Dimensiones (Basado en códigos de negocio)
SELECT 'Buscando códigos de institución duplicados...' AS Test;
SELECT Institucion_CodigoCapitulo, Institucion_CodigoSubCapitulo, Institucion_CodigoUnidadEjecutora, COUNT(*) 
FROM dbo.Institucion 
GROUP BY Institucion_CodigoCapitulo, Institucion_CodigoSubCapitulo, Institucion_CodigoUnidadEjecutora 
HAVING COUNT(*) > 1;
GO

SELECT 'Pruebas de integridad finalizadas.' AS Mensaje;
GO
