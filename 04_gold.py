# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE workspace.gold.daily_sales AS
# MAGIC SELECT
# MAGIC   invoice_date,
# MAGIC   country,
# MAGIC   count(DISTINCT invoice_no)                               AS invoices,
# MAGIC   sum(CASE WHEN is_cancellation THEN 0 ELSE quantity END)  AS units_sold,
# MAGIC   sum(line_amount)                                         AS net_revenue
# MAGIC FROM workspace.silver.sales_clean
# MAGIC GROUP BY invoice_date, country;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE workspace.gold.product_monthly AS
# MAGIC SELECT
# MAGIC   date_trunc('MONTH', invoice_date) AS month,
# MAGIC   stock_code,
# MAGIC   max(description)                  AS description,
# MAGIC   sum(quantity)                     AS units,
# MAGIC   sum(line_amount)                  AS revenue
# MAGIC FROM workspace.silver.sales_clean
# MAGIC WHERE NOT is_cancellation
# MAGIC GROUP BY 1, 2;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT invoice_date, country, invoices, net_revenue
# MAGIC FROM workspace.gold.daily_sales
# MAGIC ORDER BY net_revenue DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY workspace.silver.sales_clean;
