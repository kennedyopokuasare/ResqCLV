DROP VIEW IF EXISTS CUSTOMER_COHORT;

CREATE VIEW CUSTOMER_COHORT
AS
    WITH FIRSTORDERDATES AS (
        SELECT 
            USERID, 
            MIN(DATE(CREATEDAT)) AS FIRST_ORDER_DATE
        FROM ORDERS
        GROUP BY USERID
    ),
    COHORTS AS (
        SELECT 
            USERID, 
            MAX(COHORT) AS COHORT
        FROM (
                SELECT 
                    O.USERID, 
                    ((strftime('%Y', O.CREATEDAT) - strftime('%Y', FOD.FIRST_ORDER_DATE)) * 12) + 
                    (strftime('%m', O.CREATEDAT) - strftime('%m', FOD.FIRST_ORDER_DATE)) AS COHORT
                FROM ORDERS O
                LEFT JOIN FIRSTORDERDATES FOD ON O.USERID = FOD.USERID
        ) AS HISTORICALCOHORTS
        GROUP BY USERID  
)
SELECT * FROM COHORTS 
ORDER BY COHORT DESC;
