DROP VIEW IF EXISTS CUSTOMER_COHORT;

CREATE VIEW CUSTOMER_COHORT
AS
    -- cte (with statemements) no longer works in slite view definition. see https://sqlite.org/forum/info/4f65b1c296087176b59371073a4c381f8bdd4a87f308fc4c5320769fa6beb41d
    -- using sub queries instead
   
    SELECT 
        O.USERID, 
        O.CREATEDAT AS ORDER_DATE, 
        FOD.FIRST_ORDER_DATE, 
        ((strftime('%Y', O.CREATEDAT) - strftime('%Y', FOD.FIRST_ORDER_DATE)) * 12) + 
        (strftime('%m', O.CREATEDAT) - strftime('%m', FOD.FIRST_ORDER_DATE)) AS COHORT
    FROM ORDERS O
    LEFT JOIN (
        SELECT 
            USERID, 
            MIN(DATE(CREATEDAT)) AS FIRST_ORDER_DATE
        FROM ORDERS
        GROUP BY USERID
    ) FOD ON O.USERID = FOD.USERID
    ORDER BY O.USERID, O.CREATEDAT;
