import pandas as pd
import os

def validate_clean_data():
    fact_path = 'datos/Limpios/Fact_Ejecucion_Presupuestaria.csv'
    original_excel_path = 'datos/originales/ejecucion-de-los-gastos-por-institucion.xlsx'
    
    print("=== Validando Datos Limpios vs Originales ===")
    
    if not os.path.exists(fact_path):
        print(f"ERROR: No se encuentra {fact_path}")
        return

    # Read Clean Fact
    try:
        df_clean = pd.read_csv(fact_path)
        sum_vigente_clean = df_clean['Presupuesto_Vigente'].sum()
        sum_devengado_clean = df_clean['Devengado_Aprobado'].sum()
    except Exception as e:
        print(f"Error al leer datos limpios: {e}")
        return

    # Read Original Excel (Institutional)
    try:
        df_orig = pd.read_excel(original_excel_path)
        sum_vigente_orig = df_orig['Pres. Vigente Aprobado'].sum()
        sum_devengado_orig = df_orig['Devengado Aprobado'].sum()
    except Exception as e:
        print(f"Error al leer datos originales: {e}")
        return

    print(f"  Clean Vigente:    {sum_vigente_clean:,.2f}")
    print(f"  Original Vigente: {sum_vigente_orig:,.2f}")
    diff_vigente = abs(sum_vigente_clean - sum_vigente_orig)
    print(f"  Diferencia Vigente: {diff_vigente:,.2f} ({'OK' if diff_vigente < 1000 else 'ERROR'})")

    print(f"  Clean Devengado:    {sum_devengado_clean:,.2f}")
    print(f"  Original Devengado: {sum_devengado_orig:,.2f}")
    diff_devengado = abs(sum_devengado_clean - sum_devengado_orig)
    print(f"  Diferencia Devengado: {diff_devengado:,.2f} ({'OK' if diff_devengado < 1000 else 'ERROR'})")

if __name__ == "__main__":
    validate_clean_data()
