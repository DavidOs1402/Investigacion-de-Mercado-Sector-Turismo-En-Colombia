# Análisis de Oportunidades de Negocio Turístico en Colombia

## Descripción

Este proyecto realiza un análisis profundo del mercado turístico colombiano mediante la combinación de dos fuentes de datos principales: el Registro Nacional de Turismo (RUNT) del período 2024-2026 y las Encuestas de Gasto Turístico del DANE. El objetivo es identificar oportunidades de negocio basadas en la relación entre demanda turística (personas que viajan y gastan dinero) y oferta disponible (número de negocios por categoría).

El análisis responde a cuatro preguntas estratégicas que ayudan a emprendedores y analistas a tomar decisiones informadas sobre dónde invertir en negocios turísticos en Colombia.

**Objetivo Principal:** Identificar brechas de mercado (demanda alta / oferta baja) que representen oportunidades de negocio rentables y viables en diferentes regiones y categorías del sector turístico.

---

## Estructura del Proyecto

```
Project/
├── main.py                          # Ejecuta todo el pipeline
├── data/
│   ├── raw/                         # Datos originales
│   │   ├── Registro_Nacional_de_Turismo_-_RNT_20260513.csv  ⚠️ Descargar manualmente (ver abajo)
│   │   ├── TURISMO I.csv
│   │   ├── TURISMO II.csv
│   │   ├── TURISMO III.csv
│   │   └── TURISMO IV.csv
│   └── processed/                   # Datos limpios y fusionados (generados al ejecutar)
│       ├── runt_2024_limpio.csv
│       ├── runt_2026_limpio.csv
│       ├── encuestas_unidas_limpias.csv
│       └── fusion_runt_encuestas.csv
├── src/
│   ├── cleaning.py                  # Limpieza y normalización de datos
│   ├── merging.py                   # Creación de features
│   ├── analysis.py                  # Análisis de preguntas clave
│   └── viz.py                       # Generación de visualizaciones
├── outputs/
│   ├── pregunta_1_gasto.csv
│   ├── pregunta_2_demanda_oferta.csv
│   ├── pregunta_2_por_categoria_2024.csv
│   ├── pregunta_3_concentracion_turistica.csv
│   └── graficos/                    # 4 gráficos PNG
├── notebooks/
│   └── 03_analisis_final_presentacion.ipynb
├── requirements.txt
└── README.md
```

---

## ⚠️ Descarga del RUNT (paso obligatorio)

El archivo del Registro Nacional de Turismo supera el límite de GitHub (110 MB) y **no está incluido en el repositorio**. Debes descargarlo manualmente:

