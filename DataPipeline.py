import sqlite3
import pandas as pd
from datetime import datetime


class DataPipeline(object):
    db_path = "./data/mock_resq.db"

    def __init__(self):
        super().__init__()
        self._log("Initializing pipeline")
        self._create_connection()
        self._create_customer_cohorts_view()
        self._create_top_partners_by_sales_view()
        self._create_partner_segment_order_quantity_view()
        self._close_connection()
        self._log("Done")

    def top_n_partners(self, top_n):
        """
        Return top n partners by sales
        """
        
        sql = "SELECT * FROM TOP_PARTNERS LIMIT ?"
        return self._execute_query(query= sql, param=(top_n,))

    def customers_top_partner_segment(self, top_n=None):
        """
        Returns the order quantity of the top n partner segment.
        If top_n is not specified, it returns the favourite partner segment
        """

        top_n = 1 if top_n is None else top_n
        sql = "SELECT * FROM PARTNET_SEGMENT_ORDER_QUANTIY LIMIT ?"
        
        return self._execute_query(query=sql, param=(top_n,))

    def m1_retention_rate(self):
        """
        Returns M1 retention rate
        """

        sql = """
                SELECT 
                    (
                        CAST((SELECT COUNT(*) FROM CUSTOMER_COHORT WHERE COHORT > 0) AS REAL) / 
                        CAST((SELECT COUNT(*)  FROM USERS) AS REAL)
                    ) * 100 AS M1_SHARE_PERCENTAGE
              """
        return self._execute_query(query=sql)

    def _create_top_partners_by_sales_view(self):
        """
        Creates top partners by sales view
        """

        self._log("Creating top partners by sales view in database")
        script_path = "./data/sql/top_partners.sql"
        self._execute_script(script_path)

    def _create_partner_segment_order_quantity_view(self):
        """
        Creates partner segments and order quantity view 
        """

        self._log("Creating partner segments and order quantity view in database")
        script_path = "./data/sql/partner_segment_order_quantity.sql"
        self._execute_script(script_path)

    def _create_customer_cohorts_view(self):
        """
        Creates customer cohorts view
        """

        self._log("Creating customer cohorts view in database")
        script_path = "./data/sql/customer_cohort.sql"
        self._execute_script(script_path)

    def _create_connection(self):
        """
        Creates a database connection
        """

        self.conn = sqlite3.connect(self.db_path)

    def _close_connection(self):
        """
        Closes existing database connection.
        """

        if self.conn:
            self.conn.commit()
            self.conn.close()

    def _execute_script(self, script_path):
        """
        Execute SQL script from file 
        """

        with open(script_path, "r") as file:
            sql_script = file.read()

        cursor = self.conn.cursor()
        cursor.executescript(sql_script)

    def _execute_query(self, query, param=None):
        """
        Execute SQL query with parameters 
        """

        self._create_connection()
        with self.conn as connection:
            return pd.read_sql_query(sql=query, con=connection, params=param)
    
    def _log(self, text):
        print(datetime.now().strftime('%H:%M:%S'), text)
