import os
import pandas as pd

def verificar_archivos():
    """
    Verifica que los archivos CSV limpios existan y tengan las columnas esperadas.
    """
    # Directorio de datos limpios
    base_path = r"C:\Users\Ricky\Universidad Autonoma de Santo Domingo\CI-MACDIA - Documents\Maestria IA y Ciencias de DAtos\2do modulo\INF-8235-C2 -Base de Datos I\Practica Final\datos\Limpios"
    
    # Definición de archivos y sus encabezados requeridos
    archivos_esperados = {
        "Dim_Institucion.csv": ["Cod_Capitulo", "Capitulo", "Cod_SubCapitulo", "SubCapitulo", "Cod_Unidad_Ejecutora", "Unidad_Ejecutora"],
        "Dim_Geografia.csv": ["Region", "Provincia", "Municipio"],
        "Dim_Programa.csv": ["Cod_Programa", "Programa", "Cod_Producto", "Producto", "Cod_Proyecto", "Proyecto", "Cod_Actividad", "Actividad"],
        "Dim_Objeto_Gasto.csv": ["Cod_Tipo", "Tipo", "Cod_Concepto", "Concepto", "Cod_Cuenta", "Cuenta", "Cod_SubCuenta", "SubCuenta", "Cod_Auxiliar", "Auxiliar"],
        "Fact_Ejecucion_Presupuestaria.csv": ["Cod_Capitulo", "Cod_SubCapitulo", "Cod_Unidad_Ejecutora", "Cod_Municipio", "Cod_Programa", "Cod_Producto", "Cod_Proyecto", "Cod_Actividad", "Cod_Tipo", "Cod_Concepto", "Cod_Cuenta", "Cod_SubCuenta", "Cod_Auxiliar", "Periodo_Anio", "Mes_Imputacion", "Presupuesto_Inicial", "Presupuesto_Vigente", "Devengado_Aprobado"]
    }

    print("=== Iniciando Verificación de Consistencia de Datos ===\n")

    if not os.path.exists(base_path):
        print(f"ERROR: No se encontró la carpeta: {base_path}")
        return

    for archivo, columnas in archivos_esperados.items():
        file_path = os.path.join(base_path, archivo)
        
        if os.path.exists(file_path):
            try:
                # Intentar leer el archivo
                df = pd.read_csv(file_path, nrows=0) # Solo leer encabezados para rapidez
                columnas_actuales = list(df.columns)
                
                # Verificar columnas
                faltantes = [col for col in columnas if col not in columnas_actuales]
                
                if not faltantes:
                    print(f"[OK] {archivo}: Archivo encontrado y columnas validadas.")
                else:
                    print(f"[ERROR] {archivo}: Faltan las siguientes columnas: {faltantes}")
            except Exception as e:
                print(f"[ERROR] {archivo}: No se pudo leer el archivo. Error: {e}")
        else:
            print(f"[ADVERTENCIA] {archivo}: El archivo no existe en la carpeta especificada.")

    print("\n=== Verificación Finalizada ===")

if __name__ == "__main__":
    verificar_archivos()
