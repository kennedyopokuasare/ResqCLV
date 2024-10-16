import os
import sqlite3
import pandas as pd
from datetime import datetime

class DataPipeline(object):

    def __init__(self, db_and_scripts_path="./data"):
        super().__init__()
        self._log("Initializing pipeline")

        self.db_path = os.path.join(db_and_scripts_path, "mock_resq.db")
        self._script_path = os.path.join(db_and_scripts_path, "sql")
        os.makedirs(os.path.join(db_and_scripts_path, "sql"), exist_ok=True)

        self._create_connection()
        self._create_customer_cohorts_view()
        self._create_provider_cohorts_view()
        self._create_top_partners_by_sales_view()
        self._create_partner_segment_order_quantity_view()
        self._create_lifespan_frequency_sales_view()
        self._close_connection()

        self._log("Done")

    def top_n_partners(self, top_n=5):
        """
        Return top n partners by sales
        """

        if not isinstance(int(top_n), int):
            raise ValueError("top n must be in int")

        sql = "SELECT * FROM TOP_PARTNERS LIMIT ?"
        return self.execute_query(query=sql, param=(top_n,))

    def customers_top_partner_segment(self, top_n=None):
        """
        Returns the order quantity of the top n partner segment.
        If top_n is not specified, it returns the favourite partner segment
        """

        if (top_n is not None) and (not isinstance(top_n, int)):
            raise ValueError("top n must be in int or None")

        top_n = 1 if top_n is None else top_n

        sql = "SELECT * FROM PARTNET_SEGMENT_ORDER_QUANTIY LIMIT ?"

        return self.execute_query(query=sql, param=(top_n,))

    def m_customer_retention_rate(self, month=1):
        """
        Returns M customer retention rate. Defauts to MI retention rate
        """

        if not isinstance(month, int):
            raise ValueError("month must be in int")

        sql = """
                SELECT 
                (
                    CAST(
                    (
                        SELECT COUNT(*) 
                        FROM CUSTOMER_COHORT 
                        WHERE MONTHS_SINCE_FIRST_PURCHASE = ?
                    ) AS REAL) / 
                    CAST(
                        (
                            SELECT COUNT(DISTINCT(USERID)) FROM CUSTOMER_COHORT
                        ) AS REAL)
                ) * 100 AS M_RETENTION
              """
        return self.execute_query(query=sql, param=(month,))
    
    def m_provider_retention_rate(self, month=1):
        """
        Returns M provider retention rate. Defauts to MI retention rate
        """

        if not isinstance(month, int):
            raise ValueError("month must be in int")

        sql = """
                SELECT 
                (
                    CAST(
                    (
                        SELECT COUNT(*) 
                        FROM PROVIDER_COHORT 
                        WHERE MONTHS_SINCE_FIRST_PURCHASE = ?
                    ) AS REAL) / 
                    CAST(
                        (
                            SELECT COUNT(DISTINCT(providerId)) FROM PROVIDER_COHORT
                        ) AS REAL)
                ) * 100 AS M_RETENTION
              """
        return self.execute_query(query=sql, param=(month,))
    
    def m_customer_retention_rate_by_cohort(self, month=1, cohort=None):
        """
        Returns M customer retention rate by cohort. Defauts to MI retention rate of entire customers

        Keyword arguments:

        :cohort: -- the cohort in the form yyyy-mm-01
        """

        if not isinstance(month, int):
            raise ValueError("month must be an int")

        if not cohort:
            return self.m_customer_retention_rate(month=month)

        error_message = "cohort must be a date in the format yyyy-mm-01"
        try:
            cohort_date = datetime.fromisoformat(cohort)

            if cohort_date.day != 1:
                raise ValueError(error_message)
        except:
            raise ValueError(error_message)

        sql = """
                SELECT 
                (
                    CAST(
                    (
                        SELECT COUNT(*) 
                        FROM CUSTOMER_COHORT 
                        WHERE MONTHS_SINCE_FIRST_PURCHASE = ? AND COHORT_DATE = ?
                    ) AS REAL) / 
                    CAST(
                        (
                            SELECT COUNT(DISTINCT(USERID)) 
                            FROM CUSTOMER_COHORT
                            WHERE COHORT_DATE = ?
                        ) AS REAL)
                ) * 100 AS M_RETENTION
              """
        return self.execute_query(
            query=sql,
            param=(
                month,
                cohort,
                cohort,
            ),
        )

    def m_provider_retention_rate_by_cohort(self, month=1, cohort=None):
        """
        Returns M provider retention rate by cohort. Defauts to MI retention rate of entire customers

        Keyword arguments:

        :cohort: -- the cohort in the form yyyy-mm-01
        """

        if not isinstance(month, int):
            raise ValueError("month must be an int")

        if not cohort:
            return self.m_provider_retention_rate(month=month)

        error_message = "cohort must be a date in the format yyyy-mm-01"
        try:
            cohort_date = datetime.fromisoformat(cohort)

            if cohort_date.day != 1:
                raise ValueError(error_message)
        except:
            raise ValueError(error_message)

        sql = """
                SELECT 
                (
                    CAST(
                    (
                        SELECT COUNT(*) 
                        FROM PROVIDER_COHORT 
                        WHERE MONTHS_SINCE_FIRST_PURCHASE = ? AND COHORT_DATE = ?
                    ) AS REAL) / 
                    CAST(
                        (
                            SELECT COUNT(DISTINCT(providerId)) 
                            FROM PROVIDER_COHORT
                            WHERE COHORT_DATE = ?
                        ) AS REAL)
                ) * 100 AS M_RETENTION
              """
        return self.execute_query(
            query=sql,
            param=(
                month,
                cohort,
                cohort,
            ),
        )
    
    def execute_query(self, query: str, param : tuple | None= None):
        """
        Execute SQL query with parameters
        """

        self._create_connection()
        with self.conn as connection:
            return pd.read_sql_query(sql=query, con=connection, params=param)

    def _create_top_partners_by_sales_view(self):
        """
        Creates top partners by sales view
        """

        self._log("Creating top partners by sales view in database")
        script_path = os.path.join(self._script_path,"top_partners.sql")
        self._execute_script(script_path)

    def _create_partner_segment_order_quantity_view(self):
        """
        Creates partner segments and order quantity view
        """

        self._log("Creating partner segments and order quantity view in database")
        script_path = os.path.join(self._script_path,"partner_segment_order_quantity.sql")
        self._execute_script(script_path)

    def _create_customer_cohorts_view(self):
        """
        Creates customer cohorts view
        """

        self._log("Creating customer cohorts view in database")
        script_path = os.path.join(self._script_path,"customer_cohort.sql")
        self._execute_script(script_path)
    
    def _create_provider_cohorts_view(self):
        """
        Creates provider cohorts view
        """

        self._log("Creating provider cohorts view in database")
        script_path = os.path.join(self._script_path,"provider_cohort.sql")
        self._execute_script(script_path)

    def _create_lifespan_frequency_sales_view(self):
        """
        Creates Lifespan, Frequency, sales value view
        """

        self._log("Creating Lifespan, Frequency, sales value view in database")
        script_path = os.path.join(self._script_path,"lifespan_frequency_sales_value.sql")
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

    def _log(self, text):
        print(datetime.now().strftime("%H:%M:%S"), text)
