/*
 * Proyecto Final: Presupuesto Nacional RD
 * Autor: Lic. Manuel Mañana Santana
 * LinkedIn: www.linkedin.com/in/manuelmañana
 *
 * Descripción: Script de Definición de Datos (DDL) para SQL Server.
 * Crea la base de datos, tablas, restricciones, índices y vistas.
 */

-- Creación de la base de datos
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'PresupuestoNacionalRD')
BEGIN
    CREATE DATABASE PresupuestoNacionalRD;
END
GO

USE PresupuestoNacionalRD;
GO

-- ==========================================================
-- 1. TABLAS DIMENSIONALES
-- ==========================================================

-- Dimensión Institución
IF OBJECT_ID('dbo.Dim_Institucion', 'U') IS NOT NULL DROP TABLE dbo.Dim_Institucion;
CREATE TABLE dbo.Dim_Institucion (
    ID_Institucion INT IDENTITY(1,1) PRIMARY KEY,
    Cod_Capitulo VARCHAR(10) NOT NULL,
    Capitulo VARCHAR(255) NOT NULL,
    Cod_SubCapitulo VARCHAR(10),
    SubCapitulo VARCHAR(255),
    Cod_Unidad_Ejecutora VARCHAR(10) NOT NULL,
    Unidad_Ejecutora VARCHAR(255) NOT NULL,
    CONSTRAINT UQ_Institucion UNIQUE (Cod_Capitulo, Cod_SubCapitulo, Cod_Unidad_Ejecutora)
);
GO

-- Dimensión Programa
IF OBJECT_ID('dbo.Dim_Programa', 'U') IS NOT NULL DROP TABLE dbo.Dim_Programa;
CREATE TABLE dbo.Dim_Programa (
    ID_Programa INT IDENTITY(1,1) PRIMARY KEY,
    Cod_Programa VARCHAR(20) NOT NULL,
    Programa VARCHAR(255) NOT NULL,
    Cod_Producto VARCHAR(20),
    Producto VARCHAR(255),
    Cod_Proyecto VARCHAR(20),
    Proyecto VARCHAR(255),
    Cod_Actividad VARCHAR(20) NOT NULL,
    Actividad VARCHAR(255) NOT NULL,
    CONSTRAINT UQ_Programa UNIQUE (Cod_Programa, Cod_Producto, Cod_Proyecto, Cod_Actividad)
);
GO

-- Dimensión Objeto del Gasto
IF OBJECT_ID('dbo.Dim_Objeto_Gasto', 'U') IS NOT NULL DROP TABLE dbo.Dim_Objeto_Gasto;
CREATE TABLE dbo.Dim_Objeto_Gasto (
    ID_Objeto_Gasto INT IDENTITY(1,1) PRIMARY KEY,
    Cod_Tipo VARCHAR(20) NOT NULL,
    Tipo VARCHAR(100) NOT NULL,
    Cod_Concepto VARCHAR(20) NOT NULL,
    Concepto VARCHAR(100) NOT NULL,
    Cod_Cuenta VARCHAR(20) NOT NULL,
    Cuenta VARCHAR(100) NOT NULL,
    Cod_SubCuenta VARCHAR(20) NOT NULL,
    SubCuenta VARCHAR(100) NOT NULL,
    Cod_Auxiliar VARCHAR(20) NOT NULL,
    Auxiliar VARCHAR(255) NOT NULL,
    CONSTRAINT UQ_Objeto_Gasto UNIQUE (Cod_Tipo, Cod_Concepto, Cod_Cuenta, Cod_SubCuenta, Cod_Auxiliar)
);
GO

-- Dimensión Tiempo
IF OBJECT_ID('dbo.Dim_Tiempo', 'U') IS NOT NULL DROP TABLE dbo.Dim_Tiempo;
CREATE TABLE dbo.Dim_Tiempo (
    ID_Tiempo INT IDENTITY(1,1) PRIMARY KEY,
    Periodo_Anio INT NOT NULL,
    Mes_Imputacion INT NOT NULL CHECK (Mes_Imputacion BETWEEN 1 AND 12),
    Nombre_Mes VARCHAR(20) NOT NULL,
    CONSTRAINT UQ_Tiempo UNIQUE (Periodo_Anio, Mes_Imputacion)
);
GO

