/*
 * Proyecto Final: Presupuesto Nacional RD
 * Autor: Lic. Manuel Mañana Santana
 *
 * Descripción: Script de Backup y Restauración para SQL Server.
 * Proporciona los comandos T-SQL para respaldar y restaurar la base de datos.
 * Aplicando nuevas normas de nomenclatura.
 */

USE master;
GO

-- ==========================================================
-- 1. COMANDO PARA BACKUP (Respaldo Completo)
-- ==========================================================
/*
   Asegúrese de que la carpeta de destino exista y tenga permisos de escritura 
   para el servicio de SQL Server.
*/

-- BACKUP DATABASE PresupuestoNacionalRD 
-- TO DISK = 'C:\Backups\PresupuestoNacionalRD_Completo.bak'
-- WITH FORMAT, MEDIANAME = 'SQLServerBackups', NAME = 'Full Backup of PresupuestoNacionalRD';
-- GO

-- ==========================================================
-- 2. COMANDO PARA RESTAURACIÓN
-- ==========================================================
/*
   Utilice este comando para restaurar la base de datos desde un archivo .bak.
*/

-- RESTORE DATABASE PresupuestoNacionalRD 
-- FROM DISK = 'C:\Backups\PresupuestoNacionalRD_Completo.bak'
-- WITH REPLACE, RECOVERY;
-- GO

-- ==========================================================
-- 3. LOG DE MANTENIMIENTO
-- ==========================================================
USE PresupuestoNacionalRD;
GO

IF OBJECT_ID('dbo.LogMantenimiento', 'U') IS NOT NULL DROP TABLE dbo.LogMantenimiento;
CREATE TABLE dbo.LogMantenimiento (
    LogMantenimiento_ID INT IDENTITY(1,1) PRIMARY KEY,
    LogMantenimiento_Accion VARCHAR(100),
    LogMantenimiento_Usuario VARCHAR(50),
    LogMantenimiento_Fecha DATETIME DEFAULT CURRENT_TIMESTAMP
);
GO

INSERT INTO dbo.LogMantenimiento (LogMantenimiento_Accion, LogMantenimiento_Usuario) 
VALUES ('Template de Backup Sincronizado para SQL Server', SYSTEM_USER);
GO

SELECT * FROM dbo.LogMantenimiento;
GO
