import pandas as pd
import numpy as np
from IPython.display import display

df_encuestas = pd.read_csv("Project/data/processed/encuestas_unidas_limpias.csv")
df_runt = pd.read_csv("Project/data/processed/runt_2024_limpio.csv")


#Crear demanda total ponderada por departamento
df_encuestas_agrupado = df_encuestas.groupby("CODIGO_DESTINO").agg({
    "Fex_c": "sum"}).reset_index()

df_demanda_dept  = df_encuestas_agrupado[["CODIGO_DESTINO", "Fex_c"]].rename(columns={"Fex_c": "DEMANDA_TOTAL_PONDERADA"})

df_encuesta_por_departamento = df_encuestas.groupby("CODIGO_DESTINO").apply(
    lambda x: pd.Series({
        "GASTO_PROMEDIO_PONDERADO":
            (x["GASTO_TOTAL_EUROS"] * x["Fex_c"]).sum() / x["Fex_c"].sum()
    })
).reset_index()

df_gasto_dept = df_encuesta_por_departamento[["CODIGO_DESTINO", "GASTO_PROMEDIO_PONDERADO"]].rename(columns={"GASTO_PROMEDIO_PONDERADO": "GASTO_TOTAL_PONDERADO"})

# fusionar

df_encuestas_final = df_demanda_dept.merge(df_gasto_dept, on="CODIGO_DESTINO", how="left")

#Unir Runt con encuesta por departamento

df_fusion = df_runt.merge(df_encuestas_final, left_on="CODIGO_DEPARTAMENTO",
                          right_on="CODIGO_DESTINO", how="left")


#Crear columnas utiles en el nuevo dataframe

df_fusion_oferta = df_fusion.groupby("CODIGO_DEPARTAMENTO").agg({
    "CODIGO_RNT": "count"}).reset_index().rename(columns={"CODIGO_RNT": "OFERTA_TOTAL"})

df_fusion = df_fusion.merge(df_fusion_oferta, on="CODIGO_DEPARTAMENTO", how="left")

#Calcular ratio demanda/oferta
df_fusion["RATIO_DEMANDA_OFERTA"] = df_fusion["DEMANDA_TOTAL_PONDERADA"] / df_fusion["OFERTA_TOTAL"]

#Calcular gasto total por departamento
df_fusion["GASTO_TOTAL_DEPARTAMENTO"] = df_fusion["GASTO_TOTAL_PONDERADO"] * df_fusion["DEMANDA_TOTAL_PONDERADA"]

# Guardar resultado
df_fusion.to_csv("Project/data/processed/fusion_runt_encuestas.csv", index=False)
