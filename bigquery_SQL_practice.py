### Library Imports
from google.cloud import bigquery
import pandas as pd

client = bigquery.Client()

sql = """
    SELECT *
    FROM `bigquery-public-data.google_cfe.datacenter_cfe`
    LIMIT 100
"""

# Run a Standard SQL query using the environment's default project
df = client.query(sql).to_dataframe(create_bqstorage_client=False)

print(df.head())
