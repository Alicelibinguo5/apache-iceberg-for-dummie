# Apache Iceberg for Dummies

A hands-on tutorial for Apache Iceberg with Spark and Trino.

## Project Structure

```
.
├── 01_spark_iceberg_setup.ipynb    # Spark + Iceberg tutorial (WORKING ✓)
├── 02_trino_iceberg_setup.ipynb    # Trino + Iceberg tutorial (WIP)
├── docker-compose.yml               # Docker services configuration
├── trino/
│   ├── Dockerfile                   # Custom Trino image with baked-in config
│   └── etc/                        # Trino configuration files
│       ├── config.properties
│       ├── jvm.config
│       ├── node.properties
│       └── catalog/
│           └── iceberg.properties  # Iceberg catalog configuration
└── warehouse/                      # Iceberg table storage (gitignored)
```

## Quick Start

### Spark + Iceberg (Recommended - Working ✓)

```bash
# Run the Spark notebook
jupyter notebook 01_spark_iceberg_setup.ipynb
```

This notebook demonstrates:
- Creating Iceberg tables with Spark
- Writing partitioned data
- Querying Iceberg metadata
- Time travel queries
- Schema evolution

**This is the recommended way to learn Apache Iceberg!**

### Trino + Iceberg (Reference Only - Not Working)

⚠️ **Note**: The Trino setup is currently not functional due to catalog configuration challenges with file-based storage. See "Known Issues" below for details.

The `02_trino_iceberg_setup.ipynb` notebook and `test_trino.py` script are provided as reference for future implementation.

**For a working Trino + Iceberg setup, you would need:**
- Cloud storage (S3, GCS, or Azure Blob)
- Or a properly configured Hive Metastore with PostgreSQL
- Or Nessie catalog server

## Current Status

### ✅ Working
- Spark + Iceberg integration
- HadoopCatalog with file-based storage
- Docker setup for Spark
- Custom Trino Docker image with lift-and-shift configuration approach

### 🚧 Known Issues

#### Trino Iceberg Catalog Configuration

We've encountered challenges configuring Trino to work with Iceberg:

1. **REST Catalog Path Issue**: The `tabulario/iceberg-rest` image returns table locations as `file:/warehouse...` (single slash) instead of `file:///warehouse...` (triple slash), causing "No factory for location" errors in Trino.

2. **JDBC Catalog**: Requires SQLite JDBC driver to be properly loaded, configuration parsing issues.

3. **Hive Metastore**: Requires additional PostgreSQL setup and JDBC drivers.

#### Attempted Solutions

- ✓ Custom Trino Docker image with baked-in configurations
- ✓ Platform-specific build for Apple Silicon (ARM64)
- ✗ REST catalog with HadoopCatalog backend
- ✗ JDBC catalog with SQLite
- ✗ File-based Hive metastore (not supported in Trino)
- ✗ External Hive metastore service (driver compatibility issues)

## Configuration Details

### Docker Compose

Current configuration uses:
- Trino (custom build with ARM64 support)
- Volume mount for `/warehouse` directory

### Trino Catalog Properties

Located at `trino/etc/catalog/iceberg.properties`. Various catalog types attempted:

**REST Catalog** (issue with path format):
```properties
connector.name=iceberg
iceberg.catalog.type=rest
iceberg.rest-catalog.uri=http://iceberg-rest:8181
```

**JDBC Catalog** (driver loading issue):
```properties
connector.name=iceberg
iceberg.catalog.type=jdbc
iceberg.jdbc-catalog.driver-class=org.sqlite.JDBC
iceberg.jdbc-catalog.connection-url=jdbc:sqlite:/warehouse/iceberg_catalog.db
```

## Next Steps

To get Trino working with Iceberg, consider:

1. **Use a different Iceberg REST catalog** that properly handles file:/// URIs
2. **Set up a proper Hive Metastore** with all required JDBC drivers
3. **Use cloud storage** (S3, GCS, Azure) instead of local file storage
4. **Use Iceberg's Nessie catalog** for better REST API support

## Requirements

- Docker & Docker Compose
- Python 3.10+
- Jupyter Notebook
- For Spark: `pyspark`, `pyiceberg`, `pandas`
- For Trino: `sqlalchemy-trino`, `pandas`

## Installation

```bash
# Install Python dependencies
pip install pyspark pyiceberg pandas sqlalchemy-trino

# Start services
docker compose up -d
```

## Architecture

```
┌─────────────────┐
│  Spark/Trino    │
│   (Compute)     │
└────────┬────────┘
         │
         ├─────────────────┐
         │                 │
         ▼                 ▼
┌─────────────────┐  ┌──────────────┐
│ Iceberg Catalog │  │   Warehouse  │
│   (Metadata)    │  │    (Data)    │
└─────────────────┘  └──────────────┘
```

## License

MIT

## Contributing

This is a learning project. Feel free to open issues or PRs with improvements!

