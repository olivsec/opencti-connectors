# OpenCTI Connectors

This repository hosts a collection of OpenCTI connectors developed to integrate and enhance threat intelligence workflows. Currently, it includes three connectors:

1. **Lobo Guará Certificate Domains**
   - Retrieves a list of monitored certificate domains from the Lobo Guará platform (https://loboguara.olivsec.com.br/).
   - Creates observables within OpenCTI.

2. **Domain Monitoring**
   - Monitors domains in OpenCTI.
   - Checks for any applications launched on these domains.
   - Creates an incident in OpenCTI if an application is identified.

3. **CrowdStrike Device Information**
   - Fetches device information from CrowdStrike.
   - Sends the retrieved information to OpenCTI.

Each connector is designed to streamline the integration process, ensuring seamless communication between different security platforms and enhancing the overall threat intelligence capability.

## Installation

To install and set up the connectors, follow the instructions provided in each connector's directory.

## Usage

Detailed usage instructions for each connector can be found in their respective directories. Ensure to configure the necessary API keys and environment variables as specified.

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests for any enhancements or bug fixes.
