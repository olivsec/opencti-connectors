# Lobo Guara Connector for OpenCTI

This is the Lobo Guara connector for OpenCTI, which fetches monitored certificate domains from a specified URL and imports them as observables into OpenCTI.

## Configuration

The connector can be configured using the following environment variables:

- `OPENCTI_URL`: The URL of the OpenCTI instance.
- `OPENCTI_TOKEN`: The API token for accessing OpenCTI.
- `CONNECTOR_ID`: The unique identifier for the connector.
- `LOBOGUARA_API_TOKEN`: The API token for authenticating with the Lobo Guara API (provided by the user).
- `LOBOGUARA_INTERVAL_SEC`: The interval in seconds for fetching certificates. Default is 3600 seconds.
- `LOBOGUARA_VERIFY_SSL`: Whether to verify SSL certificates when connecting to the Lobo Guara API. Default is true.
- `LOBOGUARA_TLP`: The TLP marking to apply to observables. Default is `TLP:AMBER`.
- `LOBOGUARA_SCORE`: The score to apply to observables. Default is 50.
- `CONNECTOR_LOG_LEVEL`: The logging level for the connector. Default is `ERROR`.

## Running the Connector

To run the connector, use the following command:

```sh
docker-compose up --build
```

## Docker Compose Configuration

An example `docker-compose.yml` configuration for the connector:

```yaml
version: '3'
services:
  lobo_guara_connector:
    image: olivsec/lobo_guara_connector:latest
    container_name: lobo_guara_connector
    environment:
      - OPENCTI_URL=http://opencti:8080
      - OPENCTI_TOKEN=your_opencti_token
      - CONNECTOR_ID=unique_connector_id
      - LOBOGUARA_API_TOKEN=your_loboguara_api_token
      - LOBOGUARA_INTERVAL_SEC=1800
      - LOBOGUARA_VERIFY_SSL=false
      - LOBOGUARA_TLP=TLP:AMBER
      - LOBOGUARA_SCORE=50
      - CONNECTOR_LOG_LEVEL=INFO
    restart: always
    networks:
      - your_network_name

networks:
  your_network_name:
    external: true
```

Replace `your_opencti_token`, `unique_connector_id`, `your_loboguara_api_token`, and `your_network_name` with your actual OpenCTI token, unique connector ID, Lobo Guara API token, and network name.

## License

This project is licensed under the terms of the MIT license.