-- ==========================================================
-- 2. TABLA DE HECHOS
-- ==========================================================

IF OBJECT_ID('dbo.Fact_Ejecucion_Presupuestaria', 'U') IS NOT NULL DROP TABLE dbo.Fact_Ejecucion_Presupuestaria;
CREATE TABLE dbo.Fact_Ejecucion_Presupuestaria (
    ID_Ejecucion INT IDENTITY(1,1) PRIMARY KEY,
    ID_Institucion INT NOT NULL,
    ID_Programa INT NOT NULL,
    ID_Objeto_Gasto INT NOT NULL,
    ID_Tiempo INT NOT NULL,
    Presupuesto_Inicial DECIMAL(18,2) DEFAULT 0.00 CHECK (Presupuesto_Inicial >= 0),
    Presupuesto_Vigente DECIMAL(18,2) DEFAULT 0.00 CHECK (Presupuesto_Vigente >= 0),
    Devengado_Aprobado DECIMAL(18,2) DEFAULT 0.00 CHECK (Devengado_Aprobado >= 0),
    
    -- Relaciones (Claves Foráneas)
    CONSTRAINT FK_Institucion FOREIGN KEY (ID_Institucion) REFERENCES dbo.Dim_Institucion(ID_Institucion),
    CONSTRAINT FK_Programa FOREIGN KEY (ID_Programa) REFERENCES dbo.Dim_Programa(ID_Programa),
    CONSTRAINT FK_Objeto_Gasto FOREIGN KEY (ID_Objeto_Gasto) REFERENCES dbo.Dim_Objeto_Gasto(ID_Objeto_Gasto),
    CONSTRAINT FK_Tiempo FOREIGN KEY (ID_Tiempo) REFERENCES dbo.Dim_Tiempo(ID_Tiempo)
);
GO

-- ==========================================================
-- 3. ÍNDICES
-- ==========================================================

-- Índices para mejorar el rendimiento de las consultas frecuentes
CREATE INDEX IDX_Fact_Institucion ON dbo.Fact_Ejecucion_Presupuestaria(ID_Institucion);
CREATE INDEX IDX_Fact_Tiempo ON dbo.Fact_Ejecucion_Presupuestaria(ID_Tiempo);
CREATE INDEX IDX_ObjGasto_Codigos ON dbo.Dim_Objeto_Gasto(Cod_Tipo, Cod_Concepto);
GO

-- ==========================================================
-- 4. VISTAS ÚTILES
-- ==========================================================

-- Vista 1: Resumen de Ejecución por Institución y Año
CREATE OR ALTER VIEW dbo.View_Resumen_Institucion_Anio AS
SELECT 
    i.Capitulo,
    t.Periodo_Anio,
    SUM(f.Presupuesto_Inicial) AS Total_Inicial,
    SUM(f.Presupuesto_Vigente) AS Total_Vigente,
    SUM(f.Devengado_Aprobado) AS Total_Devengado,
    (SUM(f.Devengado_Aprobado) / NULLIF(SUM(f.Presupuesto_Vigente), 0)) * 100 AS Porcentaje_Ejecucion
FROM dbo.Fact_Ejecucion_Presupuestaria f
JOIN dbo.Dim_Institucion i ON f.ID_Institucion = i.ID_Institucion
JOIN dbo.Dim_Tiempo t ON f.ID_Tiempo = t.ID_Tiempo
GROUP BY i.Capitulo, t.Periodo_Anio;
GO

-- Vista 2: Análisis por Objeto de Gasto (Nivel Tipo)
CREATE OR ALTER VIEW dbo.View_Gasto_Por_Tipo AS
SELECT 
    og.Tipo,
    SUM(f.Devengado_Aprobado) AS Total_Devengado
FROM dbo.Fact_Ejecucion_Presupuestaria f
JOIN dbo.Dim_Objeto_Gasto og ON f.ID_Objeto_Gasto = og.ID_Objeto_Gasto
GROUP BY og.Tipo;
GO
