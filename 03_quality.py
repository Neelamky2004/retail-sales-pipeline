# Databricks notebook source
from datetime import datetime, timezone

TABLE = "workspace.silver.sales_clean"

checks = {
    "duplicate_lines":
        f"SELECT count(*) FROM (SELECT invoice_no, stock_code, invoice_ts "
        f"FROM {TABLE} GROUP BY 1,2,3 HAVING count(*) > 1)",
    "null_stock_code":
        f"SELECT count(*) FROM {TABLE} WHERE stock_code IS NULL",
    "zero_or_negative_price":
        f"SELECT count(*) FROM {TABLE} WHERE unit_price <= 0",
    "future_dates":
        f"SELECT count(*) FROM {TABLE} WHERE invoice_date > current_date()",
    "negative_qty_not_flagged":
        f"SELECT count(*) FROM {TABLE} WHERE quantity < 0 AND is_cancellation = false",
}

BLOCKING = {"duplicate_lines", "null_stock_code", "zero_or_negative_price", "future_dates"}

# COMMAND ----------

results = []

for name, sql in checks.items():
    bad_rows = spark.sql(sql).collect()[0][0]
    results.append((name, int(bad_rows), bad_rows == 0, datetime.now(timezone.utc)))
    print(f"{name}: {bad_rows}")

dq = spark.createDataFrame(
    results, "check_name string, bad_rows long, passed boolean, checked_at timestamp")

dq.write.format("delta").mode("append").saveAsTable("workspace.silver.quality_results")
display(dq)

# COMMAND ----------

failed   = [r[0] for r in results if not r[2]]
blocking = [n for n in failed if n in BLOCKING]

for n in failed:
    if n not in BLOCKING:
        print(f"WARNING: {n}")

if blocking:
    raise Exception(f"Data quality check failed: {blocking}")

print("No blocking failures.")
