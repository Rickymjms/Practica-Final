/*
 * Proyecto Final: Presupuesto Nacional RD
 * Autor: Lic. Manuel Mañana Santana
 * LinkedIn: www.linkedin.com/in/manuelmañana
 *
 * Descripción: Script de Programación SQL (Stored Procedures y Triggers) para SQL Server.
 * Incluye lógica de negocio, auditoría y validaciones.
 */

USE PresupuestoNacionalRD;
GO

-- ==========================================================
-- 1. TABLAS DE AUDITORÍA Y REGISTRO HISTÓRICO
-- ==========================================================

IF OBJECT_ID('dbo.Audit_Fact_Updates', 'U') IS NOT NULL DROP TABLE dbo.Audit_Fact_Updates;
CREATE TABLE dbo.Audit_Fact_Updates (
    ID_Audit INT IDENTITY(1,1) PRIMARY KEY,
    ID_Ejecucion INT,
    Campo_Modificado VARCHAR(50),
    Valor_Anterior DECIMAL(18,2),
    Valor_Nuevo DECIMAL(18,2),
    Usuario VARCHAR(100),
    Fecha_Cambio DATETIME DEFAULT CURRENT_TIMESTAMP
);
GO

IF OBJECT_ID('dbo.Historial_Presupuesto', 'U') IS NOT NULL DROP TABLE dbo.Historial_Presupuesto;
CREATE TABLE dbo.Historial_Presupuesto (
    ID_Historial INT IDENTITY(1,1) PRIMARY KEY,
    ID_Ejecucion INT,
    Presupuesto_Vigente_Antiguo DECIMAL(18,2),
    Fecha_Registro DATETIME DEFAULT CURRENT_TIMESTAMP
);
GO

-- ==========================================================
-- 2. STORED PROCEDURES (5)
-- ==========================================================

-- SP 1: Insertar una nueva ejecución presupuestaria
CREATE OR ALTER PROCEDURE dbo.SP_Insertar_Ejecucion
    @p_ID_Inst INT, @p_ID_Prog INT, 
    @p_ID_Obj INT, @p_ID_Time INT, 
    @p_P_Inicial DECIMAL(18,2), @p_P_Vigente DECIMAL(18,2), @p_Devengado DECIMAL(18,2)
AS
BEGIN
    INSERT INTO dbo.Fact_Ejecucion_Presupuestaria (ID_Institucion, ID_Programa, ID_Objeto_Gasto, ID_Tiempo, Presupuesto_Inicial, Presupuesto_Vigente, Devengado_Aprobado)
    VALUES (@p_ID_Inst, @p_ID_Prog, @p_ID_Obj, @p_ID_Time, @p_P_Inicial, @p_P_Vigente, @p_Devengado);
END;
GO

-- SP 2: Obtener el presupuesto total por institución en un año específico
CREATE OR ALTER PROCEDURE dbo.SP_Get_Presupuesto_Institucion_Anio
    @p_Capitulo VARCHAR(255),
    @p_Anio INT
AS
BEGIN
    SELECT i.Capitulo, SUM(f.Presupuesto_Vigente) AS Total_Vigente
    FROM dbo.Fact_Ejecucion_Presupuestaria f
    JOIN dbo.Dim_Institucion i ON f.ID_Institucion = i.ID_Institucion
    JOIN dbo.Dim_Tiempo t ON f.ID_Tiempo = t.ID_Tiempo
    WHERE i.Capitulo = @p_Capitulo AND t.Periodo_Anio = @p_Anio
    GROUP BY i.Capitulo;
END;
GO

-- SP 3: Actualizar el monto devengado de una ejecución
CREATE OR ALTER PROCEDURE dbo.SP_Actualizar_Devengado
    @p_ID_Ejecucion INT,
    @p_Nuevo_Devengado DECIMAL(18,2)
AS
BEGIN
    UPDATE dbo.Fact_Ejecucion_Presupuestaria 
    SET Devengado_Aprobado = @p_Nuevo_Devengado 
    WHERE ID_Ejecucion = @p_ID_Ejecucion;
END;
GO

-- SP 4: Listar ejecuciones por Tipo de Institución
CREATE OR ALTER PROCEDURE dbo.SP_Listar_Por_Tipo_Institucion
    @p_Tipo VARCHAR(50)
AS
BEGIN
    SELECT f.*, i.Capitulo, i.Tipo_Institucion
    FROM dbo.Fact_Ejecucion_Presupuestaria f
    JOIN dbo.Dim_Institucion i ON f.ID_Institucion = i.ID_Institucion
    WHERE i.Tipo_Institucion = @p_Tipo;
END;
GO

-- SP 5: Eliminar registros de un año específico (Limpieza)
CREATE OR ALTER PROCEDURE dbo.SP_Eliminar_Ejecuciones_Anio
    @p_Anio INT
AS
BEGIN
    DELETE FROM dbo.Fact_Ejecucion_Presupuestaria 
    WHERE ID_Tiempo IN (SELECT ID_Tiempo FROM dbo.Dim_Tiempo WHERE Periodo_Anio = @p_Anio);
END;
GO

-- ==========================================================
-- 3. TRIGGERS (3)
-- ==========================================================

-- Trigger 1: Auditoría en actualizaciones de la tabla de hechos
CREATE OR ALTER TRIGGER dbo.TRG_Audit_Fact_Update
ON dbo.Fact_Ejecucion_Presupuestaria
AFTER UPDATE
AS
BEGIN
    INSERT INTO dbo.Audit_Fact_Updates (ID_Ejecucion, Campo_Modificado, Valor_Anterior, Valor_Nuevo, Usuario)
    SELECT i.ID_Ejecucion, 'Devengado_Aprobado', d.Devengado_Aprobado, i.Devengado_Aprobado, SYSTEM_USER
    FROM inserted i
    JOIN deleted d ON i.ID_Ejecucion = d.ID_Ejecucion
    WHERE i.Devengado_Aprobado <> d.Devengado_Aprobado;
END;
GO

-- Trigger 2: Registro histórico del presupuesto vigente antes de cambiar
CREATE OR ALTER TRIGGER dbo.TRG_Historial_Presupuesto
ON dbo.Fact_Ejecucion_Presupuestaria
AFTER UPDATE
AS
BEGIN
    INSERT INTO dbo.Historial_Presupuesto (ID_Ejecucion, Presupuesto_Vigente_Antiguo)
    SELECT d.ID_Ejecucion, d.Presupuesto_Vigente
    FROM deleted d
    JOIN inserted i ON d.ID_Ejecucion = i.ID_Ejecucion
    WHERE d.Presupuesto_Vigente <> i.Presupuesto_Vigente;
END;
GO

-- Trigger 3: Validación de inserción (Presupuesto Inicial no negativo)
CREATE OR ALTER TRIGGER dbo.TRG_Validar_Presupuesto_Insert
ON dbo.Fact_Ejecucion_Presupuestaria
AFTER INSERT
AS
BEGIN
    IF EXISTS (SELECT 1 FROM inserted WHERE Presupuesto_Inicial < 0)
    BEGIN
        RAISERROR('Error: El presupuesto inicial no puede ser negativo.', 16, 1);
        ROLLBACK TRANSACTION;
    END
END;
GO
