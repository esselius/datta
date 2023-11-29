FROM eclipse-temurin:11.0.18_10-jre-focal

RUN curl -fL http://client.hub.confluent.io/confluent-hub-client-latest.tar.gz | tar xz -C /usr/local
RUN mkdir -p /build/confluent-hub-components

RUN confluent-hub install --no-prompt --component-dir /build/confluent-hub-components --worker-configs /dev/null debezium/debezium-connector-postgresql:2.2.1
RUN confluent-hub install --no-prompt --component-dir /build/confluent-hub-components --worker-configs /dev/null confluentinc/kafka-connect-jdbc:10.7.0
RUN confluent-hub install --no-prompt --component-dir /build/confluent-hub-components --worker-configs /dev/null confluentinc/kafka-connect-datagen:0.6.3
RUN confluent-hub install --no-prompt --component-dir /build/confluent-hub-components --worker-configs /dev/null confluentinc/kafka-connect-avro-converter:7.5.2

FROM quay.io/strimzi/kafka:0.38.0-kafka-3.6.0

ARG ICEBERG_CONNECTOR_VERSION=0.6.5

USER root:root

RUN mkdir -p /opt/kafka/plugins/confluentinc-kafka-connect-jdbc \
  && mkdir -p /opt/kafka/plugins/tabular-iceberg-kafka-connect

RUN cd /opt/kafka/plugins/tabular-iceberg-kafka-connect/ \
  && curl -sSfL https://github.com/tabular-io/iceberg-kafka-connect/releases/download/v${ICEBERG_CONNECTOR_VERSION}/iceberg-kafka-connect-runtime-hive-${ICEBERG_CONNECTOR_VERSION}.zip > iceberg.zip \
  && unzip iceberg.zip \
  && mv iceberg-kafka-connect-runtime-hive-${ICEBERG_CONNECTOR_VERSION}/lib /opt/kafka/plugins/tabular-iceberg-kafka-connect/ \
  && rm -rf iceberg.zip iceberg-kafka-connect-runtime-hive-${ICEBERG_CONNECTOR_VERSION}

RUN curl -sSfL https://jdbc.postgresql.org/download/postgresql-42.6.0.jar > /opt/kafka/plugins/confluentinc-kafka-connect-jdbc/postgresql.jar

COPY --from=0 /build/confluent-hub-components/debezium-debezium-connector-postgresql/lib /opt/kafka/plugins/debezium-postgresql/
COPY --from=0 /build/confluent-hub-components/confluentinc-kafka-connect-jdbc/lib /opt/kafka/plugins/confluentinc-kafka-connect-jdbc/
COPY --from=0 /build/confluent-hub-components/confluentinc-kafka-connect-datagen/lib /opt/kafka/plugins/confluentinc-kafka-connect-datagen/
COPY --from=0 /build/confluent-hub-components/confluentinc-kafka-connect-avro-converter/lib /opt/kafka/plugins/confluentinc-kafka-connect-avro-converter/

USER 1001
