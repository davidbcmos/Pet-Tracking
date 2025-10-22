# 🐾 PET TRACKING – Intelligent Emotional Interpretation System

### Big Data & AI Project | AWS | Streaming | ML | Power BI
[🇪🇸 Español](./README.es.md) | [🇬🇧 English](./README.md)

---

## 🚀 Overview

**Pet Tracking** es un sistema inteligente diseñado para **interpretar en tiempo real las emociones y necesidades básicas de mascotas (perros y gatos)** mediante el análisis de señales fisiológicas, vocalizaciones y comportamiento físico.  
Su arquitectura combina **Big Data, Machine Learning e IoT** para ofrecer una **comunicación emocional animal-humano** basada en datos objetivos y visualizaciones analíticas.

---

## 🎯 Objetivos

- Analizar grandes volúmenes de datos estructurados y no estructurados (sensores, audio, video, reportes).
- Identificar patrones de conducta y estados emocionales.
- Traducir emociones en mensajes comprensibles para cuidadores y veterinarios.
- Generar visualizaciones interactivas en **Power BI**.
- Prevenir estrés, ansiedad o enfermedades mediante **alertas inteligentes**.

---

## 🧠 Arquitectura General

```plaintext
[Wearables / Cámaras / Micrófonos / Reportes]
↓
(Ingesta de Datos)
├── AWS Glue / S3 (Batch)
├── AWS Kinesis / Lambda / Firehose (Streaming)
↓
(Almacenamiento)
Amazon S3 / Redshift / Athena
↓
(Procesamiento)
Amazon EMR (Spark) / Redshift ML
↓
(Visualización)
Power BI Dashboard
```

---

## 🗂️ Recolección de Datos

| Fuente | Tipo de Datos |
|---------|----------------|
| **Wearables (Collares, Sensores)** | Ritmo cardíaco, temperatura, actividad física, GPS |
| **Micrófonos Ambientales** | Vocalizaciones, tono emocional, frecuencia de sonidos |
| **Cámaras** | Postura corporal, gestos, patrones de movimiento |
| **Reportes de Cuidadores** | Etiquetas emocionales: alegría, ansiedad, hambre, dolor, etc. |

---

## 🔄 Ingesta de Datos

### 🧩 Batch (Diaria)
- **Origen:** Reportes e historiales de sensores.
- **Servicios AWS:**  
  - `Amazon S3`  
  - `AWS Glue Studio`, `Glue Data Catalog`, `Glue Data Quality`  
- **Transformaciones:**  
  - Normalización de tipos y nombres de columnas.  
  - Clasificación de niveles de riesgo (`alert_level`) y actividad (`activity_level`).  
  - Validación de calidad con `Glue Data Quality`.

### ⚡ Streaming (Tiempo Real)
- **Origen:** Dispositivos IoT enviando datos vitales y vocalizaciones.
- **Servicios AWS:**  
  - `Amazon Kinesis Data Streams`  
  - `AWS Lambda` (transformación JSON → Parquet)  
  - `Amazon Firehose` (entrega a S3)
- **Formato:** Parquet comprimido con Snappy, particionado por año/mes/día.

---

## 🧱 Almacenamiento de Datos

Estructura del bucket principal:  
`s3://pet-tracking-data-bucket/`

```plaintext
├── raw/
│   ├── batch/ (Datos crudos por lotes)
│   ├── stream/ (Datos en tiempo real)
├── processed/ (Datos transformados)
├── firehose-output/ (Salida automática de Firehose)
├── warehouse/
│   ├── athena/
│   └── redshift/
├── dashboards/
│   ├── powerbi/
│   └── data_snapshots/
├── logs/
├── archive/
└── s3-management/ (Lifecycle rules)
```

### Políticas de Ciclo de Vida en S3

| Carpeta | Acción | Tiempo |
|----------|---------|--------|
| `raw/batch/` | Mover a Glacier | 30 días |
| `raw/stream/` | Eliminar | 7 días |
| `processed/` | Eliminar | 90 días |
| `firehose-output/` | Eliminar | 60 días |

---

## ⚙️ Procesamiento Analítico

