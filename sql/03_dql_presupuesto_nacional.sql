/*
 * Proyecto Final: Presupuesto Nacional RD
 * Autor: Lic. Manuel Mañana Santana
 * LinkedIn: www.linkedin.com/in/manuelmañana
 *
 * Descripción: Script de Consultas (DQL) para SQL Server.
 * Contiene 25 consultas SQL que van de nivel básico a avanzado.
 * Aplicando nuevas normas de nomenclatura.
 */

USE PresupuestoNacionalRD;
GO

-- 1. Listar todas las instituciones registradas (Primeras 100)
SELECT TOP 100 * FROM dbo.Institucion;
GO

-- 2. Mostrar los nombres de los capítulos y subcapítulos sin duplicados
SELECT DISTINCT Institucion_Capitulo, Institucion_SubCapitulo FROM dbo.Institucion ORDER BY Institucion_Capitulo;
GO

-- 3. Obtener el presupuesto inicial total consolidado de todas las instituciones
SELECT SUM(EjecucionPresupuestaria_PresupuestoInicial) AS Gran_Total_Inicial FROM dbo.EjecucionPresupuestaria;
GO

-- 4. Contar cuántas unidades ejecutoras hay en cada capítulo ministerial
SELECT Institucion_Capitulo, COUNT(DISTINCT Institucion_CodigoUnidadEjecutora) AS Cantidad_Unidades 
FROM dbo.Institucion 
GROUP BY Institucion_Capitulo;
GO

-- 5. Mostrar las ejecuciones donde el presupuesto vigente es mayor al presupuesto inicial (Modificaciones)
SELECT TOP 100 * FROM dbo.EjecucionPresupuestaria WHERE EjecucionPresupuestaria_PresupuestoVigente > EjecucionPresupuestaria_PresupuestoInicial;
GO

-- 6. Listar los 5 programas con mayor presupuesto vigente asignado
SELECT TOP 5 p.Programa_Nombre, SUM(f.EjecucionPresupuestaria_PresupuestoVigente) as Total_Vigente
FROM dbo.EjecucionPresupuestaria f
JOIN dbo.Programa p ON f.EjecucionPresupuestaria_ProgramaID = p.Programa_ID
GROUP BY p.Programa_Nombre
ORDER BY Total_Vigente DESC;
GO

-- 7. Obtener el promedio de devengado por Tipo de Institución
SELECT i.Institucion_TipoInstitucion, AVG(f.EjecucionPresupuestaria_DevengadoAprobado) as Promedio_Devengado
FROM dbo.EjecucionPresupuestaria f
JOIN dbo.Institucion i ON f.EjecucionPresupuestaria_InstitucionID = i.Institucion_ID
GROUP BY i.Institucion_TipoInstitucion;
GO

-- 8. Consultar la ejecución por mes para el capítulo de 'PRESIDENCIA DE LA REPÚBLICA'
SELECT t.Tiempo_NombreMes, SUM(f.EjecucionPresupuestaria_DevengadoAprobado) as Ejecucion_Mensual
FROM dbo.EjecucionPresupuestaria f
JOIN dbo.Institucion i ON f.EjecucionPresupuestaria_InstitucionID = i.Institucion_ID
JOIN dbo.Periodo t ON f.EjecucionPresupuestaria_TiempoID = t.Tiempo_ID
WHERE i.Institucion_Capitulo LIKE '%PRESIDENCIA%'
GROUP BY t.Tiempo_ID, t.Tiempo_NombreMes
ORDER BY t.Tiempo_ID;
GO

-- 9. Mostrar los conceptos de gasto que han devengado montos significativos (> 100 Millones)
SELECT og.ObjetoGasto_Concepto, SUM(f.EjecucionPresupuestaria_DevengadoAprobado) as Total
FROM dbo.EjecucionPresupuestaria f
JOIN dbo.ObjetoGasto og ON f.EjecucionPresupuestaria_ObjetoGastoID = og.ObjetoGasto_ID
GROUP BY og.ObjetoGasto_Concepto
HAVING SUM(f.EjecucionPresupuestaria_DevengadoAprobado) > 100000000;
GO

