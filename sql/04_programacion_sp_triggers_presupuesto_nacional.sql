/*
 * Proyecto Final: Presupuesto Nacional RD
 * Autor: Lic. Manuel Mañana Santana
 * LinkedIn: www.linkedin.com/in/manuelmañana
 *
 * Descripción: Script de Programación SQL (Stored Procedures y Triggers) para SQL Server.
 * Incluye lógica de negocio, auditoría y validaciones.
 * Aplicando nuevas normas de nomenclatura.
 */

USE PresupuestoNacionalRD;
GO

-- ==========================================================
-- 1. TABLAS DE AUDITORÍA Y REGISTRO HISTÓRICO
-- ==========================================================

IF OBJECT_ID('dbo.AuditoriaEjecucion', 'U') IS NOT NULL DROP TABLE dbo.AuditoriaEjecucion;
CREATE TABLE dbo.AuditoriaEjecucion (
    AuditoriaEjecucion_ID INT IDENTITY(1,1) PRIMARY KEY,
    AuditoriaEjecucion_EjecucionID INT,
    AuditoriaEjecucion_CampoModificado VARCHAR(50),
    AuditoriaEjecucion_ValorAnterior DECIMAL(18,2),
    AuditoriaEjecucion_ValorNuevo DECIMAL(18,2),
    AuditoriaEjecucion_Usuario VARCHAR(100),
    AuditoriaEjecucion_FechaCambio DATETIME DEFAULT CURRENT_TIMESTAMP
);
GO

IF OBJECT_ID('dbo.HistorialPresupuesto', 'U') IS NOT NULL DROP TABLE dbo.HistorialPresupuesto;
CREATE TABLE dbo.HistorialPresupuesto (
    HistorialPresupuesto_ID INT IDENTITY(1,1) PRIMARY KEY,
    HistorialPresupuesto_EjecucionID INT,
    HistorialPresupuesto_PresupuestoVigenteAntiguo DECIMAL(18,2),
    HistorialPresupuesto_FechaRegistro DATETIME DEFAULT CURRENT_TIMESTAMP
);
GO

-- ==========================================================
-- 2. STORED PROCEDURES (5)
-- ==========================================================

-- SP 1: Insertar una nueva ejecución presupuestaria
CREATE OR ALTER PROCEDURE dbo.SP_Insertar_Ejecucion
    @p_InstID INT, @p_ProgID INT, 
    @p_ObjID INT, @p_TimeID INT,
    @p_FuenteID INT = NULL, @p_GeoID INT = NULL,
    @p_P_Inicial DECIMAL(18,2), @p_P_Vigente DECIMAL(18,2), @p_Devengado DECIMAL(18,2)
AS
BEGIN
    INSERT INTO dbo.EjecucionPresupuestaria (
        EjecucionPresupuestaria_InstitucionID, 
        EjecucionPresupuestaria_ProgramaID, 
        EjecucionPresupuestaria_ObjetoGastoID, 
        EjecucionPresupuestaria_TiempoID,
        EjecucionPresupuestaria_FuenteFinanciamientoID,
        EjecucionPresupuestaria_GeografiaID,
        EjecucionPresupuestaria_PresupuestoInicial, 
        EjecucionPresupuestaria_PresupuestoVigente, 
        EjecucionPresupuestaria_DevengadoAprobado
    )
    VALUES (@p_InstID, @p_ProgID, @p_ObjID, @p_TimeID, @p_FuenteID, @p_GeoID, @p_P_Inicial, @p_P_Vigente, @p_Devengado);
END;
GO

-- SP 2: Obtener el presupuesto total por institución en un año específico
CREATE OR ALTER PROCEDURE dbo.SP_Get_Presupuesto_Institucion_Anio
    @p_Capitulo VARCHAR(255),
    @p_Anio INT
AS
BEGIN
    SELECT i.Institucion_Capitulo, SUM(f.EjecucionPresupuestaria_PresupuestoVigente) AS Total_Vigente
    FROM dbo.EjecucionPresupuestaria f
    JOIN dbo.Institucion i ON f.EjecucionPresupuestaria_InstitucionID = i.Institucion_ID
    JOIN dbo.Tiempo t ON f.EjecucionPresupuestaria_TiempoID = t.Tiempo_ID
    WHERE i.Institucion_Capitulo = @p_Capitulo AND t.Tiempo_Anio = @p_Anio
    GROUP BY i.Institucion_Capitulo;
END;
GO

