import pandas as pd
from sqlalchemy import create_engine
from time import time

# Connect to Postgres
engine = create_engine('postgresql://root:root@localhost:5433/ny_taxi')

# Read CSV in chunks
df_iter = pd.read_csv("yellow_tripdata_2025-01.csv", iterator=True, chunksize=100000)

# Create table schema (empty table with headers)
df = next(df_iter)
df.head(0).to_sql(name='yellow_taxi_intf', con=engine, if_exists='replace')

# Insert the first chunk (already read above)
t_start = time()
df.to_sql(name='yellow_taxi_intf', con=engine, if_exists='append')
t_end = time()
print('First chunk inserted, cost %.3f seconds' % (t_end - t_start))

# Insert the rest of the chunks
while True:
    try:
        t_start = time()
        df = next(df_iter)
        df.to_sql(name='yellow_taxi_intf', con=engine, if_exists='append')
        t_end = time()
        print('Chunk inserted, cost %.3f seconds' % (t_end - t_start))
    except StopIteration:
        print('Finished inserting data.')
        break