1. Ve a: [https://www.datos.gov.co/Comercio-Industria-y-Turismo/Registro-Nacional-de-Turismo-RNT/thwd-ivmp/data_preview](https://www.datos.gov.co/Comercio-Industria-y-Turismo/Registro-Nacional-de-Turismo-RNT/thwd-ivmp/data_preview)
2. Haz clic en **Exportar → CSV**
3. Guarda el archivo en: `data/raw/`
4. Renómbralo exactamente como: `Registro_Nacional_de_Turismo_-_RNT_20260513.csv`

---

## Metodología

### Preguntas de Investigación

**1. ¿Cuál es el gasto promedio por región?**
   - **Objetivo:** Identificar dónde se generan mayores ingresos turísticos
   - **Variables:** Departamento, Gasto promedio ponderado
   - **Dataset:** Encuestas DANE 2024 + RUNT 2024
   - **Métrica:** Promedio de gasto turístico por departamento

**2. ¿Dónde hay DEMANDA ALTA pero OFERTA BAJA?**
   - **Objetivo:** Identificar brechas críticas de mercado (oportunidades de negocio)
   - **Variables:** Demanda (turistas ponderados), Oferta (# negocios), Ratio demanda/oferta
   - **Dataset:** RUNT 2024 + Encuestas DANE 2024
   - **Métrica:** Ratio demanda/oferta; clasificación por estado (CRÍTICO, ALTO, MODERADO, BAJO)

**3. ¿Dónde hay demanda alta pero oferta baja por categoría?**
   - **Objetivo:** Identificar qué tipos de negocios hacen falta en qué regiones
   - **Variables:** Departamento, Categoría general, # de negocios, % de distribución
   - **Dataset:** RUNT 2024 (filtrado por departamentos críticos)
   - **Métrica:** Distribución de oferta por región × categoría

**4. ¿Qué tan concentrada está la oferta turística?**
   - **Objetivo:** Determinar si el mercado es competitivo o centralizado
   - **Variables:** % de negocios por departamento, concentración acumulada
   - **Dataset:** RUNT 2024
   - **Métrica:** Distribución de Pareto (curva 80/20)

---

### Issues de Datos Esperables y Resueltos

| Problema | Solución |
|----------|----------|
| **Duplicados en RUNT:** Un CODIGO_RNT repetido en múltiples años | Deduplicar por CODIGO_RNT, mantener el más reciente |
| **Valores nulos en encuestas:** Respuestas incompletas | Eliminar filas con datos críticos faltantes |
| **Normalización de strings:** Categorías con inconsistencias | Aplicar .strip() en cleaning.py |
| **Conversión de moneda:** Encuestas en pesos, necesarias en euros | Aplicar TRM 4.300 pesos = 1 euro |
| **Agregación ponderada:** Encuestas tienen factor de expansión (Fex_c) | Usar Fex_c como peso en agregaciones |

---

### Transformaciones de Datos

**1. Limpieza RUNT (src/cleaning.py - limpiar_rnt)**
   - Filtrar por año (2024 / 2026)
   - Eliminar duplicados por CODIGO_RNT
   - Normalizar strings en CATEGORIA y SUB_CATEGORIA
   - Mapear categorías genéricas (ALOJAMIENTO, GASTRONOMÍA, TRANSPORTE, etc.)
   - **Resultado:** ~113.913 negocios únicos en 2024

**2. Limpieza Encuestas (src/cleaning.py - limpiar_encuestas)**
   - Consolidar 4 encuestas DANE en 1 dataset
   - Filtrar solo turismo interno (DESTINO_INTERNO_EXTERNO = 2)
   - Filtrar solo personas que viajaron (VIAJO_F_N = 1)
   - Convertir gasto a euros (GASTO_TOTAL ÷ 4.300)
   - **Resultado:** ~27.401 respuestas válidas

**3. Merging (fusion_runt_encuestas.csv)**
   - Agregar encuestas por CODIGO_DESTINO con ponderación (Fex_c)
   - Calcular DEMANDA_TOTAL_PONDERADA (suma de Fex_c)
   - Calcular GASTO_PROMEDIO_PONDERADO (promedio ponderado en euros)
   - Fusionar RUNT con datos agregados de encuestas
   - Crear métricas: OFERTA_TOTAL, RATIO_DEMANDA_OFERTA
   - **Resultado:** Dataset fusionado de 113.913 registros

**4. Análisis (src/analysis.py)**
   - **Pregunta 1:** Agrupar por DEPARTAMENTO, calcular gasto promedio ponderado
   - **Pregunta 2:** Calcular RATIO demanda/oferta, clasificar por ESTADO
   - **Pregunta 3:** Agrupar por DEPARTAMENTO × CATEGORIA en zonas críticas
   - **Pregunta 4:** Calcular concentración acumulada por departamento

---

### Gráficos Generados

**Pregunta 1: Gasto Promedio por Región**
- Barplot horizontal: Gasto promedio por departamento
- Interpretación: Identifica dónde se gasta más dinero en turismo

**Pregunta 2: Demanda vs Oferta**
- Scatter plot: Relación demanda vs oferta con colores por estado
- Interpretación: Visualiza las 4 zonas de mercado y etiqueta puntos críticos

**Pregunta 3: Oferta por Categoría**
- Heatmap: Región × Categoría de negocio (Top 15 departamentos)
- Interpretación: Muestra dónde faltan qué tipos de negocios

**Pregunta 4: Concentración de Oferta**
- Gráfico de línea acumulada: Concentración por departamento ordenados
- Interpretación: Identifica cuántos departamentos tienen el 80% de la oferta

---

## Resultados

### Pregunta 1 — Gasto Promedio por Región y Categoría

| Departamento | Gasto Promedio (€) | Oferta (negocios) |
|---|---|---|
| Amazonas | 735.33 | 484 |
| San Andrés y Providencia | 712.64 | 1.792 |
| Bogotá | media nacional | 13.965 |
| Cauca | ~93 | 727 |
| Vichada | ~93 | 83 |

**Hallazgos:**
- **Amazonas lidera** con €735 de gasto promedio por turista, seguido de cerca por **San Andrés y Providencia** con €712 — ambos impulsados por turismo de naturaleza y destinos insulares con alto valor percibido.
- La categoría **Agencias de Viajes** en Amazonas tiene el mismo gasto promedio que Alojamiento (€735), lo que indica que los turistas que llegan a destinos remotos gastan de forma transversal en todos los servicios.
- **Cauca y Vichada** presentan los menores gastos (~€93–109), reflejando turismo de bajo presupuesto o visitas cortas sin pernoctación.
- Las regiones con mayor infraestructura turística (Antioquia, Bogotá) tienen gasto individual moderado pero compensan con alto volumen de visitantes.

---

### Pregunta 2 — Demanda vs Oferta: Brechas de Mercado

| Estado | Departamentos | Ratio promedio |
|---|---|---|
| 🔴 CRÍTICO | Arauca, Cauca, Cesar, Tolima | 102 – 292 turistas por negocio |
| 🟠 ALTO | Guaviare, Córdoba, Chocó, Sucre, Cundinamarca, San Andrés, Caldas, Boyacá, Caquetá, Santander, Nariño, Meta | 49 – 96 turistas por negocio |
| 🟡 MODERADO | Quindío, Atlántico, Nde Santander, Antioquia, Valle, Magdalena, Risaralda, Guajira, Huila, Casanare | 33 – 47 turistas por negocio |
| 🟢 BAJO | Bogotá, Putumayo, Bolívar, Vichada, Guainía, Amazonas | 2 – 23 turistas por negocio |

**Hallazgos:**
- **Arauca es el caso más crítico del país** con un ratio de 291:1 — hay 291 turistas por cada negocio registrado. Con apenas 147 negocios para atender a más de 42.000 visitantes ponderados, la brecha es estructural.
- **Tolima sorprende** por su alto ratio (102:1) siendo un departamento relativamente grande y bien comunicado, lo que lo convierte en una oportunidad de inversión con menor riesgo logístico que Arauca.
- **Cundinamarca** aparece en estado ALTO (83:1) a pesar de tener 8.125 negocios, lo que refleja una demanda turística extraordinariamente alta impulsada por la proximidad a Bogotá.
- **Bogotá** tiene el ratio más bajo de los departamentos grandes (22:1), indicando un mercado relativamente bien abastecido comparado con el resto del país.
- **Vichada y Guainía** tienen ratios bajos (3-4:1) no por exceso de oferta sino por demanda casi inexistente — son mercados sin desarrollar, no saturados.

---

### Pregunta 3 — Oferta por Categoría en Departamentos Críticos y Altos

| Departamento | Categoría dominante | % del total | Categoría más escasa |
|---|---|---|---|
| Arauca | Alojamiento | 66.0% | Entretenimiento / Transporte (1.4% cada uno) |
| Boyacá | Alojamiento | 78.6% | Gastronomía (0.6%) |
| Caldas | Alojamiento | 71.4% | Entretenimiento (0.4%) |
| Caquetá | Alojamiento | 54.6% | — |

**Hallazgos:**
- **Alojamiento domina en absolutamente todos los departamentos** críticos y altos, representando entre el 55% y el 79% de la oferta total en cada región.
- **Gastronomía es la gran ausente**: en Boyacá representa solo el 0.6% de los negocios (25 establecimientos para más de 259.000 turistas ponderados). En Arauca apenas el 2.7%.
- **Entretenimiento y Parques** es prácticamente inexistente fuera de los grandes centros urbanos — en Arauca solo hay 2 negocios de esta categoría.
- **Agencias de Viajes** tienen presencia razonable (12–22%) en los departamentos críticos, lo que sugiere que la demanda se está canalizando pero sin suficiente oferta de servicios complementarios.
- La concentración en alojamiento indica que los emprendedores han respondido a la necesidad más básica del turista, pero han dejado sin cubrir la experiencia completa (gastronomía, actividades, entretenimiento).

---

### Pregunta 4 — Concentración de la Oferta Turística

| Umbral | Departamentos necesarios |
|---|---|
| 50% de la oferta nacional | 4 departamentos |
| 80% de la oferta nacional | 11 departamentos |
| 100% de la oferta nacional | 33 departamentos |

**Top 5 por concentración:**

| # | Departamento | Negocios | % Oferta | Acumulado |
|---|---|---|---|---|
| 1 | Antioquia | 22.681 | 19.9% | 19.9% |
| 2 | Bogotá | 13.965 | 12.3% | 32.2% |
| 3 | Bolívar | 10.817 | 9.5% | 41.7% |
| 4 | Cundinamarca | 8.125 | 7.1% | 48.8% |
| 5 | Magdalena | 7.906 | 6.9% | 55.7% |

**Hallazgos:**
- **Solo 4 departamentos concentran el 50% de toda la oferta turística nacional**: Antioquia, Bogotá, Bolívar y Cundinamarca. Esto refleja una distribución altamente desigual del tejido empresarial turístico.
- **Antioquia domina con casi el 20% de todos los negocios** del país — casi 1 de cada 5 negocios turísticos de Colombia está en ese departamento.
- **11 departamentos acumulan el 80% de la oferta**, dejando a los 22 departamentos restantes con apenas el 20% — muchos de ellos con alta demanda insatisfecha (casos CRÍTICO y ALTO).
- **Arauca, con ratio 291:1, tiene solo el 0.13% de la oferta nacional** — el contraste entre su demanda y su representación en el mercado es el más extremo del país.
- La curva de concentración sigue un patrón de Pareto pronunciado, indicando que el mercado no es competitivo ni distribuido: está capturado por pocas regiones con ventaja histórica de infraestructura.

---

## Conclusiones y Recomendaciones

### Top 3 Hallazgos
1. **Arauca es la mayor oportunidad del país**: ratio 291:1, prácticamente sin competencia, con demanda real documentada.
2. **Gastronomía y Entretenimiento están ausentes** en casi todas las zonas de alta demanda — el turista llega y duerme, pero no hay dónde comer ni qué hacer.
3. **El 80% del mercado está controlado por 11 departamentos**, lo que significa que el 60% del territorio colombiano opera con oferta mínima frente a demanda creciente.

### Top 3 Oportunidades de Negocio
1. **Restaurantes y gastronomía local en Arauca, Tolima y Cauca** — categoría casi inexistente con turistas que ya están llegando.
2. **Alojamiento boutique en Amazonas y San Andrés** — turistas de alto gasto (€700+) con oferta formal limitada en el segmento premium.
3. **Operadoras de experiencias y turismo de aventura en Boyacá y Santander** — alta demanda, buena infraestructura base, pero escasez de productos de entretenimiento estructurado.

### Limitaciones
- El RUNT solo registra negocios **formales** — la economía informal turística (especialmente en zonas rurales) no está capturada.
- La TRM utilizada es fija (4.300 COP/€) y no refleja variaciones del tipo de cambio real.
- Las Encuestas DANE tienen error muestral (~5%) y el factor de expansión Fex_c es una estimación estadística.
- El análisis es un corte estático de 2024 y no captura estacionalidad ni tendencias de crecimiento.

### Próximos Pasos
1. Incorporar datos RUNT 2022–2026 para análisis de tendencias por región
2. Cruzar con datos de informalidad laboral del DANE para ajustar la oferta real
3. Construir un modelo predictivo de demanda por departamento usando variables macroeconómicas

---

## Instalación y Ejecución

### Requisitos
- Python 3.12+

### Pasos

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/DavidOs1402/Inestigacion-de-Mercado-Sector-Turismo-En-Colombia.git
   cd Inestigacion-de-Mercado-Sector-Turismo-En-Colombia
   ```

2. **Crear y activar entorno virtual:**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Descargar el RUNT** (ver sección ⚠️ arriba)

5. **Ejecutar pipeline completo:**
   ```bash
   python main.py
   ```

6. **Verificar salidas:**
   - Datos procesados: `data/processed/`
   - Análisis CSV: `outputs/`
   - Gráficos PNG: `outputs/graficos/`

---

## Autor

**David Oswaldo Herrera Riaño**  
Fecha de conclusión: 21 de mayo de 2026

---

## Licencia

Este proyecto es de uso educativo y está disponible bajo licencia abierta.