### 🔸 AWS EMR (Apache Spark)
- Limpieza, agregación y enriquecimiento de datos.
- Scripts en `PySpark` almacenados en `emr/scripts/`.
- Resultados exportados a `emr/results/`.
- Configuración escalable mediante `bootstrap actions` y `roles` dedicados.

### 🔸 Redshift + Redshift ML
- Integración con S3 vía **Spectrum**.
- Entrenamiento de modelo **K-Means** sobre métricas numéricas:
  - `age`, `heart_rate_bpm`, `activity_steps`, `gps_lat`, `gps_lon`.
- Predicción de clústeres de comportamiento emocional.
- Resultados disponibles para dashboards o alertas.

### 🔸 Athena
- Consultas SQL sobre tablas particionadas en Parquet.
- Ejemplo de query:
  ```sql
  SELECT emotion, COUNT(*) AS freq
  FROM pet_sounds_data_cleaned
  GROUP BY emotion
  ORDER BY freq DESC;
  ```

---

## 📊 Visualización (Power BI)

**Dashboard 1 – Análisis de Datos y Emociones**
- Volumen de audios registrados.
- Emoción más común.
- Evolución de emociones en el tiempo.
- Frecuencia máxima por emoción.
- Tabla con espectrogramas asociados.

**Indicadores Clave (DAX):**
```DAX
Total_Audios = COUNT('pet-sound-data'[IDAudio])

Emocion_Mas_Comun = 
CALCULATE(
    MAXX(
        TOPN(1, 
            SUMMARIZE('pet-sounds-data', 'pet-sounds-data'[Emocion], 
                      "Conteo", COUNT('pet-sounds-data'[Emocion])
            ), [Conteo], DESC
        ),
    'pet-sounds-data'[Emocion]
)
)
```

---

## 🧩 Servicios AWS Utilizados

| Etapa | Servicios AWS |
|--------|----------------|
| **Ingesta Batch** | AWS Glue Studio, Glue Data Catalog, S3 |
| **Ingesta Streaming** | Kinesis Data Streams, Lambda, Firehose |
| **Almacenamiento** | S3, Redshift, Athena |
| **Procesamiento** | EMR (Spark), Redshift ML |
| **Visualización** | Power BI |

---

## 🧾 Beneficios e Impacto

| Beneficio | Impacto |
|------------|----------|
| Comunicación emocional animal-humano | Mejora la relación y empatía con la mascota |
| Prevención de estrés o enfermedad | Detección temprana basada en datos |
| Herramienta para veterinarios | Diagnóstico complementario y predictivo |
| Personalización por raza e individuo | Modelos IA adaptativos |
| Aplicación educativa y social | Uso en hogares, refugios y clínicas |

---

## 🧩 Buenas Prácticas Implementadas

- **Data Lake estructurado** con separación clara entre raw, processed y results.
- **Data Quality** con Glue para garantizar consistencia y completitud.
- **Particionado temporal** (`year/`, `month/`, `day/`) para escalabilidad.
- **Integración total con servicios nativos de AWS**.
- **Seguridad y gobernanza** mediante roles IAM y reglas de ciclo de vida.
- **Documentación completa** en `/docs` con arquitectura y dependencias.

---

## 📁 Estructura del Proyecto (Resumen)

```plaintext
pet-tracking-project/
├── glue/
├── kinesis/
├── emr/
├── warehouse/
├── dashboards/
├── logs/
└── docs/
```

---

## 🧪 Futuras Mejoras

- Incorporación de modelos **Deep Learning** (CNN/LSTM) para análisis multimodal de emociones.
- Integración con **Amazon SageMaker** para orquestación de pipelines ML.
- Aplicación móvil con notificaciones push para alertas de bienestar.
- Uso de **AWS IoT Core** para gestión directa de dispositivos.

---

## 👥 Autores y Créditos

**Proyecto desarrollado por:**  
Equipo de Ingeniería en Big Data & IA  
**Rol:** Arquitectura, Integración y Análisis Predictivo  
**Infraestructura:** AWS Cloud  
**Visualización:** Power BI  

---

## 📚 Licencia

Este proyecto está bajo la licencia **MIT**.  
Puedes usarlo, modificarlo y distribuirlo citando la fuente original.

---

**© 2025 – Pet Tracking | Big Data & AI Emotion Analytics**
