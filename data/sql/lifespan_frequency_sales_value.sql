DROP VIEW IF EXISTS LIFESPAN_FREQUENCY_SALES;

CREATE VIEW LIFESPAN_FREQUENCY_SALES
AS
    WITH FIRSTORDERDATES AS (
            SELECT 
                USERID, 
                strftime('%Y-%m-01', MIN(DATE(CREATEDAT)))  AS COHORT_DATE
            FROM ORDERS
            GROUP BY USERID
        )

    SELECT 
        O.USERID,
        FOD.COHORT_DATE,
        strftime('%Y-%m-01', MAX(DATE(CREATEDAT)))  AS purchase_month,
        ((strftime('%Y', MAX(DATE(CREATEDAT))) - strftime('%Y', FOD.COHORT_DATE)) * 12) + (strftime('%m', MAX(DATE(CREATEDAT))) - strftime('%m', FOD.COHORT_DATE)) as lifespan,
        COUNT(O.SALES) AS frequency,
        O.currency,
        AVG(O.SALES) AS average_sales
    FROM ORDERS O
    LEFT JOIN FIRSTORDERDATES FOD ON O.USERID = FOD.USERID
    GROUP BY O.USERID, O.currency
