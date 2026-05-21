import pandas as pd
import numpy as np
from IPython.display import display

def generar_gasto_promedio_por_categoria():
    """
    Pregunta 1: Calcula el gasto promedio por categoría de negocio y región.
    """
    df = pd.read_csv("Project/data/processed/fusion_runt_encuestas.csv")

    df_resultado = df.groupby(
        ["DEPARTAMENTO", "CATEGORIA_GENERAL"]
    ).agg(
        GASTO_PROMEDIO=("GASTO_TOTAL_PONDERADO", "mean"),
        NUMERO_NEGOCIOS=("CODIGO_RNT", "count"),
        DEMANDA=("DEMANDA_TOTAL_PONDERADA", "mean")
    ).reset_index()

    df_resultado = df_resultado.sort_values(
        by="GASTO_PROMEDIO",
        ascending=False
    )

    ruta_salida = "Project/outputs/pregunta_1_gasto.csv"
    df_resultado.to_csv(ruta_salida, index=False)

    return df_resultado


def demanda_vs_oferta_general_dept():
    """
    Pregunta 2: Calcula la relación entre demanda y oferta por departamento.
    """
    df = pd.read_csv("Project/data/processed/fusion_runt_encuestas.csv")
    df_resultado = df.groupby("DEPARTAMENTO").agg(
        DEMANDA_TOTAL_PONDERADA=("DEMANDA_TOTAL_PONDERADA", "first"),
        OFERTA_TOTAL=("CODIGO_RNT", "count"),
        RATIO_DEMANDA_OFERTA=("RATIO_DEMANDA_OFERTA", "first")
    ).reset_index()
    
    df_resultado["ESTADO"] = pd.cut(
        df_resultado["RATIO_DEMANDA_OFERTA"],
        bins=[0, 24, 49, 99, np.inf],
        labels=["BAJO", "MODERADO", "ALTO", "CRITICO"]
    )
    
    df_resultado = df_resultado.sort_values(by="RATIO_DEMANDA_OFERTA", ascending=False)
    
    df_resultado.to_csv("Project/outputs/pregunta_2_demanda_oferta.csv", index=False)
    
    return df_resultado


def construir_tabla_2_por_categoria():
    """
    Pregunta 3: Analiza la oferta por categoría de negocio en departamentos críticos.
    """
    df_base = pd.read_csv("Project/outputs/pregunta_2_demanda_oferta.csv")

    departamentos_criticos = df_base[
        df_base["ESTADO"].isin(["CRITICO", "ALTO"])
    ]["DEPARTAMENTO"].unique()

    df = pd.read_csv("Project/data/processed/fusion_runt_encuestas.csv")

    df_filtrado = df[df["DEPARTAMENTO"].isin(departamentos_criticos)]

    tabla_2 = df_filtrado.groupby(
        ["DEPARTAMENTO", "CATEGORIA_GENERAL"]
    ).agg(
        NUMERO_NEGOCIOS=("CODIGO_RNT", "count")
    ).reset_index()

    totales = df_filtrado.groupby("DEPARTAMENTO").agg(
        TOTAL_NEGOCIOS=("CODIGO_RNT", "count")
    ).reset_index()

    tabla_2 = tabla_2.merge(
        totales,
        on="DEPARTAMENTO",
        how="left"
    )

    tabla_2["% DEL TOTAL"] = (
        tabla_2["NUMERO_NEGOCIOS"] / tabla_2["TOTAL_NEGOCIOS"]
    ) * 100

    tabla_2 = tabla_2.sort_values(
        by=["DEPARTAMENTO", "NUMERO_NEGOCIOS"],
        ascending=[True, False]
    )

    tabla_2.to_csv(
        "Project/outputs/pregunta_2_por_categoria_2024.csv",
        index=False
    )

    return tabla_2


def pregunta_tres_concentracion_turistica():
    """
    Pregunta 4: Analiza la concentración de oferta turística por departamento.
    """
    df = pd.read_csv("Project/data/processed/fusion_runt_encuestas.csv")
    
    total_negocios = df["CODIGO_RNT"].count()
    
    concentracion = df.groupby("DEPARTAMENTO").agg(
        NUMERO_NEGOCIOS=("CODIGO_RNT", "count"),
        DEMANDA_DEPARTAMENTO=("DEMANDA_TOTAL_PONDERADA", "mean")
    ).reset_index()
    
    concentracion["% CONCENTRACION"] = (
        concentracion["NUMERO_NEGOCIOS"] / total_negocios) * 100
    
    concentracion = concentracion.sort_values(
        by="NUMERO_NEGOCIOS",
        ascending=False
    ).reset_index(drop=True)
    
    concentracion["CONCENTRACION_ACUMULADA"] = (
        concentracion["% CONCENTRACION"].cumsum()
    )
    
    concentracion.to_csv("Project/outputs/pregunta_3_concentracion_turistica.csv", index=False)
    return concentracion