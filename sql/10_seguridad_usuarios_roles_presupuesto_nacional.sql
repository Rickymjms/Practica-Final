/*
 * Proyecto Final: Presupuesto Nacional RD
 * Autor: Lic. Manuel Mañana Santana
 *
 * Descripción: Gestión de Seguridad, Usuarios y Roles para SQL Server.
 * Implementa el principio de mínimo privilegio.
 * Aplicando nuevas normas de nomenclatura.
 */

USE master;
GO

-- ==========================================================
-- 1. CREACIÓN DE LOGIN (Nivel Servidor)
-- ==========================================================

IF NOT EXISTS (SELECT * FROM sys.server_principals WHERE name = 'usuario_consulta')
BEGIN
    -- Se recomienda cambiar esta contraseña en un entorno de producción real
    CREATE LOGIN usuario_consulta WITH PASSWORD = 'Presu2025*', CHECK_POLICY = OFF;
END
GO

USE PresupuestoNacionalRD;
GO

-- ==========================================================
-- 2. CREACIÓN DE USUARIO Y ROL (Nivel Base de Datos)
-- ==========================================================

-- Crear el rol de consulta si no existe
IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = 'Rol_Consulta_Presupuesto' AND type = 'R')
BEGIN
    CREATE ROLE Rol_Consulta_Presupuesto;
END
GO

-- Asignar permisos de solo lectura al rol en el esquema dbo
GRANT SELECT TO Rol_Consulta_Presupuesto;
GO

-- Crear el usuario 'usuario_consulta' vinculado al login
IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = 'usuario_consulta')
BEGIN
    CREATE USER usuario_consulta FOR LOGIN usuario_consulta;
END
GO

-- Asignar el rol al usuario
ALTER ROLE Rol_Consulta_Presupuesto ADD MEMBER usuario_consulta;
GO

-- ==========================================================
-- 3. VERIFICACIÓN DE PERMISOS
-- ==========================================================

-- Listar permisos del usuario
SELECT
    pr.name AS Usuario,
    pe.permission_name AS Permiso,
    pe.state_desc AS Estado
FROM sys.database_permissions pe
JOIN sys.database_principals pr ON pe.grantee_principal_id = pr.principal_id
WHERE pr.name = 'Rol_Consulta_Presupuesto';
GO

SELECT 'Seguridad configurada correctamente para SQL Server.' AS Mensaje;
GO
