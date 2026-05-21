import pandas as pd
import numpy as np
from src.cleaning import limpiar_rnt, limpiar_encuestas
import src.analysis as analysis
import src.viz as viz

def main():
    """
    Ejecuta el pipeline completo de análisis turístico:
    limpieza de datos, análisis y generación de visualizaciones.
    """
    
    print("=" * 70)
    print("INICIANDO PIPELINE DE ANÁLISIS TURÍSTICO")
    print("=" * 70 + "\n")
    
    # Limpieza de datos RNT
    print("FASE 1: LIMPIEZA DE DATOS")
    print("-" * 70)
    
    ruta = "Project/data/raw/Registro_Nacional_de_Turismo_-_RNT_20260513.csv"
    
    df_2024 = limpiar_rnt(ruta, 2024)
    df_2026 = limpiar_rnt(ruta, 2026)
    
    print("Limpieza RNT completada\n")
    
    # Limpieza de encuestas
    print("FASE 2: LIMPIEZA DE ENCUESTAS")
    print("-" * 70)
    
    df_encuestas = limpiar_encuestas()
    
    print("Limpieza de encuestas completada\n")
    
    # Preparación de datos
    print("FASE 3: FUSIÓN DE DATOS")
    print("-" * 70)
    
    print("Datos listos para análisis\n")
    
    # Análisis
    print("FASE 4: ANÁLISIS DE DATOS")
    print("-" * 70)
    
    df_resultado_1 = analysis.generar_gasto_promedio_por_categoria()
    print("Pregunta 1: Gasto promedio por categoría\n")
    
    df_resultado_2 = analysis.demanda_vs_oferta_general_dept()
    print("Pregunta 2: Demanda vs Oferta\n")
    
    df_resultado_3 = analysis.construir_tabla_2_por_categoria()
    print("Pregunta 3: Oferta por categoría\n")
    
    df_resultado_4 = analysis.pregunta_tres_concentracion_turistica()
    print("Pregunta 4: Concentración turística\n")
    
    # Resumen
    print("RESUMEN DE RESULTADOS")
    print("-" * 70)
    print("\n1. GASTO PROMEDIO POR CATEGORÍA Y REGIÓN:")
    print(df_resultado_1.head())
    
    print("\n2. DEMANDA VS OFERTA POR DEPARTAMENTO:")
    print(df_resultado_2.head())
    
    print("\n3. OFERTA POR CATEGORÍA:")
    print(df_resultado_3.head())
    
    print("\n4. CONCENTRACIÓN TURÍSTICA:")
    print(df_resultado_4.head())
    
    # Visualizaciones
    print("\n" + "=" * 70)
    print("FASE 5: GENERACIÓN DE VISUALIZACIONES")
    print("=" * 70 + "\n")
    
    viz.viz_pregunta_1()
    viz.viz_pregunta_2()
    viz.viz_pregunta_3()
    viz.viz_pregunta_4()
    
    # Finalización
    print("=" * 70)
    print("PIPELINE COMPLETADO EXITOSAMENTE")
    print("=" * 70)
    print("\nResultados guardados en:")
    print("  Datos procesados: Project/data/processed/")
    print("  Análisis: Project/outputs/")
    print("  Gráficos: Project/outputs/graficos/")
    

if __name__ == "__main__":
    main()