-- 10. Listar ejecuciones con presupuesto vigente en un rango medio (Uso de BETWEEN)
SELECT TOP 100 * FROM dbo.EjecucionPresupuestaria WHERE EjecucionPresupuestaria_PresupuestoVigente BETWEEN 5000000 AND 10000000;
GO

-- 11. Buscar programas relacionados con 'VIVIENDA' o 'HÁBITAT' (Uso de LIKE)
SELECT * FROM dbo.Programa WHERE Programa_Nombre LIKE '%VIVIENDA%' OR Programa_Nombre LIKE '%HABITAT%';
GO

-- 12. Obtener el valor máximo y mínimo de presupuesto vigente en una sola fila
SELECT MAX(EjecucionPresupuestaria_PresupuestoVigente) AS Max_Vigente, MIN(EjecucionPresupuestaria_PresupuestoVigente) AS Min_Vigente 
FROM dbo.EjecucionPresupuestaria;
GO

-- 13. Subconsulta: Capítulos que no presentan ejecución de gasto (devengado en cero)
SELECT Institucion_Capitulo FROM dbo.Institucion 
WHERE Institucion_ID NOT IN (SELECT DISTINCT EjecucionPresupuestaria_InstitucionID FROM dbo.EjecucionPresupuestaria WHERE EjecucionPresupuestaria_DevengadoAprobado > 0);
GO

-- 14. JOIN de 4 tablas: Detalle consolidado de ejecución (Institución, Programa, Objeto, Monto)
SELECT TOP 100 i.Institucion_Capitulo, p.Programa_Nombre, og.ObjetoGasto_Auxiliar, f.EjecucionPresupuestaria_DevengadoAprobado
FROM dbo.EjecucionPresupuestaria f
JOIN dbo.Institucion i ON f.EjecucionPresupuestaria_InstitucionID = i.Institucion_ID
JOIN dbo.Programa p ON f.EjecucionPresupuestaria_ProgramaID = p.Programa_ID
JOIN dbo.ObjetoGasto og ON f.EjecucionPresupuestaria_ObjetoGastoID = og.ObjetoGasto_ID;
GO

-- 15. Calcular la diferencia entre presupuesto vigente y devengado (Saldo por Ejecutar)
SELECT TOP 100 EjecucionPresupuestaria_ID, (EjecucionPresupuestaria_PresupuestoVigente - EjecucionPresupuestaria_DevengadoAprobado) AS Saldo_Pendiente 
FROM dbo.EjecucionPresupuestaria;
GO

-- 16. Mostrar el top 5 de auxiliares de gasto con menor ejecución registrada
SELECT TOP 5 og.ObjetoGasto_Auxiliar, SUM(f.EjecucionPresupuestaria_DevengadoAprobado) as Total
FROM dbo.EjecucionPresupuestaria f
JOIN dbo.ObjetoGasto og ON f.EjecucionPresupuestaria_ObjetoGastoID = og.ObjetoGasto_ID
GROUP BY og.ObjetoGasto_Auxiliar
ORDER BY Total ASC;
GO

-- 17. Contar cuántas actividades diferentes existen por cada programa ministerial
SELECT Programa_Nombre, COUNT(DISTINCT Programa_Actividad) as Cant_Actividades FROM dbo.Programa GROUP BY Programa_Nombre;
GO

-- 18. Listar las ejecuciones del cuarto trimestre (Meses 10, 11, 12) usando IN
SELECT f.* 
FROM dbo.EjecucionPresupuestaria f
JOIN dbo.Periodo t ON f.EjecucionPresupuestaria_TiempoID = t.Tiempo_ID
WHERE t.Tiempo_Mes IN (10, 11, 12);
GO

-- 19. Obtener el total devengado agrupado por Clasificación de Objeto de Gasto
SELECT og.ObjetoGasto_Tipo, SUM(f.EjecucionPresupuestaria_DevengadoAprobado) as Total
FROM dbo.EjecucionPresupuestaria f
JOIN dbo.ObjetoGasto og ON f.EjecucionPresupuestaria_ObjetoGastoID = og.ObjetoGasto_ID
GROUP BY og.ObjetoGasto_Tipo;
GO

