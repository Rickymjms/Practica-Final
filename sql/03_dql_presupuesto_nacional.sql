/*
 * Proyecto Final: Presupuesto Nacional RD
 * Autor: Lic. Manuel Mañana Santana
 * LinkedIn: www.linkedin.com/in/manuelmañana
 *
 * Descripción: Script de Consultas (DQL) para SQL Server.
 * Contiene 25 consultas SQL que van de nivel básico a avanzado.
 * NOTA: Este script ha sido optimizado para clasificaciones Institucionales, 
 * Programáticas y Económicas, omitiendo dimensiones geográficas.
 */

USE PresupuestoNacionalRD;
GO

-- 1. Listar todas las instituciones registradas (Primeras 100)
SELECT TOP 100 * FROM dbo.Dim_Institucion;
GO

-- 2. Mostrar los nombres de los capítulos y subcapítulos sin duplicados
SELECT DISTINCT Capitulo, SubCapitulo FROM dbo.Dim_Institucion ORDER BY Capitulo;
GO

-- 3. Obtener el presupuesto inicial total consolidado de todas las instituciones
SELECT SUM(Presupuesto_Inicial) AS Gran_Total_Inicial FROM dbo.Fact_Ejecucion_Presupuestaria;
GO

-- 4. Contar cuántas unidades ejecutoras hay en cada capítulo ministerial
SELECT Capitulo, COUNT(DISTINCT Cod_Unidad_Ejecutora) AS Cantidad_Unidades 
FROM dbo.Dim_Institucion 
GROUP BY Capitulo;
GO

-- 5. Mostrar las ejecuciones donde el presupuesto vigente es mayor al presupuesto inicial (Modificaciones)
SELECT TOP 100 * FROM dbo.Fact_Ejecucion_Presupuestaria WHERE Presupuesto_Vigente > Presupuesto_Inicial;
GO

-- 6. Listar los 5 programas con mayor presupuesto vigente asignado
SELECT TOP 5 p.Programa, SUM(f.Presupuesto_Vigente) as Total_Vigente
FROM dbo.Fact_Ejecucion_Presupuestaria f
JOIN dbo.Dim_Programa p ON f.ID_Programa = p.ID_Programa
GROUP BY p.Programa
ORDER BY Total_Vigente DESC;
GO

-- 7. Obtener el promedio de devengado por Tipo de Institución (Clasificación creada en DML)
SELECT i.Tipo_Institucion, AVG(f.Devengado_Aprobado) as Promedio_Devengado
FROM dbo.Fact_Ejecucion_Presupuestaria f
JOIN dbo.Dim_Institucion i ON f.ID_Institucion = i.ID_Institucion
GROUP BY i.Tipo_Institucion;
GO

-- 8. Consultar la ejecución por mes para el capítulo de 'PRESIDENCIA DE LA REPÚBLICA'
SELECT t.Nombre_Mes, SUM(f.Devengado_Aprobado) as Ejecucion_Mensual
FROM dbo.Fact_Ejecucion_Presupuestaria f
JOIN dbo.Dim_Institucion i ON f.ID_Institucion = i.ID_Institucion
JOIN dbo.Dim_Tiempo t ON f.ID_Tiempo = t.ID_Tiempo
WHERE i.Capitulo LIKE '%PRESIDENCIA%'
GROUP BY t.ID_Tiempo, t.Nombre_Mes
ORDER BY t.ID_Tiempo;
GO

-- 9. Mostrar los conceptos de gasto que han devengado montos significativos (> 100 Millones)
SELECT og.Concepto, SUM(f.Devengado_Aprobado) as Total
FROM dbo.Fact_Ejecucion_Presupuestaria f
JOIN dbo.Dim_Objeto_Gasto og ON f.ID_Objeto_Gasto = og.ID_Objeto_Gasto
GROUP BY og.Concepto
HAVING SUM(f.Devengado_Aprobado) > 100000000;
GO

-- 10. Listar ejecuciones con presupuesto vigente en un rango medio (Uso de BETWEEN)
SELECT TOP 100 * FROM dbo.Fact_Ejecucion_Presupuestaria WHERE Presupuesto_Vigente BETWEEN 5000000 AND 10000000;
GO

-- 11. Buscar programas relacionados con 'VIVIENDA' o 'HÁBITAT' (Uso de LIKE)
SELECT * FROM dbo.Dim_Programa WHERE Programa LIKE '%VIVIENDA%' OR Programa LIKE '%HABITAT%';
GO

-- 12. Obtener el valor máximo y mínimo de presupuesto vigente en una sola fila
SELECT MAX(Presupuesto_Vigente) AS Max_Vigente, MIN(Presupuesto_Vigente) AS Min_Vigente 
FROM dbo.Fact_Ejecucion_Presupuestaria;
GO

-- 13. Subconsulta: Capítulos que no presentan ejecución de gasto (devengado en cero)
SELECT Capitulo FROM dbo.Dim_Institucion 
WHERE ID_Institucion NOT IN (SELECT DISTINCT ID_Institucion FROM dbo.Fact_Ejecucion_Presupuestaria WHERE Devengado_Aprobado > 0);
GO

-- 14. JOIN de 4 tablas: Detalle consolidado de ejecución (Institución, Programa, Objeto, Monto)
SELECT TOP 100 i.Capitulo, p.Programa, og.Auxiliar, f.Devengado_Aprobado
FROM dbo.Fact_Ejecucion_Presupuestaria f
JOIN dbo.Dim_Institucion i ON f.ID_Institucion = i.ID_Institucion
JOIN dbo.Dim_Programa p ON f.ID_Programa = p.ID_Programa
JOIN dbo.Dim_Objeto_Gasto og ON f.ID_Objeto_Gasto = og.ID_Objeto_Gasto;
GO

