#!/usr/bin/env python3
"""Test Trino Iceberg setup"""

import os
from sqlalchemy import create_engine, text
import pandas as pd

# Clear proxy settings
for var in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"):
    os.environ.pop(var, None)
os.environ["NO_PROXY"] = "localhost,127.0.0.1"

print("=" * 60)
print("Testing Trino Connection")
print("=" * 60)

ENGINE = create_engine("trino://user@localhost:8081/iceberg?http_scheme=http")

# Test connection
print("\n1. Testing connection...")
try:
    with ENGINE.connect() as conn:
        result = conn.execute(text("SELECT 1")).fetchall()
        print(f"✓ Connection successful: {result}")
except Exception as e:
    print(f"✗ Connection failed: {e}")
    exit(1)

# Create schema and table
print("\n2. Creating schema and table...")
try:
    with ENGINE.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS demo"))
        print("✓ Schema created")
        
        # Try to drop existing table, but don't fail if it errors
        try:
            conn.execute(text("DROP TABLE IF EXISTS demo.test_events"))
            print("✓ Dropped existing table (if any)")
        except Exception as e:
            print(f"⚠ Could not drop table (may not exist): {e}")
        
        conn.execute(text("""
            CREATE TABLE demo.test_events (
                id BIGINT,
                category VARCHAR,
                ts TIMESTAMP(6)
            ) WITH (
                format = 'PARQUET',
                partitioning = ARRAY['day(ts)']
            )
        """))
        print("✓ Table created")
        
        # Insert sample data
        conn.execute(text("INSERT INTO demo.test_events VALUES (1, 'alpha', TIMESTAMP '2024-01-01 10:00:00')"))
        conn.execute(text("INSERT INTO demo.test_events VALUES (2, 'beta',  TIMESTAMP '2024-01-02 12:30:00')"))
        conn.execute(text("INSERT INTO demo.test_events VALUES (3, 'alpha', TIMESTAMP '2024-01-02 13:45:00')"))
        print("✓ Data inserted")
except Exception as e:
    print(f"✗ Table creation/insertion failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Query the data
print("\n3. Querying data...")
try:
    with ENGINE.connect() as conn:
        df = pd.read_sql(text("SELECT * FROM demo.test_events ORDER BY id"), conn)
        print("✓ Data retrieved:")
        print(df)
except Exception as e:
    print(f"✗ Query failed: {e}")
    exit(1)

# Query metadata
print("\n4. Querying metadata tables...")
try:
    with ENGINE.connect() as conn:
        print("\n=== Data Files ===")
        files_df = pd.read_sql(text('SELECT file_path, record_count, file_size_in_bytes FROM demo."test_events$files"'), conn)
        print(files_df)
        
        print("\n=== File Summary ===")
        summary_df = pd.read_sql(text('SELECT COUNT(*) AS num_files, SUM(record_count) AS total_rows FROM demo."test_events$files"'), conn)
        print(summary_df)
        print("✓ Metadata queries successful")
except Exception as e:
    print(f"✗ Metadata query failed: {e}")
    exit(1)

print("\n" + "=" * 60)
print("All tests passed! ✓")
print("=" * 60)

