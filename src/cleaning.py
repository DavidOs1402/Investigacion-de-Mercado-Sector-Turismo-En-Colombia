import pandas as pd
import numpy as np
from IPython.display import display


# ==============================
# MAPA DE CATEGORÍAS (GLOBAL)
# ==============================

mapa_categorias = {

    # ALOJAMIENTO
    "ESTABLECIMIENTOS DE ALOJAMIENTO TURÍSTICO": "ALOJAMIENTO",
    "VIVIENDAS TURÍSTICAS": "ALOJAMIENTO",
    "EMPRESAS DE TIEMPO COMPARTIDO Y MULTIPROPIEDAD": "ALOJAMIENTO",
    "COMPAÑÍAS DE INTERCAMBIO VACACIONAL": "ALOJAMIENTO",
    "OTROS TIPOS DE HOSPEDAJE TURÍSTICOS NO PERMANENTES": "ALOJAMIENTO",

    # GASTRONOMÍA
    "ESTABLECIMIENTOS DE GASTRONOMÍA": "GASTRONOMÍA",
    "ESTABLECIMIENTOS DE GASTRONOMÍA Y SIMILARES": "GASTRONOMÍA",
    "BARES": "GASTRONOMÍA",

    # AGENCIAS DE VIAJES
    "AGENCIAS DE VIAJES": "AGENCIAS DE VIAJES",
    "OFICINAS DE REPRESENTACION TURÍSTICA": "AGENCIAS DE VIAJES",
    "EMPRESAS CAPTADORAS DE AHORRO PARA VIAJES": "AGENCIAS DE VIAJES",

    # TRANSPORTE
    "ARRENDADORES DE VEHÍCULOS PARA TURISMO NACIONAL E INTERNACIONAL": "TRANSPORTE",
    "EMPRESAS DE TRANSPORTE TERRESTRE AUTOMOTOR": "TRANSPORTE",

    # ENTRETENIMIENTO
    "PARQUES TEMÁTICOS": "ENTRETENIMIENTO/PARQUES",
    "CONCESIONARIOS DE SERVICIOS TURÍSTICOS EN PARQUE": "ENTRETENIMIENTO/PARQUES",

    # SERVICIOS TURÍSTICOS
    "GUIAS DE TURISMO": "SERVICIOS TURÍSTICOS",
    "OPERADORES PROFESIONALES DE CONGRESOS FERIAS Y CONVENCIONES": "SERVICIOS TURÍSTICOS",
    "USUARIOS INDUSTRIALES OPERADORES O DESARROLLADORES DE SERVICIOS TURISTICOS DE LAS ZONAS FRANCAS": "SERVICIOS TURÍSTICOS",
    "ORGANIZADORES DE BODA DESTINO": "SERVICIOS TURÍSTICOS",
    "OPERADORES DE PLATAFORMAS ELECTRÓNICAS O DIGITALES DE SERVICIOS TURÍSTICOS": "SERVICIOS TURÍSTICOS",
}


# ==============================
# FUNCIÓN DE LIMPIEZA RNT
# ==============================

def limpiar_rnt(ruta, año):
    
    df = pd.read_csv(ruta)

    print("="*60)
    print(f"PROCESANDO AÑO {año}")
    print("="*60)

    # Filtrar año
    df = df[df["AÑO"] == año]

    # Deduplicar
    df = df.drop_duplicates(subset="CODIGO_RNT", keep="first")

    # Limpiar strings
    df.columns = df.columns.str.strip()

    df["CATEGORIA"] = df["CATEGORIA"].astype(str).str.strip()
    df["SUB_CATEGORIA"] = df["SUB_CATEGORIA"].astype(str).str.strip()

    # Crear categoría general
    df["CATEGORIA_GENERAL"] = df["CATEGORIA"].map(mapa_categorias)

    # Seleccionar columnas finales
    df_final = df[
        [
            "CODIGO_RNT",
            "RAZON_SOCIAL_ESTABLECIMIENTO",
            "DEPARTAMENTO",
            "CODIGO_DEPARTAMENTO",
            "MUNICIPIO",
            "SUB_CATEGORIA",
            "CATEGORIA_GENERAL"
        ]
    ]

    print(f"Shape final {año}: {df_final.shape}")
    display(df_final.head())

    # Guardar
    salida = f"Project/data/processed/runt_{año}_limpio.csv"
    df_final.to_csv(salida, index=False)

    print(f"Guardado en: {salida}")

    return df_final