-- SP 3: Actualizar el monto devengado de una ejecución
CREATE OR ALTER PROCEDURE dbo.SP_Actualizar_Devengado
    @p_ID INT,
    @p_Nuevo_Devengado DECIMAL(18,2)
AS
BEGIN
    UPDATE dbo.EjecucionPresupuestaria 
    SET EjecucionPresupuestaria_DevengadoAprobado = @p_Nuevo_Devengado 
    WHERE EjecucionPresupuestaria_ID = @p_ID;
END;
GO

-- SP 4: Listar ejecuciones por Organismo (Usando la nueva relación)
CREATE OR ALTER PROCEDURE dbo.SP_Listar_Por_Organismo
    @p_Organismo_Codigo VARCHAR(10)
AS
BEGIN
    SELECT f.*, i.Institucion_Capitulo, o.Organismo_Nombre
    FROM dbo.EjecucionPresupuestaria f
    JOIN dbo.Institucion i ON f.EjecucionPresupuestaria_InstitucionID = i.Institucion_ID
    JOIN dbo.Organismo o ON i.Institucion_OrganismoID = o.Organismo_ID
    WHERE o.Organismo_Codigo = @p_Organismo_Codigo;
END;
GO

-- SP 5: Eliminar registros de un año específico (Limpieza)
CREATE OR ALTER PROCEDURE dbo.SP_Eliminar_Ejecuciones_Anio
    @p_Anio INT
AS
BEGIN
    DELETE FROM dbo.EjecucionPresupuestaria 
    WHERE EjecucionPresupuestaria_TiempoID IN (SELECT Tiempo_ID FROM dbo.Tiempo WHERE Tiempo_Anio = @p_Anio);
END;
GO

-- ==========================================================
-- 3. TRIGGERS (3)
-- ==========================================================

-- Trigger 1: Auditoría en actualizaciones de la tabla de hechos
CREATE OR ALTER TRIGGER dbo.TRG_Auditoria_Ejecucion_Update
ON dbo.EjecucionPresupuestaria
AFTER UPDATE
AS
BEGIN
    INSERT INTO dbo.AuditoriaEjecucion (
        AuditoriaEjecucion_EjecucionID, 
        AuditoriaEjecucion_CampoModificado, 
        AuditoriaEjecucion_ValorAnterior, 
        AuditoriaEjecucion_ValorNuevo, 
        AuditoriaEjecucion_Usuario
    )
    SELECT 
        i.EjecucionPresupuestaria_ID, 
        'EjecucionPresupuestaria_DevengadoAprobado', 
        d.EjecucionPresupuestaria_DevengadoAprobado, 
        i.EjecucionPresupuestaria_DevengadoAprobado, 
        SYSTEM_USER
    FROM inserted i
    JOIN deleted d ON i.EjecucionPresupuestaria_ID = d.EjecucionPresupuestaria_ID
    WHERE i.EjecucionPresupuestaria_DevengadoAprobado <> d.EjecucionPresupuestaria_DevengadoAprobado;
END;
GO

-- Trigger 2: Registro histórico del presupuesto vigente antes de cambiar
CREATE OR ALTER TRIGGER dbo.TRG_Historial_Presupuesto_Update
ON dbo.EjecucionPresupuestaria
AFTER UPDATE
AS
BEGIN
    INSERT INTO dbo.HistorialPresupuesto (
        HistorialPresupuesto_EjecucionID, 
        HistorialPresupuesto_PresupuestoVigenteAntiguo
    )
    SELECT 
        d.EjecucionPresupuestaria_ID, 
        d.EjecucionPresupuestaria_PresupuestoVigente
    FROM deleted d
    JOIN inserted i ON d.EjecucionPresupuestaria_ID = i.EjecucionPresupuestaria_ID
    WHERE d.EjecucionPresupuestaria_PresupuestoVigente <> i.EjecucionPresupuestaria_PresupuestoVigente;
END;
GO

-- Trigger 3: Validación de inserción (Presupuesto Inicial no negativo)
CREATE OR ALTER TRIGGER dbo.TRG_Validar_Ejecucion_Insert
ON dbo.EjecucionPresupuestaria
AFTER INSERT
AS
BEGIN
    IF EXISTS (SELECT 1 FROM inserted WHERE EjecucionPresupuestaria_PresupuestoInicial < 0)
    BEGIN
        RAISERROR('Error: El presupuesto inicial no puede ser negativo.', 16, 1);
        ROLLBACK TRANSACTION;
    END
END;
GO
