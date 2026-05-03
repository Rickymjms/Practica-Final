import pandas as pd
import json

def generate_dashboard_data():
    pbi_path = 'powerbi/PresupuestoNacionalRD_PowerBI_Unificado.csv'
    df = pd.read_csv(pbi_path)
    
    # Fill NaNs in columns we group by
    df['Concepto'] = df['Concepto'].fillna('GASTOS')
    df['Capitulo'] = df['Capitulo'].fillna('No especificado')
    
    group_cols = [
        'Periodo_Anio', 
        'Seccion_Institucional', 
        'Capitulo',
        'Finalidad', 
        'Tipo_Presupuesto', 
        'Fuente_Financiamiento', 
        'Concepto'
    ]
    
    agg = df.groupby(group_cols).agg({
        'Presupuesto_Inicial': 'sum',
        'Presupuesto_Vigente': 'sum',
        'Devengado_Aprobado': 'sum'
    }).reset_index()
    
    # Rename columns to match requirements
    agg.columns = ['year', 'seccion', 'capitulo', 'finalidad', 'tipo', 'fuente', 'concepto', 'initial', 'budget', 'spent']
    
    # Convert to Millions (MM) with high precision (4 decimals) for internal calculations
    # but the dashboard will format to 2 decimals for display.
    # Actually, let's keep them in full RD$ to avoid precision issues in sums, 
    # or use high decimal places.
    agg['initial'] = (agg['initial'] / 1000000).round(4)
    agg['budget'] = (agg['budget'] / 1000000).round(4)
    agg['spent'] = (agg['spent'] / 1000000).round(4)
    
    # Filter out rows with zero values to keep JSON small
    agg = agg[(agg['initial'] != 0) | (agg['budget'] != 0) | (agg['spent'] != 0)]
    
    # Validation check
    total_2024 = agg[agg['year'] == 2024]['budget'].sum() * 1000000
    total_2025 = agg[agg['year'] == 2025]['budget'].sum() * 1000000
    print(f"// Validation 2024: {total_2024:,.2f} (Target: 1,868,118,635,354.31)")
    print(f"// Validation 2025: {total_2025:,.2f} (Target: 2,068,892,291,237.19)")
    
    # Convert to JSON records
    records = agg.to_dict('records')
    
    # Output to stdout to be captured or used to update main.js
    print("const MOCK_DATA = " + json.dumps(records, indent=2, ensure_ascii=False) + ";")
    
    # Print other constants
    print("const SECCIONES = " + json.dumps(sorted(df['Seccion_Institucional'].unique().tolist()), ensure_ascii=False) + ";")
    print("const FINALIDADES = " + json.dumps(sorted(df['Finalidad'].unique().tolist()), ensure_ascii=False) + ";")
    print("const FUENTES = " + json.dumps(sorted(df['Fuente_Financiamiento'].unique().tolist()), ensure_ascii=False) + ";")
    print("const CONCEPTOS = " + json.dumps(sorted(df['Concepto'].unique().tolist()), ensure_ascii=False) + ";")

if __name__ == "__main__":
    generate_dashboard_data()