-- 20. Subconsulta correlacionada: Ejecuciones superiores al promedio de su respectivo programa
SELECT f1.EjecucionPresupuestaria_ID, f1.EjecucionPresupuestaria_DevengadoAprobado
FROM dbo.EjecucionPresupuestaria f1
WHERE f1.EjecucionPresupuestaria_DevengadoAprobado > (
    SELECT AVG(f2.EjecucionPresupuestaria_DevengadoAprobado) 
    FROM dbo.EjecucionPresupuestaria f2 
    WHERE f2.EjecucionPresupuestaria_ProgramaID = f1.EjecucionPresupuestaria_ProgramaID
);
GO

-- 21. Uso de CASE: Etiquetar el nivel de eficiencia de ejecución presupuestaria
SELECT EjecucionPresupuestaria_ID, 
    CASE 
        WHEN (EjecucionPresupuestaria_DevengadoAprobado / NULLIF(EjecucionPresupuestaria_PresupuestoVigente, 0)) >= 0.90 THEN 'Alta Ejecución'
        WHEN (EjecucionPresupuestaria_DevengadoAprobado / NULLIF(EjecucionPresupuestaria_PresupuestoVigente, 0)) BETWEEN 0.50 AND 0.89 THEN 'Ejecución Media'
        ELSE 'Baja Ejecución'
    END AS Nivel_Eficiencia
FROM dbo.EjecucionPresupuestaria;
GO

-- 22. Ranking de Ministerios (Capítulos) por volumen de presupuesto vigente
SELECT i.Institucion_Capitulo, SUM(f.EjecucionPresupuestaria_PresupuestoVigente) as Total
FROM dbo.EjecucionPresupuestaria f
JOIN dbo.Institucion i ON f.EjecucionPresupuestaria_InstitucionID = i.Institucion_ID
GROUP BY i.Institucion_Capitulo
ORDER BY Total DESC;
GO

-- 23. Obtener el porcentaje de participación de cada tipo de institución en el gasto nacional total
DECLARE @total_gasto_nacional DECIMAL(18,2) = (SELECT SUM(EjecucionPresupuestaria_DevengadoAprobado) FROM dbo.EjecucionPresupuestaria);
SELECT i.Institucion_TipoInstitucion, (SUM(f.EjecucionPresupuestaria_DevengadoAprobado) / NULLIF(@total_gasto_nacional, 0)) * 100 AS Porcentaje_Participacion
FROM dbo.EjecucionPresupuestaria f
JOIN dbo.Institucion i ON f.EjecucionPresupuestaria_InstitucionID = i.Institucion_ID
GROUP BY i.Institucion_TipoInstitucion;
GO

-- 24. Listar capítulos que contienen proyectos de inversión (Cod_Proyecto distinto de 0 o N/A)
SELECT DISTINCT i.Institucion_Capitulo
FROM dbo.EjecucionPresupuestaria f
JOIN dbo.Institucion i ON f.EjecucionPresupuestaria_InstitucionID = i.Institucion_ID
JOIN dbo.Programa p ON f.EjecucionPresupuestaria_ProgramaID = p.Programa_ID
WHERE p.Programa_CodigoProyecto <> '0' AND p.Programa_Proyecto <> 'N/A';
GO

-- 25. Resumen Ejecutivo Final: Entidades, Programas y Ejecución Global
SELECT 
    (SELECT COUNT(*) FROM dbo.Institucion) as Total_Instituciones,
    (SELECT COUNT(*) FROM dbo.Programa) as Total_Programas,
    SUM(EjecucionPresupuestaria_PresupuestoVigente) as Total_Presupuesto_Vigente,
    SUM(EjecucionPresupuestaria_DevengadoAprobado) as Total_Gasto_Devengado,
    (SUM(EjecucionPresupuestaria_DevengadoAprobado) / NULLIF(SUM(EjecucionPresupuestaria_PresupuestoVigente), 0)) * 100 AS Eficiencia_Global
FROM dbo.EjecucionPresupuestaria;
GO