# ==============================
# FUNCIÓN DE LIMPIEZA ENCUESTAS
# ==============================

def limpiar_encuestas():
    """
    Carga, limpia y procesa los datos de encuestas turísticas
    """
    
    # =========================================================
    # CARGA Y UNIÓN DE ENCUESTAS
    # =========================================================

    encuesta_uno = "Project/data/raw/TURISMO I.csv"
    encuesta_dos = "Project/data/raw/TURISMO II.csv"
    encuesta_tres = "Project/data/raw/TURISMO III.csv"
    encuesta_cuatro = "Project/data/raw/TURISMO IV.csv"

    encuestas_unidas = pd.concat([
        pd.read_csv(encuesta_uno, sep="|"),
        pd.read_csv(encuesta_dos, sep="|"),
        pd.read_csv(encuesta_tres, sep="|"),
        pd.read_csv(encuesta_cuatro, sep="|")
    ], ignore_index=True)

    print("Shape inicial:")
    print(encuestas_unidas.shape)


    # =========================================================
    # LIMPIEZA DE NOMBRES DE COLUMNAS
    # =========================================================

    encuestas_unidas.columns = (
        encuestas_unidas.columns
        .str.strip()
    )

    print("\nColumnas cargadas correctamente")


    # =========================================================
    # ELIMINAR COLUMNAS INNECESARIAS
    # =========================================================

    columnas_a_eliminar = [

        # ---------------- Variables técnicas ----------------
        'Secuencia_encuesta',
        'Orden',

        # ---------------- Variables redundantes ----------------
        'P7571S1A1', 'P7571S1A2', 'P7571S1A3',
        'P7573S3',
        'P7571S2', 'P7571S2A1',
        'P7579',
        'P7580S3', 'P7580S1',
        'P7573S2',

        # ---------------- Variables alojamiento ----------------
        'P7574S1A1',
        'P7574S5', 'P7574S5A1',
        'P7574S2', 'P7574S2A1',
        'P7574S8', 'P7574S8A1',
        'P7574S4', 'P7574S4A1',
        'P7574S10', 'P7574S10A1',
        'P7574S3', 'P7574S3A1',
        'P7574S7', 'P7574S7A2',

        # ---------------- Plataforma digital ----------------
        'P15001',

        # ---------------- Paquetes turísticos ----------------
        'P7576',
        'P7576S1',
        'P7576S2',
        'P7576S3',
        'P7576S5',

        # ---------------- Servicios incluidos ----------------
        'P7577S1',
        'P7577S2',
        'P7577S3',
        'P7577S4',
        'P7577S5',
        'P7577S6',
        'P7577S7',

        # ---------------- Variables auxiliares de gasto ----------------
        'P7581S1A2', 'P7581S1A3',
        'P7581S9A1', 'P7581S9A2', 'P7581S9A3',
        'P7581S10A1', 'P7581S10A2', 'P7581S10A3',
        'P7581S3A1', 'P7581S3A2', 'P7581S3A3',
        'P7581S4A1', 'P7581S4A2', 'P7581S4A3',
        'P7581S5A1', 'P7581S5A2', 'P7581S5A3',
        'P7581S6A1', 'P7581S6A2', 'P7581S6A3',
        'P7581S7A1', 'P7581S7A2', 'P7581S7A3',
        'P7581S8A1', 'P7581S8A2', 'P7581S8A3',
        'P7581S11A1', 'P7581S11A2'
    ]

    encuestas_limpias = encuestas_unidas.drop(
        columns=columnas_a_eliminar,
        errors="ignore"
    )

    print("\nShape después de eliminar columnas:")
    print(encuestas_limpias.shape)


    # =========================================================
    # RENOMBRAR COLUMNAS
    # =========================================================

    diccionario_maestro = {

        # ---------------- Variables principales ----------------
        'P7570': 'VIAJO_F_N',
        'P7571S1': 'DESTINO_INTERNO_EXTERNO',
        'P7573S1': 'CODIGO_DESTINO',

        # ---------------- Fechas ----------------
        'P549': 'FECHA_INICIO',
        'P549S1': 'FECHA_FIN',

        # ---------------- Alojamiento ----------------
        'P7574S1': 'TIPO_ALOJAMIENTO_PRINCIPAL',

        # ---------------- Tipo de turismo ----------------
        'P7580': 'TIPO_TURISMO',
        'P7575': 'MEDIO_TRANSPORTE',

        # ---------------- Gastos ----------------
        'P7578': 'GASTO_TOTAL',

        'P7581S1': 'GASTO_TRANSPORTE_PRINCIPAL',
        'P7581S1A1': 'GASTO_PEAJES_GASOLINA',

        'P7581S9': 'GASTO_TRANSPORTE_INTERNO',

        'P7581S10': 'GASTO_ALOJAMIENTO',

        'P7581S3': 'GASTO_ALIMENTACION',

        'P7581S4': 'GASTO_ACTIVIDADES_TOURS',

        'P7581S5': 'GASTO_COMPRAS_RECUERDOS',

        'P7581S6': 'GASTO_PAQUETE_TURISTICO',

        'P7581S7': 'GASTO_SERVICIOS_GUIA',

        'P7581S8': 'GASTO_SEGUROS_VIAJE',

        'P7581S11': 'GASTO_OTROS_RUBROS'
    }

    encuestas_limpias = encuestas_limpias.rename(
        columns=diccionario_maestro
    )

    print("\nColumnas renombradas correctamente")


    # =========================================================
    # CONVERTIR VARIABLES NUMÉRICAS
    # =========================================================

    encuestas_limpias["GASTO_TOTAL"] = pd.to_numeric(
        encuestas_limpias["GASTO_TOTAL"],
        errors="coerce"
    )


    # =========================================================
    # ELIMINAR COLUMNAS DE GASTOS DESAGREGADOS
    # =========================================================

    columnas_gastos = [

        'GASTO_TRANSPORTE_PRINCIPAL',
        'GASTO_PEAJES_GASOLINA',
        'GASTO_TRANSPORTE_INTERNO',
        'GASTO_ALOJAMIENTO',
        'GASTO_ALIMENTACION',
        'GASTO_ACTIVIDADES_TOURS',
        'GASTO_COMPRAS_RECUERDOS',
        'GASTO_PAQUETE_TURISTICO',
        'GASTO_SERVICIOS_GUIA',
        'GASTO_SEGUROS_VIAJE',
        'GASTO_OTROS_RUBROS'
    ]

    encuestas_limpias = encuestas_limpias.drop(
        columns=columnas_gastos,
        errors="ignore"
    )


    # =========================================================
    # FILTROS DE LIMPIEZA
    # =========================================================

    # Mantener solo personas que sí viajaron
    encuestas_limpias = encuestas_limpias[
        encuestas_limpias["VIAJO_F_N"] == 1
    ]

    # Mantener solo turismo interno en Colombia
    encuestas_limpias = encuestas_limpias[
        encuestas_limpias["DESTINO_INTERNO_EXTERNO"] == 2
    ]

    # Mantener gastos turísticos razonables
    encuestas_limpias = encuestas_limpias[
        encuestas_limpias["GASTO_TOTAL"] >= 10000
    ]


    # =========================================================
    # CONVERSIÓN A EUROS
    # =========================================================

    TRM = 4300

    encuestas_limpias["GASTO_TOTAL_EUROS"] = (
        encuestas_limpias["GASTO_TOTAL"] / TRM
    ).round(2)


    # =========================================================
    # INFORMACIÓN FINAL
    # =========================================================

    print("\nShape final:")
    print(encuestas_limpias.shape)

    print("\nSuma del factor de expansión:")
    print(encuestas_limpias["Fex_c"].sum())

    print("\nVista previa:")
    display(encuestas_limpias.head())


    # =========================================================
    # EXPORTAR DATASET LIMPIO
    # =========================================================

    ruta_salida = "Project/data/processed/encuestas_unidas_limpias.csv"

    encuestas_limpias.to_csv(
        ruta_salida,
        index=False
    )


    display(encuestas_limpias.info())

    encuestas_limpias["FECHA_INICIO"] = pd.to_datetime(encuestas_limpias["FECHA_INICIO"])
    encuestas_limpias["FECHA_FIN"] = pd.to_datetime(encuestas_limpias["FECHA_FIN"])
    display(encuestas_limpias.info())
    print(encuestas_limpias.columns)
    print(f"\nArchivo exportado correctamente en:\n{ruta_salida}")
    
    return encuestas_limpias