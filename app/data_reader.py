from typing import Optional

import pandas as pd
import sqlite3 as sql


class DataReader:

    def read_from_file(self, path: str, offset: int, delimiter: Optional[str] = None) -> pd.DataFrame:
        if path.endswith('csv'):
            try:
                df = pd.read_csv(path, skiprows=offset)
            except Exception as _:
                try:
                    df = pd.read_csv(path, skiprows=offset, delimiter=delimiter)
                except Exception as e:
                    print(e)
                    raise e
            return df

        else:
            try:
                df = pd.read_excel(path, skiprows=offset)
                return df
            except Exception as e:
                print(e)
                raise e

    def read_from_database(self, url, table, query=None) -> pd.DataFrame:
        try:
            conn = sql.connect(url)
            if query is None:
                query = f"SELECT * FROM {table}"
            df = pd.read_sql_query(query, conn)
            return df
        except Exception as e:
            print(e)
            raise e
