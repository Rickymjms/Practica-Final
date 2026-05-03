import pandas as pd

def clean_dim(path, keys):
    df = pd.read_csv(path)
    # Ensure all keys are strings to avoid mix-up
    for k in keys:
        df[k] = df[k].astype(str)
    count_before = len(df)
    df = df.drop_duplicates(subset=keys)
    df.to_csv(path, index=False, encoding='utf-8-sig')
    print(f"{path}: {count_before} -> {len(df)} rows.")

clean_dim('datos/Limpios/Dim_Institucion.csv', ['Cod_Capitulo', 'Cod_SubCapitulo', 'Cod_Unidad_Ejecutora'])
clean_dim('datos/Limpios/Dim_Geografia.csv', ['Cod_Municipio'])
clean_dim('datos/Limpios/Dim_Programa.csv', ['Cod_Programa', 'Cod_Producto', 'Cod_Proyecto', 'Cod_Actividad'])
clean_dim('datos/Limpios/Dim_Objeto_Gasto.csv', ['Cod_Tipo', 'Cod_Concepto', 'Cod_Cuenta', 'Cod_SubCuenta', 'Cod_Auxiliar'])
clean_dim('datos/Limpios/Dim_Tiempo.csv', ['Periodo_Anio', 'Mes_Imputacion'])
