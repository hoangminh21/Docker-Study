import pandas as pd
from pandas.io import sql
from sqlalchemy import create_engine
from time import time

# Create database engine connection
engine = create_engine('postgresql://root:root@localhost:5433/ny_taxi')

# Create the table before inserting data if it doesn't exist already
df = pd.read_csv("taxi_zone_lookup.csv", nrows=0)  # Read just the header
df.to_sql(name='zone_lookup_intf', con=engine, if_exists='replace', index=False)

# Read in chunks and insert
df_iter = pd.read_csv("taxi_zone_lookup.csv", iterator=True, chunksize=100000)

while True:
    try:
        t_start = time()
        df = next(df_iter)
        df.to_sql(name='zone_lookup_intf', con=engine, if_exists='append', index=False)
        t_end = time()
        print(f'Chunk inserted, cost {t_end - t_start:.3f} seconds')
    except StopIteration:
        print('Finished inserting data.')
        break
    except Exception as e:
        print(f'Error occurred: {e}')
        break
