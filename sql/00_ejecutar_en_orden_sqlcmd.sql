/*
 * PROYECTO FINAL: Análisis del Presupuesto Nacional RD
 * AUTOR: Lic. Manuel Mañana Santana
 * 
 * GUÍA DE EJECUCIÓN EN ORDEN (MODO SQLCMD)
 */

/*
   INSTRUCCIONES:
   1. Abra SQL Server Management Studio (SSMS).
   2. Vaya al menú Query > SQLCMD Mode (Asegúrese de que esté activado).
   3. Ejecute este archivo o el script maestro 05.
*/

:r .\01_ddl_presupuesto_nacional.sql
:r .\02_dml_presupuesto_nacional.sql
:r .\04_programacion_sp_triggers_presupuesto_nacional.sql
:r .\03_dql_presupuesto_nacional.sql
:r .\06_verificacion_demo_presupuesto_nacional.sql
GO

PRINT 'El proyecto se ha ejecutado en el orden correcto siguiendo la Guía 2.0.';
PRINT 'Autor: Lic. Manuel Mañana Santana';
