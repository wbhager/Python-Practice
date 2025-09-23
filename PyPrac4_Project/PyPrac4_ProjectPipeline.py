import yaml
from loguru import logger
from PyPrac4_UtilityFunctions import validate_dataframe
import sqlite3
import pandas as pd
from contextlib import contextmanager

class CSVLoader:
    def __init__(self, db_path):
        self.db_path = db_path

    def load(self, csv_file, table_name):
        df = pd.read_csv(csv_file)
        validate_dataframe(df, ["Gender"])
        with sqlite3.connect(self.db_path) as conn:
            df.to_sql(table_name, conn, if_exists = "replace", index = False)
        logger.info(f"File {csv_file} has been loaded into {table_name}.")

    def query(self, sql):
        with sqlite3.connect(self.db_path) as conn:
            return pd.read_sql_query(sql, conn)

@contextmanager # Can be expanded upon later
def open_config(path = "PyPrac4_yamlConfig.yml"):
    with open(path, "r") as f:
        yield yaml.safe_load(f)

def main():
    with open_config("PyPrac4_yamlConfig.yml") as config:
        print(config["database"]["path"])
        loader = CSVLoader(config["database"]["path"])
        for file in config["files"]:
            loader.load(file["path"], file["name"])

    query = loader.query("SELECT * FROM Employees_1 LIMIT 5;"); print(query)

if __name__ == "__main__":
    main()