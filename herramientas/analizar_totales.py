import pandas as pd
import os

def analyze_data():
    fact_path = 'datos/Limpios/Fact_Ejecucion_Presupuestaria.csv'
    inst_path = 'datos/Limpios/Dim_Institucion.csv'
    geo_path = 'datos/Limpios/Dim_Geografia.csv'
    gasto_path = 'datos/Limpios/Dim_Objeto_Gasto.csv'
    
    if not os.path.exists(fact_path):
        print("Error: Fact file not found")
        return

    fact = pd.read_csv(fact_path)
    inst = pd.read_csv(inst_path)
    gasto = pd.read_csv(gasto_path)
    
    # Global Totals
    total_vigente = fact['Presupuesto_Vigente'].sum()
    total_devengado = fact['Devengado_Aprobado'].sum()
    
    print(f"--- Global Totals ---")
    print(f"Total Presupuesto Vigente: {total_vigente:,.2f}")
    print(f"Total Devengado: {total_devengado:,.2f}")
    print(f"Porcentaje Ejecución: {(total_devengado/total_vigente)*100:.2f}%")
    
    # Group by Section (Joining with Inst to get Chapter names or similar)
    # Actually, let's just use the columns in Fact first
    
    # Convert columns to string for safe merge
    for col in ['Cod_Capitulo', 'Cod_SubCapitulo', 'Cod_Unidad_Ejecutora', 'Cod_Programa', 'Cod_Producto', 'Cod_Proyecto', 'Cod_Actividad']:
        fact[col] = fact[col].astype(str)
        if col in inst.columns:
            inst[col] = inst[col].astype(str)
    
    # Ensure Dim_Institucion is unique on join keys
    inst_clean = inst.groupby(['Cod_Capitulo', 'Cod_SubCapitulo', 'Cod_Unidad_Ejecutora']).first().reset_index()
    
    # We need to join to get names for the dashboard MOCK_DATA
    df = fact.merge(inst_clean, on=['Cod_Capitulo', 'Cod_SubCapitulo', 'Cod_Unidad_Ejecutora'], how='left')
    
    # Simple mapping for "Seccion" as per main.js logic
    def map_seccion(cap):
        cap = str(cap)
        if cap in ['101', '102', '201']: return "Administración central"
        if cap.startswith('5') or cap.startswith('6'): return "Instituciones públicas descentralizadas"
        return "Administración central"

    df['Seccion_Dashboard'] = df['Cod_Capitulo'].apply(map_seccion)
    
    print("\n--- Dashboard MOCK_DATA structure ---")
    # Group by Year and Section
    dashboard_data = df.groupby(['Periodo_Anio', 'Seccion_Dashboard'])[['Presupuesto_Vigente', 'Devengado_Aprobado']].sum().reset_index()
    # To millions
    dashboard_data['Presupuesto_Vigente'] = dashboard_data['Presupuesto_Vigente'] / 1000000
    dashboard_data['Devengado_Aprobado'] = dashboard_data['Devengado_Aprobado'] / 1000000
    
    for _, row in dashboard_data.iterrows():
        print(f'{{ "year": {int(row["Periodo_Anio"])}, "seccion": "{row["Seccion_Dashboard"]}", "finalidad": "Servicios Generales", "tipo_presupuesto": "Gasto", "fuente": "Tesoro Nacional", "concepto": "GASTOS", "budget": {row["Presupuesto_Vigente"]:.2f}, "spent": {row["Devengado_Aprobado"]:.2f} }},')


if __name__ == "__main__":
    analyze_data()
