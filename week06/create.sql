WITH phone_regex AS (
    SELECT '^(\\+?1[-.\\s]?)?(\\(\\d{3}\\)|\\d{3})[-.\\s]?\\d{3}[-.\\s]?\\d{4}(x\\d+)?$' AS pattern
),

zip_regex AS (
    SELECT '^(0[1-9]|[1-9]\\d)\\d{3}(-\\d{4})?$' AS pattern
),

phone_tests AS (
    SELECT 'PHONE' AS data_type, '314-555-1234' AS value, TRUE  AS expected UNION ALL
    SELECT 'PHONE', '(314) 555-1234', TRUE UNION ALL
    SELECT 'PHONE', '314.555.1234', TRUE UNION ALL
    SELECT 'PHONE', '+1-314-555-1234', TRUE UNION ALL
    SELECT 'PHONE', '314-555-1234x456', TRUE UNION ALL
    SELECT 'PHONE', '314-555-123', FALSE UNION ALL
    SELECT 'PHONE', '314-ABC-1234', FALSE UNION ALL
    SELECT 'PHONE', '1-1-314-555-1234', FALSE UNION ALL
    SELECT 'PHONE', '31-555-1234', FALSE UNION ALL
    SELECT 'PHONE', '314-555-1234x', FALSE
),

zip_tests AS (
    SELECT 'ZIP' AS data_type, '63101' AS value, TRUE UNION ALL
    SELECT 'ZIP', '63101-1234', TRUE UNION ALL
    SELECT 'ZIP', '02108', TRUE UNION ALL
    SELECT 'ZIP', '01001', TRUE UNION ALL
    SELECT 'ZIP', '99950', TRUE UNION ALL
    SELECT 'ZIP', '00123', FALSE UNION ALL
    SELECT 'ZIP', '6310', FALSE UNION ALL
    SELECT 'ZIP', '63A01', FALSE UNION ALL
    SELECT 'ZIP', '63101-123', FALSE UNION ALL
    SELECT 'ZIP', '631011234', FALSE
) 

SELECT
    data_type,
    value,
    expected,
    CASE 
        WHEN data_type = 'PHONE'
            THEN regexp_like(value, (SELECT pattern FROM phone_regex))
        WHEN data_type = 'ZIP'
            THEN regexp_like(value, (SELECT pattern FROM zip_regex))
    END AS actual,
    expected = 
    CASE 
        WHEN data_type = 'PHONE'
            THEN regexp_like(value, (SELECT pattern FROM phone_regex))
        WHEN data_type = 'ZIP'
            THEN regexp_like(value, (SELECT pattern FROM zip_regex))
    END AS test_passed
FROM (
    SELECT * FROM phone_tests
    UNION ALL
    SELECT * FROM zip_tests
) as test_cases;