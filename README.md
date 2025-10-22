# 🐾 PET TRACKING – Intelligent Emotional Interpretation System

### Big Data & AI Project | AWS | Streaming | ML | Power BI
[🇬🇧 English](./README.md) | [🇪🇸 Español](./README-es.md)

---

## 🚀 Overview

**Pet Tracking** is an intelligent system designed to **interpret, in real time, the emotions and basic needs of pets (dogs and cats)** by analyzing physiological signals, vocalizations, and physical behavior.  
Its architecture combines **Big Data, Machine Learning, and IoT** to deliver **animal–human emotional communication** based on objective data and analytical visualizations.

---

## 🎯 Goals

- Analyze large volumes of structured and unstructured data (sensors, audio, video, reports).
- Identify behavior patterns and emotional states.
- Translate emotions into messages understandable by caregivers and veterinarians.
- Generate interactive visualizations in **Power BI**.
- Prevent stress, anxiety, or disease through **smart alerts**.

---

## 🧠 High‑Level Architecture

```plaintext
[Wearables / Cameras / Microphones / Reports]
↓
(Data Ingestion)
├── AWS Glue / S3 (Batch)
├── AWS Kinesis / Lambda / Firehose (Streaming)
↓
(Storage)
Amazon S3 / Redshift / Athena
↓
(Processing)
Amazon EMR (Spark) / Redshift ML
↓
(Visualization)
Power BI Dashboard
```

---

## 🗂️ Data Collection

| Source | Data Type |
|-------|-----------|
| **Wearables (Collars, Sensors)** | Heart rate, temperature, physical activity, GPS |
| **Ambient Microphones** | Vocalizations, emotional tone, sound frequency |
| **Cameras** | Body posture, gestures, movement patterns |
| **Caregiver Reports** | Emotional labels: joy, anxiety, hunger, pain, etc. |

---

## 🔄 Data Ingestion

### 🧩 Batch (Daily)
- **Origin:** Reports and sensor histories.
- **AWS Services:**  
  - `Amazon S3`  
  - `AWS Glue Studio`, `Glue Data Catalog`, `Glue Data Quality`  
- **Transformations:**  
  - Normalization of types and column names.  
  - Classification of risk level (`alert_level`) and activity (`activity_level`).  
  - Quality validation with `Glue Data Quality`.

### ⚡ Streaming (Real Time)
- **Origin:** IoT devices sending vitals and vocalizations.
- **AWS Services:**  
  - `Amazon Kinesis Data Streams`  
  - `AWS Lambda` (JSON → Parquet transformation)  
  - `Amazon Firehose` (delivery to S3)
- **Format:** Parquet compressed with Snappy, partitioned by year/month/day.

---

## 🧱 Data Storage

Main bucket structure:  
`s3://pet-tracking-data-bucket/`

```plaintext
├── raw/
│   ├── batch/ (Raw batch data)
│   ├── stream/ (Real‑time data)
├── processed/ (Transformed data)
├── firehose-output/ (Automatic Firehose output)
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

### S3 Lifecycle Policies

| Folder | Action | Time |
|--------|--------|------|
| `raw/batch/` | Move to Glacier | 30 days |
| `raw/stream/` | Delete | 7 days |
| `processed/` | Delete | 90 days |
| `firehose-output/` | Delete | 60 days |

---

## ⚙️ Analytical Processing

### 🔸 AWS EMR (Apache Spark)
- Cleaning, aggregation, and data enrichment.
- Scripts in `PySpark` stored in `emr/scripts/`.
- Results exported to `emr/results/`.
- Scalable configuration via `bootstrap actions` and dedicated IAM roles.

### 🔸 Redshift + Redshift ML
- Integration with S3 via **Spectrum**.
- Training a **K‑Means** model on numerical metrics:
  - `age`, `heart_rate_bpm`, `activity_steps`, `gps_lat`, `gps_lon`.
- Prediction of behavioral‑emotional clusters.
- Results available for dashboards or alerts.

### 🔸 Athena
- SQL queries over partitioned Parquet tables.
- Query example:
  ```sql
  SELECT emotion, COUNT(*) AS freq
  FROM pet_sounds_data_cleaned
  GROUP BY emotion
  ORDER BY freq DESC;
  ```

---

## 📊 Visualization (Power BI)

**Dashboard 1 – Data & Emotion Analysis**
- Volume of recorded audios.
- Most common emotion.
- Emotion trends over time.
- Maximum frequency per emotion.
- Table with associated spectrograms.

**Key Indicators (DAX):**
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
*(Note: field names can be adapted to your data model in English.)*

---

## 🧩 AWS Services Used

| Stage | AWS Services |
|-------|--------------|
| **Batch Ingestion** | AWS Glue Studio, Glue Data Catalog, S3 |
| **Streaming Ingestion** | Kinesis Data Streams, Lambda, Firehose |
| **Storage** | S3, Redshift, Athena |
| **Processing** | EMR (Spark), Redshift ML |
| **Visualization** | Power BI |

---

## 🧾 Benefits & Impact

| Benefit | Impact |
|---------|--------|
| Animal–human emotional communication | Improves the relationship and empathy with the pet |
| Stress or disease prevention | Early detection based on data |
| Tool for veterinarians | Complementary and predictive diagnostics |
| Personalization by breed and individual | Adaptive AI models |
| Educational and social application | Use at homes, shelters, and clinics |

---

## 🧩 Implemented Best Practices

- **Structured data lake** with a clear separation between raw, processed, and results.
- **Data Quality** with Glue to ensure consistency and completeness.
- **Temporal partitioning** (`year/`, `month/`, `day/`) for scalability.
- **Full integration with native AWS services**.
- **Security & governance** via IAM roles and lifecycle rules.
- **Complete documentation** in `/docs` with architecture and dependencies.

---

## 📁 Project Structure (Summary)

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

## 🧪 Future Improvements

- Incorporate **Deep Learning** models (CNN/LSTM) for multimodal emotion analysis.
- Integrate **Amazon SageMaker** for ML pipeline orchestration.
- Mobile app with push notifications for wellness alerts.
- Use **AWS IoT Core** for direct device management.

---

## 👥 Authors & Credits

**Developed by:**  
Big Data & AI Engineering Team  
**Role:** Architecture, Integration, and Predictive Analytics  
**Infrastructure:** AWS Cloud  
**Visualization:** Power BI  

---

## 📚 License

This project is released under the **MIT** license.  
You are free to use, modify, and distribute it with proper attribution.

---

**© 2025 – Pet Tracking | Big Data & AI Emotion Analytics**

