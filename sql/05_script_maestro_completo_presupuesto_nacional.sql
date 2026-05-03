/*
 * PROYECTO FINAL: Análisis del Presupuesto Nacional RD
 * AUTOR: Lic. Manuel Mañana Santana
 * FECHA: Mayo 2026
 * 
 * SCRIPT MAESTRO DE ORQUESTACIÓN (T-SQL)
 * Este archivo ejecuta todo el flujo del proyecto en el orden correcto.
 */

PRINT '-------------------------------------------------------';
PRINT 'INICIANDO DESPLIEGUE DEL PROYECTO: PRESUPUESTO NACIONAL RD';
PRINT 'AUTOR: Lic. Manuel Mañana Santana';
PRINT '-------------------------------------------------------';

-- 1. CREACIÓN DE ESTRUCTURA (DDL)
:r .\01_ddl_presupuesto_nacional.sql
PRINT 'Estructura DDL creada exitosamente.';

-- 2. CARGA DE DATOS (DML)
:r .\02_dml_presupuesto_nacional.sql
PRINT 'Datos DML cargados y actualizados.';

-- 3. PROGRAMACIÓN (SP & TRIGGERS)
:r .\04_programacion_sp_triggers_presupuesto_nacional.sql
PRINT 'Lógica procedimental (SP/Triggers) instalada.';

-- 4. CONSULTAS ANALÍTICAS (DQL)
:r .\03_dql_presupuesto_nacional.sql
PRINT 'Repositorio de 25 consultas DQL listo.';

-- 5. VERIFICACIÓN FINAL
:r .\06_verificacion_demo_presupuesto_nacional.sql
PRINT '-------------------------------------------------------';
PRINT 'PROCESO DE DESPLIEGUE FINALIZADO CON ÉXITO';
PRINT '-------------------------------------------------------';
GO
