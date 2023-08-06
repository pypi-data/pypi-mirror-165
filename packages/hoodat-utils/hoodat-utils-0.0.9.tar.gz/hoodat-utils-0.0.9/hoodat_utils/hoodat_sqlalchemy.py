# Base Imports
import logging

# Libraries
import pandas as pd

# SqlAlchemy Imports
import sqlalchemy
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


import os
import pymysql


class HoodatSqlalchemy:
    def __init__(self, sqlalchemy_database_uri):
        self.sqlalchemy_database_uri = sqlalchemy_database_uri
        self.engine = sqlalchemy.create_engine(self.sqlalchemy_database_uri)

    def create_session(self):
        self.session = Session(self.engine)
        return self.session

    def commit_pandas_df(self, df, table, record_func):
        session = self.create_session()
        logging.info(f"Populating {table} table")
        n_rows = df.shape[0]
        logging.info(f"Total rows: {n_rows}")
        for i in range(n_rows):
            x = df.iloc[i]
            try:
                record = record_func(x)
                session.add(record)
                session.flush()
            except IntegrityError as e:
                logging.info("Record already exists in db")
                logging.info(e)
                session.rollback()
            else:
                logging.info("Adding row")
                session.commit()
        session.close()

    def query(self, query: str):
        """Run a query against the database

        Args:
            query (str): A SQL query to run
        """
        session = self.create_session()
        session.execute(text(query))
        session.close()

    def query_to_df(self, query):
        """Run a query against the database and return a pandas dataframe

        Args:
            query (str): A SQL query to run
        """
        session = self.create_session()
        query_result = session.execute(text(query)).all()
        session.close()
        df = pd.DataFrame(query_result)
        return df

    def create_views(self, views_obj: object, overwrite: bool = False):
        """Creates views defined in an object

        Args:
            views_obj (object): An object with `key: value` being `name of view: query to create view`
            overwrite (boolean) = False: Whether or not to overwrite existing views
        """
        for view_key in views_obj.keys():
            if overwrite:
                print("Overwrite is true")
                prefix = "CREATE OR REPLACE VIEW"
            else:
                prefix = "CREATE VIEW"
            try:
                session = self.create_session()
                query = f"{prefix} `{view_key}` AS {views_obj[view_key]}"
                session.execute(text(query))
                session.close()
            except Exception as e:
                return f"Failed to create views with error: {e}"
        return "Success"
