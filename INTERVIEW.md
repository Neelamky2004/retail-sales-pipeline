# Notes for myself

## One line
"I built a pipeline on Databricks that takes about a million retail
transactions, cleans them in stages, checks the data, and makes summary tables
for reporting."

## Words I should be able to explain

**Data pipeline** - code that moves data from where it lands to where it gets
used, cleaning it along the way.

**Bronze, silver, gold** - three layers. Raw, cleaned, summarised. Each layer
does one job so problems are easy to find.

**Delta Lake** - the table format Databricks uses. Normal files underneath, but
with database behaviour on top: transactions that fully succeed or fully fail,
schema checks, and a history of every version.

**Spark / PySpark** - the engine that does the processing. It splits the work up,
so a million rows works the same way a thousand does.

**Data quality check** - a query that counts bad rows. If it isn't 0, I stop the
pipeline so bad data never reaches a report.

## Questions I should expect

**Why three layers and not one script?**
If my cleaning has a bug, I fix it and rebuild silver and gold from bronze. I
never go back to the source. Each layer is also easy to test on its own.

**What did you actually clean?**
Renamed and typed every column, flagged cancellations (invoices starting with C),
worked out line amount, dropped rows with no description or zero price, removed
duplicates. 51,920 rows went.

**How do you know the data is right?**
Five checks run before gold gets built. Results go into a table so I can see the
history, and a failure stops the run.

**Have your checks ever failed?**
The first four can only fail if my silver cleaning broke, because silver already
filters those rows out. They're there to catch a regression. The fifth one tests
the source data itself.

**Why Delta and not just CSV?**
CSV has no transactions and no history. With Delta, a failed write doesn't leave
half a table behind, and `DESCRIBE HISTORY` shows me every version.

**What went wrong while building it?**
The source column is called `Customer ID` with a space, and Delta won't allow
spaces in column names. The write failed. I normalise column names in bronze now.

**How big was it?**
1,067,371 rows in, 1,015,451 after cleaning.

**Was this production?**
No. Personal project on Databricks Free Edition. Say it plainly.
