import pandas as pd
import snowflake.connector as snow
from snowflake.connector.pandas_tools import write_pandas
from clean_csv_data import clean_data

conn = snow.connect(user="USERNAME",
                    password="PASSWORD",
                    account="ACCOUNT",
                    warehouse="WAREHOUSE",
                    database="YOUR_DATABASE_NAME",
                    schema="YOUR_SCHEMA_NAME"
                    )

cur = conn.cursor()

original = "fbref.csv"
delimiter = ","

total = pd.read_csv(clean_data(original), sep=delimiter)

write_pandas(conn, total, "YOUR_TABLE_NAME")

sql = "ALTER WAREHOUSE WAREHOUSE SUSPEND"
cur.execute(sql)

cur.close()
conn.close()
