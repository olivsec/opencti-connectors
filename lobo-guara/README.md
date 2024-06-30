# Lobo Guara Connector for OpenCTI

This is the Lobo Guara connector for OpenCTI, which fetches monitored certificate domains from a specified URL and imports them as observables into OpenCTI.

## Configuration

The connector can be configured using the following environment variables:

- `OPENCTI_URL`: The URL of the OpenCTI instance.
- `OPENCTI_TOKEN`: The API token for accessing OpenCTI.
- `CONNECTOR_ID`: The unique identifier for the connector.
- `LOBOGUARA_USERNAME`: The username for authenticating with the Lobo Guara API.
- `LOBOGUARA_PASSWORD`: The password for authenticating with the Lobo Guara API.
- `LOBOGUARA_INTERVAL_SEC`: The interval in seconds for fetching certificates. Default is 3600 seconds.
- `LOBOGUARA_VERIFY_SSL`: Whether to verify SSL certificates when connecting to the Lobo Guara API. Default is true.
- `LOBOGUARA_URL`: The URL for fetching monitored certificate domains.
- `LOBOGUARA_TOKEN_URL`: The URL for generating an authentication token.
- `LOBOGUARA_TLP`: The TLP marking to apply to observables. Default is `TLP:AMBER`.
- `LOBOGUARA_SCORE`: The score to apply to observables. Default is 50.
- `CONNECTOR_LOG_LEVEL`: The logging level for the connector. Default is `ERROR`.

## Running the Connector

To run the connector, use the following command:

```sh
docker-compose up --build
