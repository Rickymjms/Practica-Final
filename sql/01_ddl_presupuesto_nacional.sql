/*
 * Proyecto Final: Presupuesto Nacional RD
 * Autor: Lic. Manuel Mañana Santana
 * LinkedIn: www.linkedin.com/in/manuelmañana
 *
 * Descripción: Script de Definición de Datos (DDL) para SQL Server.
 * Crea la base de datos, tablas, restricciones, índices y vistas.
 * Aplicando nuevas normas de nomenclatura y expandiendo el modelo a 10+ tablas.
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

-- Dimensión Organismo (Nueva Tabla 8)
IF OBJECT_ID('dbo.Organismo', 'U') IS NOT NULL DROP TABLE dbo.Organismo;
CREATE TABLE dbo.Organismo (
    Organismo_ID INT IDENTITY(1,1) PRIMARY KEY,
    Organismo_Codigo VARCHAR(10) NOT NULL,
    Organismo_Nombre VARCHAR(255) NOT NULL,
    CONSTRAINT UQ_Organismo UNIQUE (Organismo_Codigo)
);
GO

-- Dimensión Institución
IF OBJECT_ID('dbo.Institucion', 'U') IS NOT NULL DROP TABLE dbo.Institucion;
CREATE TABLE dbo.Institucion (
    Institucion_ID INT IDENTITY(1,1) PRIMARY KEY,
    Institucion_OrganismoID INT NULL, -- Relación con Organismo
    Institucion_CodigoCapitulo VARCHAR(10) NOT NULL,
    Institucion_Capitulo VARCHAR(255) NOT NULL,
    Institucion_CodigoSubCapitulo VARCHAR(10),
    Institucion_SubCapitulo VARCHAR(255),
    Institucion_CodigoUnidadEjecutora VARCHAR(10) NOT NULL,
    Institucion_UnidadEjecutora VARCHAR(255) NOT NULL,
    Institucion_TipoInstitucion VARCHAR(100), -- Campo para clasificación (Gobierno Central, Descentralizada, etc.)
    CONSTRAINT UQ_Institucion UNIQUE (Institucion_CodigoCapitulo, Institucion_CodigoSubCapitulo, Institucion_CodigoUnidadEjecutora),
    CONSTRAINT FK_Institucion_Organismo FOREIGN KEY (Institucion_OrganismoID) REFERENCES dbo.Organismo(Organismo_ID)
);
GO

-- Dimensión Programa
IF OBJECT_ID('dbo.Programa', 'U') IS NOT NULL DROP TABLE dbo.Programa;
CREATE TABLE dbo.Programa (
    Programa_ID INT IDENTITY(1,1) PRIMARY KEY,
    Programa_CodigoPrograma VARCHAR(20) NOT NULL,
    Programa_Nombre VARCHAR(255) NOT NULL,
    Programa_CodigoProducto VARCHAR(20),
    Programa_Producto VARCHAR(255),
    Programa_CodigoProyecto VARCHAR(20),
    Programa_Proyecto VARCHAR(255),
    Programa_CodigoActividad VARCHAR(20) NOT NULL,
    Programa_Actividad VARCHAR(255) NOT NULL,
    CONSTRAINT UQ_Programa UNIQUE (Programa_CodigoPrograma, Programa_CodigoProducto, Programa_CodigoProyecto, Programa_CodigoActividad)
);
GO

-- Dimensión Objeto del Gasto
IF OBJECT_ID('dbo.ObjetoGasto', 'U') IS NOT NULL DROP TABLE dbo.ObjetoGasto;
CREATE TABLE dbo.ObjetoGasto (
    ObjetoGasto_ID INT IDENTITY(1,1) PRIMARY KEY,
    ObjetoGasto_CodigoTipo VARCHAR(20) NOT NULL,
    ObjetoGasto_Tipo VARCHAR(100) NOT NULL,
    ObjetoGasto_CodigoConcepto VARCHAR(20) NOT NULL,
    ObjetoGasto_Concepto VARCHAR(100) NOT NULL,
    ObjetoGasto_CodigoCuenta VARCHAR(20) NOT NULL,
    ObjetoGasto_Cuenta VARCHAR(100) NOT NULL,
    ObjetoGasto_CodigoSubCuenta VARCHAR(20) NOT NULL,
    ObjetoGasto_SubCuenta VARCHAR(100) NOT NULL,
    ObjetoGasto_CodigoAuxiliar VARCHAR(20) NOT NULL,
    ObjetoGasto_Auxiliar VARCHAR(255) NOT NULL,
    CONSTRAINT UQ_ObjetoGasto UNIQUE (ObjetoGasto_CodigoTipo, ObjetoGasto_CodigoConcepto, ObjetoGasto_CodigoCuenta, ObjetoGasto_CodigoSubCuenta, ObjetoGasto_CodigoAuxiliar)
);
GO

-- Dimensión Periodo (Renombrada de Tiempo)
IF OBJECT_ID('dbo.Periodo', 'U') IS NOT NULL DROP TABLE dbo.Periodo;
CREATE TABLE dbo.Periodo (
    Periodo_ID INT IDENTITY(1,1) PRIMARY KEY,
    Periodo_Anio INT NOT NULL,
    Periodo_Mes INT NOT NULL CHECK (Periodo_Mes BETWEEN 1 AND 12),
    Periodo_NombreMes VARCHAR(20) NOT NULL,
    CONSTRAINT UQ_Periodo UNIQUE (Periodo_Anio, Periodo_Mes)
);
GO

-- Dimensión Fuente de Financiamiento (Nueva Tabla 9)
IF OBJECT_ID('dbo.FuenteFinanciamiento', 'U') IS NOT NULL DROP TABLE dbo.FuenteFinanciamiento;
CREATE TABLE dbo.FuenteFinanciamiento (
    FuenteFinanciamiento_ID INT IDENTITY(1,1) PRIMARY KEY,
    FuenteFinanciamiento_Codigo VARCHAR(10) NOT NULL,
    FuenteFinanciamiento_Descripcion VARCHAR(255) NOT NULL,
    CONSTRAINT UQ_FuenteFinanciamiento UNIQUE (FuenteFinanciamiento_Codigo)
);
GO

-- Dimensión País
IF OBJECT_ID('dbo.Pais', 'U') IS NOT NULL DROP TABLE dbo.Pais;
CREATE TABLE dbo.Pais (
    Pais_ID INT PRIMARY KEY,
    Pais_Nombre VARCHAR(255) NULL
);
GO

-- Dimensión Región (10 Regiones de Planificación)
IF OBJECT_ID('dbo.Region', 'U') IS NOT NULL DROP TABLE dbo.Region;
CREATE TABLE dbo.Region (
    Region_ID INT PRIMARY KEY,
    Region_Nombre VARCHAR(255) NULL,
    Region_PaisID INT NULL,
    CONSTRAINT FK_Region_Pais FOREIGN KEY (Region_PaisID) REFERENCES dbo.Pais(Pais_ID)
);
GO

-- Dimensión Provincia
IF OBJECT_ID('dbo.Provincia', 'U') IS NOT NULL DROP TABLE dbo.Provincia;
CREATE TABLE dbo.Provincia (
    Provincia_ID INT PRIMARY KEY,
    Provincia_Nombre VARCHAR(255) NULL,
    Provincia_RegionID INT NULL,
    CONSTRAINT FK_Provincia_Region FOREIGN KEY (Provincia_RegionID) REFERENCES dbo.Region(Region_ID)
);
GO

-- ==========================================================
-- 2. TABLA DE HECHOS
-- ==========================================================

IF OBJECT_ID('dbo.EjecucionPresupuestaria', 'U') IS NOT NULL DROP TABLE dbo.EjecucionPresupuestaria;
CREATE TABLE dbo.EjecucionPresupuestaria (
    EjecucionPresupuestaria_ID INT IDENTITY(1,1) PRIMARY KEY,
    EjecucionPresupuestaria_InstitucionID INT NOT NULL,
    EjecucionPresupuestaria_ProgramaID INT NOT NULL,
    EjecucionPresupuestaria_ObjetoGastoID INT NOT NULL,
    EjecucionPresupuestaria_PeriodoID INT NOT NULL, -- Relación actualizada
    EjecucionPresupuestaria_FuenteFinanciamientoID INT NULL,
    EjecucionPresupuestaria_ProvinciaID INT NULL, -- Relación geográfica consistente
    EjecucionPresupuestaria_PresupuestoInicial DECIMAL(18,2) DEFAULT 0.00 CHECK (EjecucionPresupuestaria_PresupuestoInicial >= 0),
    EjecucionPresupuestaria_PresupuestoVigente DECIMAL(18,2) DEFAULT 0.00 CHECK (EjecucionPresupuestaria_PresupuestoVigente >= 0),
    EjecucionPresupuestaria_DevengadoAprobado DECIMAL(18,2) DEFAULT 0.00 CHECK (EjecucionPresupuestaria_DevengadoAprobado >= 0),
    
    -- Relaciones (Claves Foráneas)
    CONSTRAINT FK_Ejecucion_Institucion FOREIGN KEY (EjecucionPresupuestaria_InstitucionID) REFERENCES dbo.Institucion(Institucion_ID),
    CONSTRAINT FK_Ejecucion_Programa FOREIGN KEY (EjecucionPresupuestaria_ProgramaID) REFERENCES dbo.Programa(Programa_ID),
    CONSTRAINT FK_Ejecucion_ObjetoGasto FOREIGN KEY (EjecucionPresupuestaria_ObjetoGastoID) REFERENCES dbo.ObjetoGasto(ObjetoGasto_ID),
    CONSTRAINT FK_Ejecucion_Periodo FOREIGN KEY (EjecucionPresupuestaria_PeriodoID) REFERENCES dbo.Periodo(Periodo_ID),
    CONSTRAINT FK_Ejecucion_FuenteFinanciamiento FOREIGN KEY (EjecucionPresupuestaria_FuenteFinanciamientoID) REFERENCES dbo.FuenteFinanciamiento(FuenteFinanciamiento_ID),
    CONSTRAINT FK_Ejecucion_Provincia FOREIGN KEY (EjecucionPresupuestaria_ProvinciaID) REFERENCES dbo.Provincia(Provincia_ID)
);
GO

-- ==========================================================
-- 3. ÍNDICES
-- ==========================================================

-- Índices para mejorar el rendimiento de las consultas frecuentes
CREATE INDEX IDX_Ejecucion_Institucion ON dbo.EjecucionPresupuestaria(EjecucionPresupuestaria_InstitucionID);
CREATE INDEX IDX_Ejecucion_Periodo ON dbo.EjecucionPresupuestaria(EjecucionPresupuestaria_PeriodoID);
CREATE INDEX IDX_ObjetoGasto_Codigos ON dbo.ObjetoGasto(ObjetoGasto_CodigoTipo, ObjetoGasto_CodigoConcepto);
GO

-- ==========================================================
-- 4. VISTAS ÚTILES
-- ==========================================================

-- Vista 1: Resumen de Ejecución por Institución y Año
CREATE OR ALTER VIEW dbo.View_Resumen_Institucion_Anio AS
SELECT 
    i.Institucion_Capitulo,
    t.Periodo_Anio,
    SUM(f.EjecucionPresupuestaria_PresupuestoInicial) AS Total_Inicial,
    SUM(f.EjecucionPresupuestaria_PresupuestoVigente) AS Total_Vigente,
    SUM(f.EjecucionPresupuestaria_DevengadoAprobado) AS Total_Devengado,
    (SUM(f.EjecucionPresupuestaria_DevengadoAprobado) / NULLIF(SUM(f.EjecucionPresupuestaria_PresupuestoVigente), 0)) * 100 AS Porcentaje_Ejecucion
FROM dbo.EjecucionPresupuestaria f
JOIN dbo.Institucion i ON f.EjecucionPresupuestaria_InstitucionID = i.Institucion_ID
JOIN dbo.Periodo t ON f.EjecucionPresupuestaria_PeriodoID = t.Periodo_ID
GROUP BY i.Institucion_Capitulo, t.Periodo_Anio;
GO

-- Vista 2: Análisis por Objeto de Gasto (Nivel Tipo)
CREATE OR ALTER VIEW dbo.View_Gasto_Por_Tipo AS
SELECT 
    og.ObjetoGasto_Tipo,
    SUM(f.EjecucionPresupuestaria_DevengadoAprobado) AS Total_Devengado
FROM dbo.EjecucionPresupuestaria f
JOIN dbo.ObjetoGasto og ON f.EjecucionPresupuestaria_ObjetoGastoID = og.ObjetoGasto_ID
GROUP BY og.ObjetoGasto_Tipo;
GO
