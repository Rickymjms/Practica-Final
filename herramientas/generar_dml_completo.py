import pandas as pd
import numpy as np
import os

def escape_sql(val, is_numeric=False):
    if pd.isna(val) or str(val).strip().lower() in ['nan', 'null', '']: 
        return "0" if is_numeric else "'N/A'"
    if is_numeric:
        try:
            # Evitar notación científica y formatear decimales
            f_val = float(val)
            if f_val == int(f_val):
                return str(int(f_val))
            return f"{f_val:.2f}"
        except:
            return "0"
    # Escapar comillas simples
    clean_val = str(val).replace("'", "''").strip()
    return f"'{clean_val}'" if clean_val != "" else "'N/A'"

def to_str_key(val):
    if pd.isna(val): return 'nan'
    s = str(val).strip()
    if s.endswith('.0'):
        return s[:-2]
    return s

def process():
    print("Leyendo dimensiones limpias...")
    dim_inst = pd.read_csv('datos/limpios/Dim_Institucion.csv')
    dim_prog = pd.read_csv('datos/limpios/Dim_Programa.csv')
    dim_og = pd.read_csv('datos/limpios/Dim_Objeto_Gasto.csv')
    
    # Crear dimensión Tiempo estática según requerimiento del usuario
    tiempo_data = []
    id_t = 1
    # De 2025 hacia atrás hasta 2017
    for anio in range(2025, 2016, -1):
        meses = [
            (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'),
            (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'),
            (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')
        ]
        for num, nombre in meses:
            tiempo_data.append({
                'ID_Tiempo': id_t,
                'Periodo_Anio': anio,
                'Mes_Imputacion': num,
                'Nombre_Mes': nombre
            })
            id_t += 1
    dim_tiempo = pd.DataFrame(tiempo_data)
    
    print("Leyendo tabla de hechos...")
    fact = pd.read_csv('datos/limpios/Fact_Ejecucion_Presupuestaria.csv')
    
    # Claves de cruce
    inst_keys = ['Cod_Capitulo', 'Cod_SubCapitulo', 'Cod_Unidad_Ejecutora']
    prog_keys = ['Cod_Programa', 'Cod_Producto', 'Cod_Proyecto', 'Cod_Actividad']
    og_keys = ['Cod_Tipo', 'Cod_Concepto', 'Cod_Cuenta', 'Cod_SubCuenta', 'Cod_Auxiliar']
    tiempo_keys = ['Periodo_Anio', 'Mes_Imputacion']
    
    print("Estandarizando claves...")
    # Omitimos dim_tiempo aquí porque ya está estandarizada arriba
    for df, keys in [(dim_inst, inst_keys), (dim_prog, prog_keys), (dim_og, og_keys)]:
        for k in keys:
            df[k] = df[k].apply(to_str_key)
            if k in fact.columns:
                fact[k] = fact[k].apply(to_str_key)
    
    # Estandarizar claves de tiempo en fact
    print("Estandarizando claves de tiempo...")
    fact['Periodo_Anio'] = fact['Periodo_Anio'].astype(int)
    # Si Mes_Imputacion viene como '2025/01', extraemos solo el 01
    def parse_month(val):
        s = str(val).strip()
        if '/' in s:
            return int(s.split('/')[1])
        return int(float(s))
    
    fact['Mes_Imputacion'] = fact['Mes_Imputacion'].apply(parse_month)
                
    # Asignar IDs a dimensiones dinámicas
    dim_inst['ID_Institucion'] = range(1, len(dim_inst) + 1)
    dim_prog['ID_Programa'] = range(1, len(dim_prog) + 1)
    dim_og['ID_Objeto_Gasto'] = range(1, len(dim_og) + 1)
    
    print("Cruzando IDs con tabla de hechos...")
    fact = fact.merge(dim_inst[inst_keys + ['ID_Institucion']], on=inst_keys, how='left')
    fact = fact.merge(dim_prog[prog_keys + ['ID_Programa']], on=prog_keys, how='left')
    fact = fact.merge(dim_og[og_keys + ['ID_Objeto_Gasto']], on=og_keys, how='left')
    fact = fact.merge(dim_tiempo[tiempo_keys + ['ID_Tiempo']], on=tiempo_keys, how='left')
    
    # Reporte de nulos por si alguna clave no cruzó
    for col in ['ID_Institucion', 'ID_Programa', 'ID_Objeto_Gasto', 'ID_Tiempo']:
        missing = fact[col].isna().sum()
        if missing > 0:
            print(f"ADVERTENCIA: Faltan {missing} mapeos en {col}")
        fact[col] = fact[col].fillna(1).astype(int) # Default 1 para evitar error de SQL
        
    # Limpieza de nulos y aseguramiento de valores no negativos (para cumplir con restricciones CHECK)
    fact['Presupuesto_Inicial'] = np.maximum(0, fact['Presupuesto_Inicial'].fillna(0)).round(2)
    fact['Presupuesto_Vigente'] = np.maximum(0, fact['Presupuesto_Vigente'].fillna(0)).round(2)
    fact['Devengado_Aprobado'] = np.maximum(0, fact['Devengado_Aprobado'].fillna(0)).round(2)
    
    out_file = 'sql/02_dml_presupuesto_nacional.sql'
    print(f"Escribiendo masivamente a {out_file} (Esto puede tomar unos momentos)...")
    
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("/*\n * Proyecto Final: Presupuesto Nacional RD\n * Autor: Lic. Manuel Mañana Santana\n *\n")
        f.write(" * Descripción: Script de Manipulación de Datos (DML) para SQL Server.\n")
        f.write(" * IMPORTANTE: Contiene TODOS los registros reales en formato INSERT INTO manual.\n */\n\n")
        f.write("USE PresupuestoNacionalRD;\nGO\n\n")
        
        f.write("PRINT 'Eliminando datos previos...';\n")
        f.write("ALTER TABLE dbo.Fact_Ejecucion_Presupuestaria NOCHECK CONSTRAINT ALL;\n")
        f.write("DELETE FROM dbo.Fact_Ejecucion_Presupuestaria;\n")
        f.write("DELETE FROM dbo.Dim_Institucion;\n")
        f.write("DELETE FROM dbo.Dim_Programa;\n")
        f.write("DELETE FROM dbo.Dim_Objeto_Gasto;\n")
        f.write("DELETE FROM dbo.Dim_Tiempo;\nGO\n\n")
        
        def write_inserts(df, table, columns, id_col=None):
            f.write(f"PRINT 'Insertando en {table}...';\n")
            if id_col:
                f.write(f"SET IDENTITY_INSERT {table} ON;\nGO\n")
            
            batch_size = 1000 # SQL Server soporta hasta 1000 filas por INSERT
            for i in range(0, len(df), batch_size):
                chunk = df.iloc[i:i+batch_size]
                if id_col:
                    cols_str = id_col + ", " + ", ".join(columns)
                else:
                    cols_str = ", ".join(columns)
                
                insert_stmt = f"INSERT INTO {table} ({cols_str}) VALUES\n"
                values = []
                for _, row in chunk.iterrows():
                    vals = []
                    if id_col:
                        vals.append(str(row[id_col]))
                    for c in columns:
                        is_num = c in ['Presupuesto_Inicial', 'Presupuesto_Vigente', 'Devengado_Aprobado', 'Periodo_Anio', 'Mes_Imputacion', 'ID_Institucion', 'ID_Programa', 'ID_Objeto_Gasto', 'ID_Tiempo']
                        vals.append(escape_sql(row[c], is_numeric=is_num))
                    values.append("(" + ", ".join(vals) + ")")
                
                insert_stmt += ",\n".join(values) + ";\nGO\n"
                f.write(insert_stmt)
                
            if id_col:
                f.write(f"SET IDENTITY_INSERT {table} OFF;\nGO\n\n")

        # Escribir Dimensiones
        inst_cols = ['Cod_Capitulo', 'Capitulo', 'Cod_SubCapitulo', 'SubCapitulo', 'Cod_Unidad_Ejecutora', 'Unidad_Ejecutora']
        write_inserts(dim_inst, 'dbo.Dim_Institucion', inst_cols, 'ID_Institucion')
        
        prog_cols = ['Cod_Programa', 'Programa', 'Cod_Producto', 'Producto', 'Cod_Proyecto', 'Proyecto', 'Cod_Actividad', 'Actividad']
        write_inserts(dim_prog, 'dbo.Dim_Programa', prog_cols, 'ID_Programa')
        
        og_cols = ['Cod_Tipo', 'Tipo', 'Cod_Concepto', 'Concepto', 'Cod_Cuenta', 'Cuenta', 'Cod_SubCuenta', 'SubCuenta', 'Cod_Auxiliar', 'Auxiliar']
        write_inserts(dim_og, 'dbo.Dim_Objeto_Gasto', og_cols, 'ID_Objeto_Gasto')
        
        # Dimensión Tiempo Estática
        tiempo_cols = ['Periodo_Anio', 'Mes_Imputacion', 'Nombre_Mes']
        write_inserts(dim_tiempo, 'dbo.Dim_Tiempo', tiempo_cols, 'ID_Tiempo')
        
        # Escribir Hechos
        fact_cols = ['ID_Institucion', 'ID_Programa', 'ID_Objeto_Gasto', 'ID_Tiempo', 'Presupuesto_Inicial', 'Presupuesto_Vigente', 'Devengado_Aprobado']
        write_inserts(fact, 'dbo.Fact_Ejecucion_Presupuestaria', fact_cols, None)
        
        # Actualizaciones Finales
        f.write("\n-- ==========================================================\n")
        f.write("-- ACTUALIZACIONES DE CLASIFICACIÓN\n")
        f.write("-- ==========================================================\n")
        f.write("IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('dbo.Dim_Institucion') AND name = 'Tipo_Institucion')\n")
        f.write("BEGIN\n    ALTER TABLE dbo.Dim_Institucion ADD Tipo_Institucion VARCHAR(50);\nEND\nGO\n\n")
        f.write("UPDATE dbo.Dim_Institucion SET Tipo_Institucion = 'Poder Legislativo' WHERE Cod_Capitulo IN ('101', '102');\n")
        f.write("UPDATE dbo.Dim_Institucion SET Tipo_Institucion = 'Poder Ejecutivo' WHERE Cod_Capitulo = '201';\n")
        f.write("UPDATE dbo.Dim_Institucion SET Tipo_Institucion = 'Ministerio Ejecutivo' WHERE Cod_Capitulo LIKE '20%' AND Cod_Capitulo <> '201';\n")
        f.write("UPDATE dbo.Dim_Institucion SET Tipo_Institucion = 'Otros Organismos' WHERE Tipo_Institucion IS NULL;\n")
        f.write("UPDATE dbo.Dim_Institucion SET Unidad_Ejecutora = Unidad_Ejecutora + ' (Sede Central)' WHERE Cod_Unidad_Ejecutora = '1';\nGO\n\n")
        f.write("ALTER TABLE dbo.Fact_Ejecucion_Presupuestaria WITH CHECK CHECK CONSTRAINT ALL;\nGO\n")
        f.write("PRINT 'Proceso DML completado exitosamente.';\n")
        
    print(f"ÉXITO: Script SQL {out_file} generado con todos los datos integrados.")

if __name__ == "__main__":
    process()
