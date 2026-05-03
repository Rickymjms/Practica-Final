import pandas as pd
import numpy as np
import os

def escape_sql(val, is_numeric=False):
    if pd.isna(val) or str(val).strip().lower() in ['nan', 'null', '']: 
        return "0" if is_numeric else "'N/A'"
    if is_numeric:
        try:
            f_val = float(val)
            if f_val == int(f_val):
                return str(int(f_val))
            return f"{f_val:.2f}"
        except:
            return "0"
    clean_val = str(val).replace("'", "''").strip()
    return f"'{clean_val}'" if clean_val != "" else "'N/A'"

def process():
    print("Leyendo dimensiones limpias...")
    # Standard reading forcing everything to string and dropping duplicates to avoid cartesian products
    dim_inst = pd.read_csv('datos/limpios/Dim_Institucion.csv', dtype=str).drop_duplicates()
    dim_prog = pd.read_csv('datos/limpios/Dim_Programa.csv', dtype=str).drop_duplicates()
    dim_og = pd.read_csv('datos/limpios/Dim_Objeto_Gasto.csv', dtype=str).drop_duplicates()
    
    # Static Time dimension (2017-2025)
    periodo_data = []
    id_p = 1
    for anio in range(2025, 2016, -1):
        for num, nombre in zip(range(1, 13), ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']):
            periodo_data.append({'Periodo_ID': id_p, 'Periodo_Anio': anio, 'Periodo_Mes': num, 'Periodo_NombreMes': nombre})
            id_p += 1
    dim_periodo = pd.DataFrame(periodo_data)

    print("Leyendo tabla de hechos...")
    fact = pd.read_csv('datos/limpios/Fact_Ejecucion_Presupuestaria.csv', dtype=str)
    print(f"Filas iniciales: {len(fact)}")
    
    # Numeric conversion for values
    for c in ['Presupuesto_Inicial', 'Presupuesto_Vigente', 'Devengado_Aprobado', 'Periodo_Anio', 'Mes_Imputacion']:
        fact[c] = pd.to_numeric(fact[c], errors='coerce').fillna(0)

    # Prepare Maps with unique keys to avoid join explosion
    print("Estandarizando claves y mapeando...")
    
    dim_inst['Institucion_ID'] = range(1, len(dim_inst) + 1)
    inst_keys = ['Cod_Capitulo', 'Cod_SubCapitulo', 'Cod_Unidad_Ejecutora']
    inst_map = dim_inst.drop_duplicates(inst_keys)[inst_keys + ['Institucion_ID']]
    fact = fact.merge(inst_map, on=inst_keys, how='left')
    print(f"Tras Institucion: {len(fact)}")
    
    dim_prog['Programa_ID'] = range(1, len(dim_prog) + 1)
    prog_keys = ['Cod_Programa', 'Cod_Producto', 'Cod_Proyecto', 'Cod_Actividad']
    prog_map = dim_prog.drop_duplicates(prog_keys)[prog_keys + ['Programa_ID']]
    fact = fact.merge(prog_map, on=prog_keys, how='left')
    print(f"Tras Programa: {len(fact)}")
    
    dim_og['ObjetoGasto_ID'] = range(1, len(dim_og) + 1)
    og_keys = ['Cod_Tipo', 'Cod_Concepto', 'Cod_Cuenta', 'Cod_SubCuenta', 'Cod_Auxiliar']
    og_map = dim_og.drop_duplicates(og_keys)[og_keys + ['ObjetoGasto_ID']]
    fact = fact.merge(og_map, on=og_keys, how='left')
    print(f"Tras ObjetoGasto: {len(fact)}")
    
    fact = fact.merge(dim_periodo, left_on=['Periodo_Anio', 'Mes_Imputacion'], right_on=['Periodo_Anio', 'Periodo_Mes'], how='left')
    print(f"Tras Periodo: {len(fact)}")

    # Final column assembly
    fact['P_I'] = fact['Institucion_ID'].fillna(1).astype(int)
    fact['P_P'] = fact['Programa_ID'].fillna(1).astype(int)
    fact['P_O'] = fact['ObjetoGasto_ID'].fillna(1).astype(int)
    fact['P_T'] = fact['Periodo_ID'].fillna(1).astype(int)
    fact['P_F'] = 1
    fact['P_G'] = pd.to_numeric(fact['Cod_Municipio'], errors='coerce').fillna(1).astype(int)
    
    out_file = 'sql/02_dml_presupuesto_nacional.sql'
    print(f"Escribiendo a {out_file}...")
    
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("USE PresupuestoNacionalRD;\nGO\n\n")
        f.write("ALTER TABLE dbo.EjecucionPresupuestaria NOCHECK CONSTRAINT ALL;\n")
        f.write("DELETE FROM dbo.EjecucionPresupuestaria; DELETE FROM dbo.Provincia; DELETE FROM dbo.Region; DELETE FROM dbo.Pais; DELETE FROM dbo.FuenteFinanciamiento; DELETE FROM dbo.Periodo; DELETE FROM dbo.ObjetoGasto; DELETE FROM dbo.Programa; DELETE FROM dbo.Institucion; DELETE FROM dbo.Organismo;\nGO\n\n")

        # Catalogs
        f.write("INSERT INTO dbo.Pais (Pais_ID, Pais_Nombre) VALUES (1, 'República Dominicana');\nGO\n")
        f.write("INSERT INTO dbo.Region (Region_ID, Region_Nombre, Region_PaisID) VALUES (1, 'Cibao Norte', 1), (2, 'Cibao Sur', 1), (3, 'Cibao Nordeste', 1), (4, 'Cibao Noroeste', 1), (5, 'Valdesia', 1), (6, 'Enriquillo', 1), (7, 'El Valle', 1), (8, 'Yuma', 1), (9, 'Higuamo', 1), (10, 'Ozama', 1);\nGO\n")
        f.write("INSERT INTO dbo.Provincia (Provincia_ID, Provincia_Nombre, Provincia_RegionID) VALUES (1, 'Santiago', 1), (2, 'Puerto Plata', 1), (3, 'Espaillat', 1), (4, 'La Vega', 2), (5, 'Monseñor Nouel', 2), (6, 'Sánchez Ramírez', 2), (7, 'Duarte', 3), (8, 'Hermanas Mirabal', 3), (9, 'María Trinidad Sánchez', 3), (10, 'Samaná', 3), (11, 'Valverde', 4), (12, 'Santiago Rodríguez', 4), (13, 'Monte Cristi', 4), (14, 'Dajabón', 4), (15, 'San Cristóbal', 5), (16, 'Peravia', 5), (17, 'San José de Ocoa', 5), (18, 'Barahona', 6), (19, 'Pedernales', 6), (20, 'Bahoruco', 6), (21, 'Independencia', 6), (22, 'San Juan', 7), (23, 'Elías Piña', 7), (24, 'Azua', 7), (25, 'La Altagracia', 8), (26, 'La Romana', 8), (27, 'El Seibo', 8), (28, 'San Pedro de Macorís', 9), (29, 'Hato Mayor', 9), (30, 'Monte Plata', 9), (31, 'Distrito Nacional', 10), (32, 'Santo Domingo', 10);\nGO\n\n")
        f.write("INSERT INTO dbo.FuenteFinanciamiento (FuenteFinanciamiento_Codigo, FuenteFinanciamiento_Descripcion) VALUES ('1', 'Tesoro Nacional');\nGO\n\n")

        def write_inserts(df, table, columns, id_col=None):
            if id_col: f.write(f"SET IDENTITY_INSERT {table} ON;\nGO\n")
            batch_size = 1000
            for i in range(0, len(df), batch_size):
                chunk = df.iloc[i:i+batch_size]
                cols_str = (id_col + ", " if id_col else "") + ", ".join(columns)
                insert_stmt = f"INSERT INTO {table} ({cols_str}) VALUES\n"
                vals_list = []
                for _, row in chunk.iterrows():
                    row_vals = []
                    if id_col: row_vals.append(str(int(row[id_col])))
                    for c in columns:
                        is_num = any(k in c for k in ['ID', 'Anio', 'Mes', 'Inicial', 'Vigente', 'Aprobado']) or c in ['P_I', 'P_P', 'P_O', 'P_T', 'P_F', 'P_G', 'Presupuesto_Inicial', 'Presupuesto_Vigente', 'Devengado_Aprobado']
                        row_vals.append(escape_sql(row[c], is_numeric=is_num))
                    vals_list.append("(" + ", ".join(row_vals) + ")")
                f.write(insert_stmt + ",\n".join(vals_list) + ";\nGO\n")
            if id_col: f.write(f"SET IDENTITY_INSERT {table} OFF;\nGO\n")

        # Institutions
        d_inst = dim_inst.rename(columns={'Cod_Capitulo': 'Institucion_CodigoCapitulo', 'Capitulo': 'Institucion_Capitulo', 'Cod_SubCapitulo': 'Institucion_CodigoSubCapitulo', 'SubCapitulo': 'Institucion_SubCapitulo', 'Cod_Unidad_Ejecutora': 'Institucion_CodigoUnidadEjecutora', 'Unidad_Ejecutora': 'Institucion_UnidadEjecutora'})
        write_inserts(d_inst, 'dbo.Institucion', [c for c in d_inst.columns if c != 'Institucion_ID'], 'Institucion_ID')

        # Programs
        d_prog = dim_prog.rename(columns={'Cod_Programa': 'Programa_CodigoPrograma', 'Programa': 'Programa_Nombre', 'Cod_Producto': 'Programa_CodigoProducto', 'Producto': 'Programa_Producto', 'Cod_Proyecto': 'Programa_CodigoProyecto', 'Proyecto': 'Programa_Proyecto', 'Cod_Actividad': 'Programa_CodigoActividad', 'Actividad': 'Programa_Actividad'})
        write_inserts(d_prog, 'dbo.Programa', [c for c in d_prog.columns if c != 'Programa_ID'], 'Programa_ID')

        # ObjetoGasto
        d_og = dim_og.rename(columns={'Cod_Tipo': 'ObjetoGasto_CodigoTipo', 'Tipo': 'ObjetoGasto_Tipo', 'Cod_Concepto': 'ObjetoGasto_CodigoConcepto', 'Concepto': 'ObjetoGasto_Concepto', 'Cod_Cuenta': 'ObjetoGasto_CodigoCuenta', 'Cuenta': 'ObjetoGasto_Cuenta', 'Cod_SubCuenta': 'ObjetoGasto_CodigoSubCuenta', 'SubCuenta': 'ObjetoGasto_SubCuenta', 'Cod_Auxiliar': 'ObjetoGasto_CodigoAuxiliar', 'Auxiliar': 'ObjetoGasto_Auxiliar'})
        write_inserts(d_og, 'dbo.ObjetoGasto', [c for c in d_og.columns if c != 'ObjetoGasto_ID'], 'ObjetoGasto_ID')

        # Periodo
        write_inserts(dim_periodo, 'dbo.Periodo', ['Periodo_Anio', 'Periodo_Mes', 'Periodo_NombreMes'], 'Periodo_ID')

        # Facts
        fact_cols = ['EjecucionPresupuestaria_PresupuestoInicial', 'EjecucionPresupuestaria_PresupuestoVigente', 'EjecucionPresupuestaria_DevengadoAprobado', 'P_I', 'P_P', 'P_O', 'P_T', 'P_F', 'P_G']
        fact_write = fact.rename(columns={'Presupuesto_Inicial': 'EjecucionPresupuestaria_PresupuestoInicial', 'Presupuesto_Vigente': 'EjecucionPresupuestaria_PresupuestoVigente', 'Devengado_Aprobado': 'EjecucionPresupuestaria_DevengadoAprobado'})
        # Reorder to match fact_cols
        fact_write = fact_write[['EjecucionPresupuestaria_PresupuestoInicial', 'EjecucionPresupuestaria_PresupuestoVigente', 'EjecucionPresupuestaria_DevengadoAprobado', 'P_I', 'P_P', 'P_O', 'P_T', 'P_F', 'P_G']]
        # Map back P_ columns to DDL names for the SQL header
        final_cols = ['EjecucionPresupuestaria_PresupuestoInicial', 'EjecucionPresupuestaria_PresupuestoVigente', 'EjecucionPresupuestaria_DevengadoAprobado', 'EjecucionPresupuestaria_InstitucionID', 'EjecucionPresupuestaria_ProgramaID', 'EjecucionPresupuestaria_ObjetoGastoID', 'EjecucionPresupuestaria_PeriodoID', 'EjecucionPresupuestaria_FuenteFinanciamientoID', 'EjecucionPresupuestaria_ProvinciaID']
        fact_write.columns = final_cols
        write_inserts(fact_write, 'dbo.EjecucionPresupuestaria', final_cols)

    print(f"DML generado exitosamente en {out_file}")

if __name__ == "__main__":
    process()
