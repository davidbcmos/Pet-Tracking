from pyspark.sql import SparkSession
from pyspark.sql.functions import when, col, avg

# Inicia sesión Spark
spark = SparkSession.builder.appName("PetBehaviorProcessing").getOrCreate()

# 1. Leer desde Parquet (ruta base del procesamiento por lotes)
df = spark.read.parquet("s3://pet-tracking-data-bucket/processed/behavior/")

# ✅ Cast para evitar errores de tipo
df = df.withColumn("idmascota", col("idmascota").cast("long"))

# 2. Filtrar alertas altas (dolor + ritmo alto)
alertas_altas = df.filter((col("heart_rate_bpm") > 130) & (col("emotion") == "dolor"))
alertas_altas.write.mode("overwrite").parquet("s3://pet-tracking-data-bucket/emr/results/alertas_altas/")

# 3. Clasificar nivel de actividad
df = df.withColumn(
    "activity_level",
    when(col("activity_steps") >= 10000, "high")
    .when(col("activity_steps") >= 5000, "medium")
    .otherwise("low")
)

# 4. Agregaciones por mascota
agg = df.groupBy("idmascota").agg(
    avg("heart_rate_bpm").alias("avg_heart_rate"),
    avg("activity_steps").alias("avg_activity_steps")
)
agg.write.mode("overwrite").parquet("s3://pet-tracking-data-bucket/emr/results/aggregados_por_mascota/")

# 5. Detección de valores anómalos
errores = df.filter((col("heart_rate_bpm") < 0) | (col("activity_steps") > 50000))
errores.write.mode("overwrite").parquet("s3://pet-tracking-data-bucket/emr/results/errores/")

# Finaliza sesión
spark.stop()