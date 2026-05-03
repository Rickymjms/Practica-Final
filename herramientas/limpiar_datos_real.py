import pandas as pd
import os

def clean_and_export():
    print("Iniciando proceso de limpieza y exportación integral...")
    
    # Ensure output directory exists
    output_dir = 'datos/limpios'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 1. Process Institutional Data (Main Fact and Dimensions)
    excel_inst = 'datos/originales/ejecucion-de-los-gastos-por-institucion.xlsx'
    if os.path.exists(excel_inst):
        df_inst = pd.read_excel(excel_inst)
        df_inst.columns = [c.replace('\xad', '') for c in df_inst.columns]
        
        mapping_inst = {
            'Cod.Capítulo': 'Cod_Capitulo', 'Capítulo': 'Capitulo',
            'Cod.SubCapitulo': 'Cod_SubCapitulo', 'SubCapitulo': 'SubCapitulo',
            'Cod.Unidad Ejecutora': 'Cod_Unidad_Ejecutora', 'Unidad Ejecutora': 'Unidad_Ejecutora',
            'Cod.Programa': 'Cod_Programa', 'Programa': 'Programa',
            'Cod.Producto': 'Cod_Producto', 'Producto': 'Producto',
            'Cod.Proyecto': 'Cod_Proyecto', 'Proyecto': 'Proyecto',
            'Cod.Actividad / Obra': 'Cod_Actividad', 'Actividad / Obra': 'Actividad',
            'Período': 'Periodo_Anio', 'Cod.Mes.Hist.Imputación': 'Mes_Imputacion',
            'Mes.Hist.Imputación': 'Nombre_Mes',
            'Pres. Inicial': 'Presupuesto_Inicial', 'Pres. Vigente Aprobado': 'Presupuesto_Vigente',
            'Devengado Aprobado': 'Devengado_Aprobado'
        }
        df_inst = df_inst.rename(columns=mapping_inst)
        
        # Dim_Institucion
        dim_inst = df_inst[['Cod_Capitulo', 'Capitulo', 'Cod_SubCapitulo', 'SubCapitulo', 'Cod_Unidad_Ejecutora', 'Unidad_Ejecutora']].drop_duplicates()
        dim_inst.to_csv(f'{output_dir}/Dim_Institucion.csv', index=False, encoding='utf-8-sig')
        print("Dim_Institucion.csv exportado.")

        # Dim_Programa
        dim_prog = df_inst[['Cod_Programa', 'Programa', 'Cod_Producto', 'Producto', 'Cod_Proyecto', 'Proyecto', 'Cod_Actividad', 'Actividad']].drop_duplicates()
        dim_prog.to_csv(f'{output_dir}/Dim_Programa.csv', index=False, encoding='utf-8-sig')
        print("Dim_Programa.csv exportado.")

        # Dim_Tiempo (Periodo)
        dim_tiempo = df_inst[['Periodo_Anio', 'Mes_Imputacion', 'Nombre_Mes']].drop_duplicates()
        dim_tiempo.to_csv(f'{output_dir}/Dim_Tiempo.csv', index=False, encoding='utf-8-sig')
        print("Dim_Tiempo.csv exportado.")

        # Fact_Ejecucion_Presupuestaria (Partial)
        fact = df_inst[['Cod_Capitulo', 'Cod_SubCapitulo', 'Cod_Unidad_Ejecutora', 'Cod_Programa', 'Cod_Producto', 'Cod_Proyecto', 'Cod_Actividad', 'Periodo_Anio', 'Mes_Imputacion', 'Presupuesto_Inicial', 'Presupuesto_Vigente', 'Devengado_Aprobado']]
        fact['Cod_Municipio'] = '1' # Default
        fact['Cod_Tipo'] = '2'
        fact['Cod_Concepto'] = '1'
        fact['Cod_Cuenta'] = '1'
        fact['Cod_SubCuenta'] = '1'
        fact['Cod_Auxiliar'] = '1'
        fact.to_csv(f'{output_dir}/Fact_Ejecucion_Presupuestaria.csv', index=False, encoding='utf-8-sig')
        print("Fact_Ejecucion_Presupuestaria.csv exportado.")
    else:
        print(f"Advertencia: No se encontró {excel_inst}")

    # 2. Process Object of Expenditure (CCP)
    excel_ccp = 'datos/originales/gastos institucionales por concepto prespuestario.xlsx'
    if os.path.exists(excel_ccp):
        df_ccp = pd.read_excel(excel_ccp)
        df_ccp.columns = [c.replace('\xad', '') for c in df_ccp.columns]
        
        mapping_ccp = {
            'Cod.Ref CCP Tipo': 'Cod_Tipo', 'Ref CCP Tipo': 'Tipo',
            'Cod.Ref CCP Concepto': 'Cod_Concepto', 'Ref CCP Concepto': 'Concepto',
            'Cod.Ref CCP Cuenta': 'Cod_Cuenta', 'Ref CCP Cuenta': 'Cuenta',
            'Cod.Ref CCP SubCuenta': 'Cod_SubCuenta', 'Ref CCP SubCuenta': 'SubCuenta',
            'Cod.Ref CCP Aux': 'Cod_Auxiliar', 'Ref CCP Aux': 'Auxiliar'
        }
        df_ccp = df_ccp.rename(columns=mapping_ccp)
        
        dim_og = df_ccp[['Cod_Tipo', 'Tipo', 'Cod_Concepto', 'Concepto', 'Cod_Cuenta', 'Cuenta', 'Cod_SubCuenta', 'SubCuenta', 'Cod_Auxiliar', 'Auxiliar']].drop_duplicates()
        dim_og.to_csv(f'{output_dir}/Dim_Objeto_Gasto.csv', index=False, encoding='utf-8-sig')
        print("Dim_Objeto_Gasto.csv exportado.")
    else:
        print(f"Advertencia: No se encontró {excel_ccp}")

    # 3. Create Static Dim_Geografia (to satisfy consistency)
    geo_data = [
        # Cibao Norte
        {'Region': 'Cibao Norte', 'Provincia': 'Santiago'},
        {'Region': 'Cibao Norte', 'Provincia': 'Puerto Plata'},
        {'Region': 'Cibao Norte', 'Provincia': 'Espaillat'},
        # Cibao Sur
        {'Region': 'Cibao Sur', 'Provincia': 'La Vega'},
        {'Region': 'Cibao Sur', 'Provincia': 'Monseñor Nouel'},
        {'Region': 'Cibao Sur', 'Provincia': 'Sánchez Ramírez'},
        # Cibao Nordeste
        {'Region': 'Cibao Nordeste', 'Provincia': 'Duarte'},
        {'Region': 'Cibao Nordeste', 'Provincia': 'Hermanas Mirabal'},
        {'Region': 'Cibao Nordeste', 'Provincia': 'María Trinidad Sánchez'},
        {'Region': 'Cibao Nordeste', 'Provincia': 'Samaná'},
        # Cibao Noroeste
        {'Region': 'Cibao Noroeste', 'Provincia': 'Valverde'},
        {'Region': 'Cibao Noroeste', 'Provincia': 'Santiago Rodríguez'},
        {'Region': 'Cibao Noroeste', 'Provincia': 'Monte Cristi'},
        {'Region': 'Cibao Noroeste', 'Provincia': 'Dajabón'},
        # Valdesia
        {'Region': 'Valdesia', 'Provincia': 'San Cristóbal'},
        {'Region': 'Valdesia', 'Provincia': 'Peravia'},
        {'Region': 'Valdesia', 'Provincia': 'San José de Ocoa'},
        # Enriquillo
        {'Region': 'Enriquillo', 'Provincia': 'Barahona'},
        {'Region': 'Enriquillo', 'Provincia': 'Pedernales'},
        {'Region': 'Enriquillo', 'Provincia': 'Bahoruco'},
        {'Region': 'Enriquillo', 'Provincia': 'Independencia'},
        # El Valle
        {'Region': 'El Valle', 'Provincia': 'San Juan'},
        {'Region': 'El Valle', 'Provincia': 'Elías Piña'},
        {'Region': 'El Valle', 'Provincia': 'Azua'},
        # Yuma
        {'Region': 'Yuma', 'Provincia': 'La Altagracia'},
        {'Region': 'Yuma', 'Provincia': 'La Romana'},
        {'Region': 'Yuma', 'Provincia': 'El Seibo'},
        # Higuamo
        {'Region': 'Higuamo', 'Provincia': 'San Pedro de Macorís'},
        {'Region': 'Higuamo', 'Provincia': 'Hato Mayor'},
        {'Region': 'Higuamo', 'Provincia': 'Monte Plata'},
        # Ozama
        {'Region': 'Ozama', 'Provincia': 'Distrito Nacional'},
        {'Region': 'Ozama', 'Provincia': 'Santo Domingo'}
    ]
    dim_geo = pd.DataFrame(geo_data)
    dim_geo.to_csv(f'{output_dir}/Dim_Geografia.csv', index=False, encoding='utf-8-sig')
    print("Dim_Geografia.csv (con 32 provincias y 10 regiones) exportado.")

    print("\nProceso de limpieza completado exitosamente.")

if __name__ == "__main__":
    clean_and_export()
