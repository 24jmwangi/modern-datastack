SELECT table_schema, table_name, COUNT(*) as row_count
FROM information_schema.tables
WHERE table_schema NOT IN ('information_schema', 'pg_catalog')

-- Add additional analysis queries as needed.