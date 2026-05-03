import pandas as pd
import os

def validate_powerbi_data():
    pbi_path = 'powerbi/PresupuestoNacionalRD_PowerBI_Unificado.csv'
    fact_path = 'datos/Limpios/Fact_Ejecucion_Presupuestaria.csv'
    
    print("=== Validando Datos Power BI vs Datos Limpios ===")
    
    if not os.path.exists(pbi_path):
        print(f"ERROR: No se encuentra {pbi_path}")
        return

    # Read Power BI Unificado
    try:
        df_pbi = pd.read_csv(pbi_path)
        sum_vigente_pbi = df_pbi['EjecucionPresupuestaria_PresupuestoVigente'].sum()
        sum_devengado_pbi = df_pbi['EjecucionPresupuestaria_DevengadoAprobado'].sum()
    except Exception as e:
        print(f"Error al leer datos Power BI: {e}")
        return

    # Read Clean Fact
    try:
        df_clean = pd.read_csv(fact_path)
        sum_vigente_clean = df_clean['Presupuesto_Vigente'].sum()
        sum_devengado_clean = df_clean['Devengado_Aprobado'].sum()
    except Exception as e:
        print(f"Error al leer datos limpios: {e}")
        return

    print(f"  PBI Vigente:      {sum_vigente_pbi:,.2f}")
    print(f"  Clean Vigente:    {sum_vigente_clean:,.2f}")
    diff_vigente = abs(sum_vigente_pbi - sum_vigente_clean)
    print(f"  Diferencia Vigente: {diff_vigente:,.2f} ({'OK' if diff_vigente < 1000 else 'ERROR'})")

    print(f"  PBI Devengado:    {sum_devengado_pbi:,.2f}")
    print(f"  Clean Devengado:  {sum_devengado_clean:,.2f}")
    diff_devengado = abs(sum_devengado_pbi - sum_devengado_clean)
    print(f"  Diferencia Devengado: {diff_devengado:,.2f} ({'OK' if diff_devengado < 1000 else 'ERROR'})")

if __name__ == "__main__":
    validate_powerbi_data()
