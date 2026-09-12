# Databricks notebook source
from pyspark.sql import functions as F

bronze = spark.table("workspace.bronze.sales_raw")

silver = (bronze
    .select(
        F.col("Invoice").cast("string").alias("invoice_no"),
        F.col("StockCode").cast("string").alias("stock_code"),
        F.trim(F.col("Description")).alias("description"),
        F.col("Quantity").cast("int").alias("quantity"),
        F.to_timestamp("InvoiceDate").alias("invoice_ts"),
        F.col("Price").cast("decimal(10,2)").alias("unit_price"),
        F.col("Customer_ID").cast("int").alias("customer_id"),
        F.col("Country").cast("string").alias("country"))
    .withColumn("invoice_date", F.to_date("invoice_ts"))
    .withColumn("is_cancellation", F.col("invoice_no").startswith("C"))
    .withColumn("line_amount", (F.col("quantity") * F.col("unit_price")).cast("decimal(12,2)"))
    .filter(F.col("description").isNotNull())
    .filter(F.col("unit_price") > 0)
    .dropDuplicates(["invoice_no", "stock_code", "invoice_ts"]))

(silver.write
       .format("delta")
       .mode("overwrite")
       .option("overwriteSchema", "true")
       .saveAsTable("workspace.silver.sales_clean"))

print("bronze rows:", bronze.count())
print("silver rows:", spark.table("workspace.silver.sales_clean").count())
display(spark.table("workspace.silver.sales_clean").limit(5))
