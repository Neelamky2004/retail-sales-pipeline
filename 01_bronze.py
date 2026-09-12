# Databricks notebook source
from pyspark.sql import functions as F

raw = (spark.read
       .option("header", True)
       .option("inferSchema", True)
       .csv("/Volumes/workspace/bronze/raw_files/retail_*.csv"))

print("rows read from file:", raw.count())
display(raw.limit(5))

# COMMAND ----------

raw = raw.toDF(*[c.strip().replace(" ", "_") for c in raw.columns])
print("columns:", raw.columns)

# COMMAND ----------

bronze = (raw
          .withColumn("_source", F.lit("uci_online_retail_ii"))
          .withColumn("_loaded_at", F.current_timestamp()))

(bronze.write
       .format("delta")
       .mode("overwrite")
       .option("overwriteSchema", "true")
       .saveAsTable("workspace.bronze.sales_raw"))

print("bronze table rows:", spark.table("workspace.bronze.sales_raw").count())
