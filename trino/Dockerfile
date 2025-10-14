FROM trinodb/trino:latest

# Copy Trino configuration files
COPY etc/config.properties /etc/trino/config.properties
COPY etc/jvm.config /etc/trino/jvm.config
COPY etc/node.properties /etc/trino/node.properties
COPY etc/catalog/iceberg.properties /etc/trino/catalog/iceberg.properties
