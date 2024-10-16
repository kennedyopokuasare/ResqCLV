DROP VIEW IF EXISTS PROVIDER_COHORT;

CREATE VIEW PROVIDER_COHORT
AS
    WITH FIRSTORDERDATES AS (
            SELECT 
                providerId, 
                strftime('%Y-%m-01', MIN(DATE(CREATEDAT)))  AS COHORT_DATE
            FROM ORDERS
            GROUP BY providerId
        ),
        AT_LEAST_ONE_ORDER_PER_MONTH AS (
            SELECT 
                providerId, 
                MAX(CREATEDAT) AS PURCHASE_DATE
            FROM ORDERS
            GROUP BY providerId, strftime('%Y-%m-01', CREATEDAT)
        )
       
        SELECT 
            O.providerId, 
            FOD.COHORT_DATE,
            O.PURCHASE_DATE, 
            ((strftime('%Y', O.PURCHASE_DATE) - strftime('%Y', FOD.COHORT_DATE)) * 12) + 
            (strftime('%m', O.PURCHASE_DATE) - strftime('%m', FOD.COHORT_DATE)) AS MONTHS_SINCE_FIRST_PURCHASE
        FROM AT_LEAST_ONE_ORDER_PER_MONTH O
        LEFT JOIN FIRSTORDERDATES FOD ON O.providerId = FOD.providerId
        ORDER BY FOD.COHORT_DATE, O.providerId, O.PURCHASE_DATE
       
