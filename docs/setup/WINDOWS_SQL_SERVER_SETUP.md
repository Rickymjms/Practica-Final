# Guía de Configuración: SQL Server en Windows

Esta guía está dirigida a usuarios de Windows. A diferencia de macOS o Linux, en Windows SQL Server se ejecuta de forma nativa sin necesidad de Docker (aunque es opcional).

## 1. Requisitos Previos

*   SQL Server (Developer o Express) instalado localmente.
*   SQL Server Management Studio (SSMS) o Azure Data Studio.
*   Herramientas de línea de comandos `sqlcmd` instaladas.

## 2. Scripts del Proyecto

Los scripts orquestadores se encuentran en la carpeta `sql/`:
*   `05_script_maestro_completo_presupuesto_nacional.sql`: Crea la DB `PresupuestoNacionalRD` y carga todas las tablas.
*   `06_verificacion_demo_presupuesto_nacional.sql`: Ejecuta conteos de auditoría.

## 3. Iniciar el Servicio SQL Server

Abra PowerShell como Administrador:

Para instancia predeterminada:
```powershell
net start MSSQLSERVER
```

Para SQL Express:
```powershell
net start MSSQL$SQLEXPRESS
```

## 4. Ejecución mediante sqlcmd

Desde la raíz del proyecto, ejecute los siguientes comandos:

**Con Autenticación de Windows:**
```powershell
sqlcmd -S localhost -E -i .\sql\05_script_maestro_completo_presupuesto_nacional.sql
sqlcmd -S localhost -E -d PresupuestoNacionalRD -i .\sql\06_verificacion_demo_presupuesto_nacional.sql
```

**Con Usuario SA:**
```powershell
sqlcmd -S localhost -U sa -P "SU_PASSWORD" -i .\sql\05_script_maestro_completo_presupuesto_nacional.sql
```

## 5. Resolución de Problemas

*   **sqlcmd no se reconoce:** Instale las "Microsoft Command Line Utilities for SQL Server".
*   **Error de conexión:** Verifique que el servicio esté iniciado y que el nombre del servidor (localhost o localhost\SQLEXPRESS) sea el correcto.
*   **Permisos:** Asegúrese de tener permisos de `sysadmin` para crear la base de datos desde el script maestro.

---
**Autor:** Lic. Manuel Mañana Santana
**Proyecto:** Análisis del Presupuesto Nacional RD
