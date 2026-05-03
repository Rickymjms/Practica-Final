import pandas as pd
import os

def clean_and_export():
    print("Iniciando proceso de limpieza y exportación...")
    
    # Path to original Excel
    excel_path = 'datos/originales/ejecucion-de-los-gastos-por-institucion.xlsx'
    if not os.path.exists(excel_path):
        print(f"Error: No se encuentra {excel_path}")
        return

    # Load original data
    df = pd.read_excel(excel_path)
    
    # Standardize columns for our model
    # Model uses: Cod_Capitulo, Capitulo, Cod_SubCapitulo, SubCapitulo, Cod_Unidad_Ejecutora, Unidad_Ejecutora
    # Excel has: 'Cod.Capítulo', 'Capítulo', 'Cod.SubCapitulo', 'SubCapitulo', 'Cod.Unidad Ejecutora', 'Unidad Ejecutora'
    
    # Use column position or robust renaming
    df.columns = [c.replace('\xad', '') for c in df.columns]
    
    mapping = {
        'Cod.Capítulo': 'Cod_Capitulo',
        'Capítulo': 'Capitulo',
        'Cod.SubCapitulo': 'Cod_SubCapitulo',
        'SubCapitulo': 'SubCapitulo',
        'Cod.Unidad Ejecutora': 'Cod_Unidad_Ejecutora',
        'Unidad Ejecutora': 'Unidad_Ejecutora',
        'Cod.Programa': 'Cod_Programa',
        'Programa': 'Programa',
        'Cod.Producto': 'Cod_Producto',
        'Producto': 'Producto',
        'Cod.Proyecto': 'Cod_Proyecto',
        'Proyecto': 'Proyecto',
        'Cod.Actividad / Obra': 'Cod_Actividad',
        'Actividad / Obra': 'Actividad',
        'Período': 'Periodo_Anio',
        'Cod.Mes.Hist.Imputación': 'Mes_Imputacion',
        'Mes.Hist.Imputación': 'Nombre_Mes',
        'Pres. Inicial': 'Presupuesto_Inicial',
        'Pres. Vigente Aprobado': 'Presupuesto_Vigente',
        'Devengado Aprobado': 'Devengado_Aprobado'
    }
    
    df = df.rename(columns=mapping)
    
    # Missing columns in this Excel that are in our model: Geografia, Objeto_Gasto
    # We might need to mock some or get them from other files.
    # But for Totals, this file is the main one.
    
    # Export Dim_Institucion
    dim_inst = df[['Cod_Capitulo', 'Capitulo', 'Cod_SubCapitulo', 'SubCapitulo', 'Cod_Unidad_Ejecutora', 'Unidad_Ejecutora']].drop_duplicates()
    dim_inst.to_csv('datos/Limpios/Dim_Institucion.csv', index=False, encoding='utf-8-sig')
    print("Dim_Institucion.csv exportado.")

    # Export Dim_Programa
    dim_prog = df[['Cod_Programa', 'Programa', 'Cod_Producto', 'Producto', 'Cod_Proyecto', 'Proyecto', 'Cod_Actividad', 'Actividad']].drop_duplicates()
    dim_prog.to_csv('datos/Limpios/Dim_Programa.csv', index=False, encoding='utf-8-sig')
    print("Dim_Programa.csv exportado.")

    # Export Dim_Tiempo
    dim_tiempo = df[['Periodo_Anio', 'Mes_Imputacion', 'Nombre_Mes']].drop_duplicates()
    dim_tiempo.to_csv('datos/Limpios/Dim_Tiempo.csv', index=False, encoding='utf-8-sig')
    print("Dim_Tiempo.csv exportado.")

    # Fact_Ejecucion_Presupuestaria
    # We'll add some dummy IDs for missing dims if needed, or just the codes
    fact = df[['Cod_Capitulo', 'Cod_SubCapitulo', 'Cod_Unidad_Ejecutora', 'Cod_Programa', 'Cod_Producto', 'Cod_Proyecto', 'Cod_Actividad', 'Periodo_Anio', 'Mes_Imputacion', 'Presupuesto_Inicial', 'Presupuesto_Vigente', 'Devengado_Aprobado']]
    
    # Add dummy cols for missing dims to keep consistency with model
    fact['Cod_Municipio'] = '1' # Default
    fact['Cod_Tipo'] = '2'
    fact['Cod_Concepto'] = '1'
    fact['Cod_Cuenta'] = '1'
    fact['Cod_SubCuenta'] = '1'
    fact['Cod_Auxiliar'] = '1'
    
    fact.to_csv('datos/Limpios/Fact_Ejecucion_Presupuestaria.csv', index=False, encoding='utf-8-sig')
    print("Fact_Ejecucion_Presupuestaria.csv exportado con totales reales.")

if __name__ == "__main__":
    clean_and_export()
