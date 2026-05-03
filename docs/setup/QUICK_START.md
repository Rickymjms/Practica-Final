# Guía de Inicio Rápido - Presupuesto Nacional RD

Este documento describe la ruta más corta para ejecutar el proyecto de base de datos del Presupuesto Nacional RD.

## 1. Scripts Principales

Para reconstruir la base de datos completa y cargar los datos reales, ejecute:

```text
sql/05_script_maestro_completo_presupuesto_nacional.sql
```

Para verificar la carga y ver el resumen de registros:

```text
sql/06_verificacion_demo_presupuesto_nacional.sql
```

Ejemplos didácticos de consultas DQL:

```text
sql/07_dql_ejemplos_didacticos_presupuesto_nacional.sql
```

Pruebas de integridad referencial:

```text
sql/08_pruebas_integridad_presupuesto_nacional.sql
```

## 2. Ejecución en Windows (SQL Server Nativo)

Abra PowerShell en la carpeta del proyecto:

Autenticación de Windows:

```powershell
sqlcmd -S localhost -E -i .\sql\05_script_maestro_completo_presupuesto_nacional.sql
sqlcmd -S localhost -E -d PresupuestoNacionalRD -i .\sql\06_verificacion_demo_presupuesto_nacional.sql
```

Autenticación de SQL (Usuario SA):

```powershell
sqlcmd -S localhost -U sa -P "SU_PASSWORD" -i .\sql\05_script_maestro_completo_presupuesto_nacional.sql
sqlcmd -S localhost -U sa -P "SU_PASSWORD" -d PresupuestoNacionalRD -i .\sql\06_verificacion_demo_presupuesto_nacional.sql
```

## 3. Visualización de Resultados

Una vez ejecutados los scripts SQL:
1.  Abra el Dashboard interactivo: `dashboard/Dashboard_PresupuestoNacionalRD.html`.
2.  O cargue el archivo `powerbi/PresupuestoNacionalRD_PowerBI_Unificado.csv` en Power BI siguiendo la guía técnica.

## 4. Conteos de Verificación Esperados

El script de verificación debería mostrar aproximadamente:
*   **Dim_Institucion:** ~350 registros.
*   **Dim_Programa:** ~4,800 registros.
*   **Dim_Objeto_Gasto:** ~1,200 registros.
*   **Fact_Ejecucion_Presupuestaria:** ~246,000 registros.

---
**Autor:** Lic. Manuel Mañana Santana
**Estatus:** Versión 2.0 - Sincronizada con Proyecto Final.
