SELECT 
    table_schema, 
    table_name, 
    COUNT(*) AS row_count
FROM information_schema.tables
WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
GROUP BY table_schema, table_name
ORDER BY table_schema, table_name;
