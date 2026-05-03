import pandas as pd
import numpy as np
import os

# Paths
csv_dir = 'datos/originales/CSV'
output_path = 'powerbi/PresupuestoNacionalRD_PowerBI_Unificado.csv'

# Ensure output directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

print("Leyendo dataset institucional...")
# 1. Main Source: Institutional (2017-2025 Gastos)
df_inst = pd.read_csv(os.path.join(csv_dir, 'ejecucion-de-los-gastos-por-institucion.csv'), 
                     sep=';', encoding='latin-1')

# Standardize columns
df_inst = df_inst.rename(columns={
    'Ref Inst Seccion': 'Seccion_Institucional',
    'Capí­tulo': 'Capitulo',
    'SubCapitulo': 'Sub_Capitulo',
    'Unidad Ejecutora': 'Unidad_Ejecutora',
    'Programa': 'Programa',
    'Período': 'Periodo_Anio',
    'Mes.Hist.Imputación': 'Nombre_Mes',
    'Pres. Inicial': 'Presupuesto_Inicial',
    'Pres. Vigente Aprobado': 'Presupuesto_Vigente',
    'Devengado Aprobado': 'Devengado_Aprobado'
})

df_inst['Tipo_Presupuesto'] = 'Gasto'

print("Leyendo dataset de conceptos para aplicaciones financieras...")
# 2. Add Aplicaciones Financieras (2024-2025)
df_conc = pd.read_csv(os.path.join(csv_dir, 'gastos institucionales por concepto prespuestario.csv'), 
                      sep=';', encoding='latin-1')

df_apps = df_conc[df_conc['Ref CCP Tipo'] == 'Aplicaciones financieras'].copy()
df_apps = df_apps.rename(columns={
    'Ref Inst Sección': 'Seccion_Institucional',
    'Capí­tulo': 'Capitulo',
    'SubCapitulo': 'Sub_Capitulo',
    'Unidad Ejecutora': 'Unidad_Ejecutora',
    'Ref CCP Concepto': 'Programa', # Placeholder for apps
    'Período': 'Periodo_Anio',
    'Mes.Hist.Imputación': 'Nombre_Mes',
    'Pres. Inicial': 'Presupuesto_Inicial',
    'Pres. Vigente Aprobado': 'Presupuesto_Vigente',
    'Devengado Aprobado': 'Devengado_Aprobado'
})
df_apps['Tipo_Presupuesto'] = 'Aplicaciones Financieras'

# Keep only shared columns
cols_shared = [
    'Seccion_Institucional', 'Capitulo', 'Sub_Capitulo', 'Unidad_Ejecutora', 
    'Programa', 'Periodo_Anio', 'Nombre_Mes', 'Tipo_Presupuesto',
    'Presupuesto_Inicial', 'Presupuesto_Vigente', 'Devengado_Aprobado'
]

df = pd.concat([df_inst[cols_shared], df_apps[cols_shared]], ignore_index=True)

print("Mapeando Finalidad, Función y SubFunción...")

# 3. Robust mapping logic
def map_funcional(row):
    prog = str(row['Programa']).lower()
    cap = str(row['Capitulo']).lower()
    
    # 1. Intereses de la Deuda (Highest priority for "Intereses")
    if 'intereses' in prog or 'deuda' in cap:
        return "Intereses de la Deuda Pública", "Intereses y comisiones de deuda pública", "Intereses de deuda pública interna"
    
    # 2. Servicios Sociales
    if any(k in prog for k in ['educación', 'escolar', 'vivienda', 'salud', 'social', 'género', 'mujer', 'infancia']):
        if 'educación' in prog:
            return "Servicios Sociales", "Educación", "Educación primaria"
        if 'salud' in prog:
            return "Servicios Sociales", "Salud", "Salud pública"
        return "Servicios Sociales", "Protección social", "Asistencia social"
    
    # 3. Servicios Económicos
    if any(k in prog for k in ['carretera', 'vial', 'agrícola', 'infraestructura', 'energía', 'minería', 'transporte']):
        if 'agrícola' in prog:
            return "Servicios Económicos", "Agropecuaria, caza, pesca y silvicultura", "Fomento agropecuario"
        if 'vial' in prog or 'carretera' in prog:
            return "Servicios Económicos", "Transporte", "Infraestructura vial"
        return "Servicios Económicos", "Asuntos económicos, comerciales y laborales", "Gestión económica"
    
    # 4. Protección Medio Ambiente
    if 'medio ambiente' in prog or 'ambiental' in prog or 'biodiversidad' in prog:
        return "Protección del Medio Ambiente", "Protección de la biodiversidad y ordenación de desechos", "Gestión ambiental"
    
    # 5. Servicios Generales (Default)
    if 'defensa' in prog or 'militar' in prog:
        return "Servicios Generales", "Defensa nacional", "Operaciones militares"
    if 'justicia' in prog or 'policía' in prog or 'seguridad' in prog:
        return "Servicios Generales", "Justicia, orden público y seguridad", "Seguridad ciudadana"
    
    return "Servicios Generales", "Administración general", "Dirección y coordinación superior"

df[['Finalidad', 'Funcion', 'Sub_Funcion']] = df.apply(lambda r: pd.Series(map_funcional(r)), axis=1)

# 4. Fuente Financiamiento (Mocked as requested previously but could be better)
fuentes = ["Tesoro Nacional", "Ingresos Propios", "Crédito Externo", "Donaciones"]
weights = [0.7, 0.15, 0.1, 0.05]
np.random.seed(42)
df['Fuente_Financiamiento'] = np.random.choice(fuentes, size=len(df), p=weights)

# 5. Data Cleaning
df['Presupuesto_Inicial'] = pd.to_numeric(df['Presupuesto_Inicial'], errors='coerce').fillna(0)
df['Presupuesto_Vigente'] = pd.to_numeric(df['Presupuesto_Vigente'], errors='coerce').fillna(0)
df['Devengado_Aprobado'] = pd.to_numeric(df['Devengado_Aprobado'], errors='coerce').fillna(0)

# Fill NAs
df['Capitulo'] = df['Capitulo'].fillna('No especificado')
df['Sub_Capitulo'] = df['Sub_Capitulo'].fillna('No especificado')
df['Programa'] = df['Programa'].fillna('No especificado')

print(f"Dataset unificado creado con {len(df)} filas.")
print("Validación de Secciones:", df['Seccion_Institucional'].unique())
print("Validación de Finalidades:", df['Finalidad'].unique()[:5])

# Save
df.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f"Archivo guardado en: {output_path}")
