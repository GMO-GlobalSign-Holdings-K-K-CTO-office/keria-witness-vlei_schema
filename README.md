## Overview
This repository provisions the backend infrastructure for KERI for issuing vLEI Credentials.

Invoke the following containers:
- Keria Agent for Issuer
- Keria Agent for Holder
- Witnesses
- vLEI Server (for retrieving vLEI credential schemas)

## Running
1. Install Docker and Docker Compose.
2. Clone the repository and switch to one of the following tags:
   * v1.x: Uses container images with demo witnesses provided by WebOfTrust.
   * v2.x: Uses raw `keripy` to launch a group of five witnesses manually.

## Reference Code
[https://github.com/WebOfTrust/signify-ts/blob/main/docker-compose.yaml](https://github.com/WebOfTrust/signify-ts/blob/main/docker-compose.yaml)
