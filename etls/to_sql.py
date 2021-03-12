#%%
# class for quick sql importing
import pandas as pd
import os
import psycopg2
from psycopg2 import extras



class pg_connect:
    def __init__(self):
        self.conn = psycopg2.connect(
            os.environ['CONN_STRING']
        )

    def _create_df(self, data, cols):
        return pd.DataFrame(data, columns = cols)

    def query(self, query):
        data = None
        with self.conn.cursor() as cur:
            
            cur.execute(query)
            
            if cur.description:

                cols = [i.name for i in cur.description]
                
                data = self._create_df(cur.fetchall(), cols)

            self.conn.commit()
            self.conn.close()
        
        return data

    def insert(self, table, df):
        df = df.where(pd.notnull(df), None).copy()
        values = list(df.itertuples(index=False, name=None))

        with self.conn.cursor() as cur:
            extras.execute_values(
                cur,
                sql = f'''INSERT INTO {table} ({', '.join(df.columns)}) VALUES %s''',
                page_size=len(values),
                argslist=values
            )

            self.conn.commit()
            self.conn.close()

        return
