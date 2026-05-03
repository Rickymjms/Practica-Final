import pandas as pd
import json
import os

def generate_json_summary():
    pbi_path = 'powerbi/PresupuestoNacionalRD_PowerBI_Unificado.csv'
    output_path = 'datos/resumen_dashboard.json'
    
    if not os.path.exists(pbi_path):
        print(f"Error: No se encuentra {pbi_path}")
        return

    print("Cargando datos unificados...")
    df = pd.read_csv(pbi_path)
    
    # Fill NAs
    df['Seccion_Institucional'] = df['Seccion_Institucional'].fillna('No especificada')
    df['Finalidad'] = df['Finalidad'].fillna('No especificada')
    df['Funcion'] = df['Funcion'].fillna('No especificada')

    print("Calculando agregaciones...")
    
    # 1. Totales Generales
    totales_generales = {
        "presupuesto_inicial": float(df['Presupuesto_Inicial'].sum()),
        "presupuesto_vigente": float(df['Presupuesto_Vigente'].sum()),
        "total_devengado": float(df['Devengado_Aprobado'].sum()),
        "variacion_neta": float(df['Presupuesto_Vigente'].sum() - df['Presupuesto_Inicial'].sum()),
        "porcentaje_ejecucion": float((df['Devengado_Aprobado'].sum() / df['Presupuesto_Vigente'].sum() * 100) if df['Presupuesto_Vigente'].sum() > 0 else 0)
    }

    # 2. Resumen por Año
    resumen_anual = df.groupby('Periodo_Anio').agg({
        'Presupuesto_Inicial': 'sum',
        'Presupuesto_Vigente': 'sum',
        'Devengado_Aprobado': 'sum'
    }).reset_index()
    
    resumen_anual['variacion'] = resumen_anual['Presupuesto_Vigente'] - resumen_anual['Presupuesto_Inicial']
    resumen_anual['pct_ejecucion'] = (resumen_anual['Devengado_Aprobado'] / resumen_anual['Presupuesto_Vigente'] * 100).fillna(0)
    
    lista_anual = resumen_anual.to_dict('records')

    # 3. Resumen por Finalidad (Top)
    resumen_finalidad = df.groupby('Finalidad').agg({
        'Presupuesto_Vigente': 'sum',
        'Devengado_Aprobado': 'sum'
    }).sort_values('Presupuesto_Vigente', ascending=False).reset_index().to_dict('records')

    # 4. Resumen por Sección
    resumen_seccion = df.groupby('Seccion_Institucional').agg({
        'Presupuesto_Vigente': 'sum',
        'Devengado_Aprobado': 'sum'
    }).reset_index().to_dict('records')

    # 5. Top 10 Funciones Prioritarias
    resumen_funcion = df.groupby(['Finalidad', 'Funcion']).agg({
        'Presupuesto_Vigente': 'sum'
    }).sort_values('Presupuesto_Vigente', ascending=False).head(10).reset_index().to_dict('records')

    # Compilar Resumen Final
    resumen_final = {
        "metadata": {
            "proyecto": "Análisis del Presupuesto Nacional RD",
            "autor": "Lic. Manuel Mañana Santana",
            "ultima_actualizacion": "Mayo 2026",
            "fuente": "DIGEPRES"
        },
        "indicadores_globales": totales_generales,
        "evolucion_anual": lista_anual,
        "distribucion_finalidad": resumen_finalidad,
        "distribucion_seccion": resumen_seccion,
        "prioridades_gasto": resumen_funcion
    }

    # Guardar JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(resumen_final, f, indent=4, ensure_ascii=False)
    
    print(f"Resumen JSON generado exitosamente en: {output_path}")

if __name__ == "__main__":
    generate_json_summary()