-- 15. Calcular la diferencia entre presupuesto vigente y devengado (Saldo por Ejecutar)
SELECT TOP 100 ID_Ejecucion, (Presupuesto_Vigente - Devengado_Aprobado) AS Saldo_Pendiente 
FROM dbo.Fact_Ejecucion_Presupuestaria;
GO

-- 16. Mostrar el top 5 de auxiliares de gasto con menor ejecución registrada
SELECT TOP 5 og.Auxiliar, SUM(f.Devengado_Aprobado) as Total
FROM dbo.Fact_Ejecucion_Presupuestaria f
JOIN dbo.Dim_Objeto_Gasto og ON f.ID_Objeto_Gasto = og.ID_Objeto_Gasto
GROUP BY og.Auxiliar
ORDER BY Total ASC;
GO

-- 17. Contar cuántas actividades diferentes existen por cada programa ministerial
SELECT Programa, COUNT(DISTINCT Actividad) as Cant_Actividades FROM dbo.Dim_Programa GROUP BY Programa;
GO

-- 18. Listar las ejecuciones del cuarto trimestre (Meses 10, 11, 12) usando IN
SELECT f.* 
FROM dbo.Fact_Ejecucion_Presupuestaria f
JOIN dbo.Dim_Tiempo t ON f.ID_Tiempo = t.ID_Tiempo
WHERE t.Mes_Imputacion IN (10, 11, 12);
GO

-- 19. Obtener el total devengado agrupado por Clasificación de Objeto de Gasto
SELECT og.Tipo, SUM(f.Devengado_Aprobado) as Total
FROM dbo.Fact_Ejecucion_Presupuestaria f
JOIN dbo.Dim_Objeto_Gasto og ON f.ID_Objeto_Gasto = og.ID_Objeto_Gasto
GROUP BY og.Tipo;
GO

-- 20. Subconsulta correlacionada: Ejecuciones superiores al promedio de su respectivo programa
SELECT f1.ID_Ejecucion, f1.Devengado_Aprobado
FROM dbo.Fact_Ejecucion_Presupuestaria f1
WHERE f1.Devengado_Aprobado > (
    SELECT AVG(f2.Devengado_Aprobado) 
    FROM dbo.Fact_Ejecucion_Presupuestaria f2 
    WHERE f2.ID_Programa = f1.ID_Programa
);
GO

-- 21. Uso de CASE: Etiquetar el nivel de eficiencia de ejecución presupuestaria
SELECT ID_Ejecucion, 
    CASE 
        WHEN (Devengado_Aprobado / NULLIF(Presupuesto_Vigente, 0)) >= 0.90 THEN 'Alta Ejecución'
        WHEN (Devengado_Aprobado / NULLIF(Presupuesto_Vigente, 0)) BETWEEN 0.50 AND 0.89 THEN 'Ejecución Media'
        ELSE 'Baja Ejecución'
    END AS Nivel_Eficiencia
FROM dbo.Fact_Ejecucion_Presupuestaria;
GO

-- 22. Ranking de Ministerios (Capítulos) por volumen de presupuesto vigente
SELECT i.Capitulo, SUM(f.Presupuesto_Vigente) as Total
FROM dbo.Fact_Ejecucion_Presupuestaria f
JOIN dbo.Dim_Institucion i ON f.ID_Institucion = i.ID_Institucion
GROUP BY i.Capitulo
ORDER BY Total DESC;
GO

-- 23. Obtener el porcentaje de participación de cada tipo de institución en el gasto nacional total
DECLARE @total_gasto_nacional DECIMAL(18,2) = (SELECT SUM(Devengado_Aprobado) FROM dbo.Fact_Ejecucion_Presupuestaria);
SELECT i.Tipo_Institucion, (SUM(f.Devengado_Aprobado) / NULLIF(@total_gasto_nacional, 0)) * 100 AS Porcentaje_Participacion
FROM dbo.Fact_Ejecucion_Presupuestaria f
JOIN dbo.Dim_Institucion i ON f.ID_Institucion = i.ID_Institucion
GROUP BY i.Tipo_Institucion;
GO

-- 24. Listar capítulos que contienen proyectos de inversión (Cod_Proyecto distinto de 0 o N/A)
SELECT DISTINCT i.Capitulo
FROM dbo.Fact_Ejecucion_Presupuestaria f
JOIN dbo.Dim_Institucion i ON f.ID_Institucion = i.ID_Institucion
JOIN dbo.Dim_Programa p ON f.ID_Programa = p.ID_Programa
WHERE p.Cod_Proyecto <> '0' AND p.Proyecto <> 'N/A';
GO

-- 25. Resumen Ejecutivo Final: Entidades, Programas y Ejecución Global
SELECT 
    (SELECT COUNT(*) FROM dbo.Dim_Institucion) as Total_Instituciones,
    (SELECT COUNT(*) FROM dbo.Dim_Programa) as Total_Programas,
    SUM(Presupuesto_Vigente) as Total_Presupuesto_Vigente,
    SUM(Devengado_Aprobado) as Total_Gasto_Devengado,
    (SUM(Devengado_Aprobado) / NULLIF(SUM(Presupuesto_Vigente), 0)) * 100 AS Eficiencia_Global
FROM dbo.Fact_Ejecucion_Presupuestaria;
GO
