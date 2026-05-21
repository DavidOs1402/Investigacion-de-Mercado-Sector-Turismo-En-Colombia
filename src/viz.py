import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Pregunta 1: Gasto promedio por región

def viz_pregunta_1():
    """Genera visualización de gasto promedio por región."""
    print("Pregunta 1: Gasto promedio por región")
    
    df = pd.read_csv('Project/outputs/pregunta_1_gasto.csv')
    gasto_por_dept = df.groupby('DEPARTAMENTO')['GASTO_PROMEDIO'].mean().sort_values(ascending=True)
    
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.barplot(x=gasto_por_dept.values, y=gasto_por_dept.index, palette='viridis', ax=ax)
    
    ax.set_title('Gasto Promedio por Región', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Gasto Promedio ($)', fontsize=12)
    ax.set_ylabel('Región (Departamento)', fontsize=12)
    ax.grid(axis='x', alpha=0.3)
    
    interpretacion = (
        "Interpretación:\n"
        "El Amazonas, SAn Andres y Providencia lidera con el gasto promedio más alto (~$750 y ~712), "
        "mientras que Cauca y Vichada presentan los menores (~$93-$109). "
        "Las regiones con mayor infraestructura turística concentran mayores gastos promedio."
    )
    fig.text(0.1, -0.08, interpretacion, fontsize=10, style='italic', wrap=True)
    
    plt.tight_layout()
    plt.savefig('Project/outputs/graficos/pregunta_1_comparacion.png', dpi=300, bbox_inches='tight')

    print("Completada\n")


# Pregunta 2: Demanda vs Oferta

def viz_pregunta_2():
    """Genera visualización de demanda vs oferta por región."""
    print("Pregunta 2: Demanda vs Oferta")
    
    df = pd.read_csv('Project/outputs/pregunta_2_demanda_oferta.csv')
    
    mediana_oferta = df["OFERTA_TOTAL"].median()
    mediana_demanda = df["DEMANDA_TOTAL_PONDERADA"].median()

    def clasificar_estado(row):
        oferta = row["OFERTA_TOTAL"]
        demanda = row["DEMANDA_TOTAL_PONDERADA"]
        if demanda > mediana_demanda and oferta < mediana_oferta:
            return "CRÍTICO"
        elif demanda > mediana_demanda and oferta >= mediana_oferta:
            return "ALTO"
        elif demanda <= mediana_demanda and oferta >= mediana_oferta:
            return "SOBREOFERTA"
        else:
            return "BAJO"

    df["ESTADO"] = df.apply(clasificar_estado, axis=1)

    fig, ax = plt.subplots(figsize=(13, 8))
    
    sns.scatterplot(
        data=df,
        x="OFERTA_TOTAL",
        y="DEMANDA_TOTAL_PONDERADA",
        hue="ESTADO",
        size="RATIO_DEMANDA_OFERTA",
        sizes=(100, 600),
        palette={'CRÍTICO': 'red', 'ALTO': 'orange', 'SOBREOFERTA': 'yellow', 'BAJO': 'green'},
        ax=ax
    )

    ax.axvline(mediana_oferta, linestyle="--", color='gray', alpha=0.5, linewidth=2)
    ax.axhline(mediana_demanda, linestyle="--", color='gray', alpha=0.5, linewidth=2)

    criticos = df[df["ESTADO"] == "CRÍTICO"]
    for _, row in criticos.iterrows():
        ax.text(row["OFERTA_TOTAL"], row["DEMANDA_TOTAL_PONDERADA"], 
                row["DEPARTAMENTO"], fontsize=9, fontweight='bold')

    ax.set_title('Demanda vs Oferta Turística por Región', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Oferta Total (# negocios)', fontsize=12)
    ax.set_ylabel('Demanda Total Ponderada', fontsize=12)
    ax.grid(alpha=0.3)
    
    interpretacion = (
        "Interpretación:\n"
        "Las zonas rojas (CRÍTICO) requieren más oferta: Arauca, Cauca, Cesar y Tolima tienen alta demanda pero oferta insuficiente. "
        "El tamaño de los puntos indica el desequilibrio (ratio demanda/oferta)."
    )
    fig.text(0.1, -0.08, interpretacion, fontsize=10, style='italic', wrap=True)
    
    plt.tight_layout()
    plt.savefig("Project/outputs/graficos/pregunta_2_relacion.png", dpi=300, bbox_inches='tight')
    
    print("Completada\n")


# Pregunta 3: Oferta por categoría

def viz_pregunta_3():
    """Genera heatmap de oferta por región y categoría."""
    print("Pregunta 3: Oferta por región y categoría")
    
    df = pd.read_csv('Project/outputs/pregunta_1_gasto.csv')
    
    df_pivot = df.pivot_table(
        values='NUMERO_NEGOCIOS',
        index='DEPARTAMENTO',
        columns='CATEGORIA_GENERAL',
        aggfunc='sum',
        fill_value=0
    )
    
    top_depts = df.groupby('DEPARTAMENTO')['DEMANDA'].sum().nlargest(15).index
    df_pivot = df_pivot.loc[top_depts]
    
    fig, ax = plt.subplots(figsize=(12, 9))
    sns.heatmap(
        df_pivot,
        annot=True,
        fmt='.0f',
        cmap='YlOrRd',
        cbar_kws={'label': '# Negocios'},
        ax=ax
    )
    
    ax.set_title('Oferta de Negocios Turísticos: Región × Categoría (Top 15)', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Categoría de Negocio', fontsize=12)
    ax.set_ylabel('Región (Departamento)', fontsize=12)
    
    interpretacion = (
        "Interpretación:\n"
        "Alojamiento domina en todas las regiones (columna más intensa). "
        "Antioquia y Cundinamarca lideran en cantidad total de negocios. "
        "Categorías como Entretenimiento muestran brecha de oferta en múltiples regiones."
    )
    fig.text(0.1, -0.08, interpretacion, fontsize=10, style='italic', wrap=True)
    
    plt.tight_layout()
    plt.savefig('Project/outputs/graficos/pregunta_3_heatmap.png', dpi=300, bbox_inches='tight')

    print("Completada\n")


# Pregunta 4: Concentración de oferta

def viz_pregunta_4():
    """Genera visualización de concentración acumulada de oferta turística."""
    print("Pregunta 4: Concentración de oferta turística")
    
    df = pd.read_csv('Project/outputs/pregunta_3_concentracion_turistica.csv')
    df_sorted = df.dropna(subset=['CONCENTRACION_ACUMULADA']).sort_values('CONCENTRACION_ACUMULADA')
    
    fig, ax = plt.subplots(figsize=(13, 7))
    
    ax.fill_between(
        range(len(df_sorted)),
        df_sorted['CONCENTRACION_ACUMULADA'].values,
        alpha=0.3,
        color='steelblue'
    )
    ax.plot(
        range(len(df_sorted)),
        df_sorted['CONCENTRACION_ACUMULADA'].values,
        marker='o',
        linewidth=2.5,
        color='steelblue',
        markersize=6
    )
    
    ax.axhline(y=80, color='r', linestyle='--', linewidth=2, label='80% Concentración', alpha=0.7)
    ax.axhline(y=50, color='orange', linestyle='--', linewidth=2, label='50% Concentración', alpha=0.7)
    
    ax.set_title('Concentración Acumulada de la Oferta Turística', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Número de Departamentos (ordenados)', fontsize=12)
    ax.set_ylabel('% Concentración Acumulada', fontsize=12)
    ax.set_ylim(0, 105)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=11)
    
    interpretacion = (
        "Interpretación:\n"
        f"Solo {len(df_sorted[df_sorted['CONCENTRACION_ACUMULADA'] <= 80])} departamentos concentran el 80% de la oferta. "
        "La oferta turística está altamente concentrada en pocas regiones, "
        "lo que indica oportunidades de desarrollo en zonas menos servidas."
    )
    fig.text(0.1, -0.10, interpretacion, fontsize=10, style='italic', wrap=True)
    
    plt.tight_layout()
    plt.savefig('Project/outputs/graficos/pregunta_4_distribucion.png', dpi=300, bbox_inches='tight')

    print("Completada\n")