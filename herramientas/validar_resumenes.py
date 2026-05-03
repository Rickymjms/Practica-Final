import pandas as pd
import os

def get_summary_totals(df):
    """
    Tries to find the totals in a Pivot Table style dataframe.
    """
    # Look for "Total general" in the first column
    total_row = df[df.iloc[:, 0].astype(str).str.contains('Total general', na=False, case=False)]
    
    if not total_row.empty:
        # Assuming columns are roughly in order: Name, Inicial, Vigente, Devengado
        # Let's find columns that have "Vigente" and "Devengado" in their names
        vigente_col = [col for col in df.columns if 'Vigente' in str(col)]
        devengado_col = [col for col in df.columns if 'Devengado' in str(col)]
        
        if vigente_col and devengado_col:
            return total_row[vigente_col[0]].values[0], total_row[devengado_col[0]].values[0]
        else:
            # Try by index if names are "Unnamed"
            # Unnamed: 2 is usually Vigente, Unnamed: 3 is Devengado based on previous observations
            return total_row.iloc[0, 2], total_row.iloc[0, 3]
    
    # If no Total general, try to sum numeric-looking rows in the first column
    # (Assuming they are the years)
    df_copy = df.copy()
    df_copy.iloc[:, 0] = pd.to_numeric(df_copy.iloc[:, 0], errors='coerce')
    df_years = df_copy.dropna(subset=[df_copy.columns[0]])
    
    # Again, try to find columns
    vigente_col = [col for col in df.columns if 'Vigente' in str(col)]
    devengado_col = [col for col in df.columns if 'Devengado' in str(col)]
    
    if vigente_col and devengado_col:
        return df_years[vigente_col[0]].sum(), df_years[devengado_col[0]].sum()
    else:
        return df_years.iloc[:, 2].sum(), df_years.iloc[:, 3].sum()

def validate_summaries():
    summary_path = 'datos/originales/Resumen_datos_ejecucion_presupuestaria.xlsx'
    csv_dir = 'datos/originales/CSV'
    
    comparisons = [
        {'sheet': 'resumen-ejecucion-institucion', 'csv': 'ejecucion-de-los-gastos-por-institucion.csv', 'name': 'Institucion'},
        {'sheet': 'Resumen-ejecucion-por-funcion', 'csv': 'ejecucion-de-los-gastos-por-funcion.csv', 'name': 'Funcion'},
        {'sheet': 'Resumen-Concepto-prespuesta', 'csv': 'gastos institucionales por concepto prespuestario.csv', 'name': 'Concepto'}
    ]

    print("=== Validando Resúmenes vs Originales (CSV) ===")
    
    for comp in comparisons:
        print(f"\nAnalizando {comp['name']}...")
        
        try:
            # Read without header first to find the real header row
            df_raw = pd.read_excel(summary_path, sheet_name=comp['sheet'], header=None)
            
            # Find the row containing 'Etiquetas de fila'
            header_row_idx = -1
            for i, row in df_raw.iterrows():
                if 'Etiquetas de fila' in str(row[0]):
                    header_row_idx = i
                    break
            
            if header_row_idx != -1:
                df_summary = pd.read_excel(summary_path, sheet_name=comp['sheet'], header=header_row_idx + 1)
            else:
                df_summary = df_raw # Fallback
            
            sum_vigente_res, sum_devengado_res = get_summary_totals(df_summary)
                
        except Exception as e:
            print(f"Error al leer hoja {comp['sheet']}: {e}")
            continue

        # Read Original CSV
        csv_path = os.path.join(csv_dir, comp['csv'])
        try:
            # We use usecols with lambda to handle potential BOM or weird spaces in CSV headers
            df_csv = pd.read_csv(csv_path, sep=';', encoding='latin-1')
            
            # Identify columns by content if needed, but names usually work with latin-1
            # Filter for Concepto
            if comp['name'] == 'Concepto':
                df_csv = df_csv[df_csv['Período'].isin([2024, 2025])]
            
            sum_vigente_csv = df_csv['Pres. Vigente Aprobado'].sum()
            sum_devengado_csv = df_csv['Devengado Aprobado'].sum()
        except Exception as e:
            print(f"Error al leer CSV {comp['csv']}: {e}")
            continue

        print(f"  Summary Vigente:  {sum_vigente_res:,.2f}")
        print(f"  Original Vigente: {sum_vigente_csv:,.2f}")
        diff_vigente = abs(sum_vigente_res - sum_vigente_csv)
        print(f"  Diferencia Vigente: {diff_vigente:,.2f} ({'OK' if diff_vigente < 1000 else 'ERROR'})")

        print(f"  Summary Devengado:  {sum_devengado_res:,.2f}")
        print(f"  Original Devengado: {sum_devengado_csv:,.2f}")
        diff_devengado = abs(sum_devengado_res - sum_devengado_csv)
        print(f"  Diferencia Devengado: {diff_devengado:,.2f} ({'OK' if diff_devengado < 1000 else 'ERROR'})")

if __name__ == "__main__":
    validate_summaries()
