## Overview
This repository provisions the backend infrastructure for KERI for issuing vLEI Credentials.

Invoke the following containers:
- Keria Agent for Issuer
- Keria Agent for Holder
- Witnesses
- vLEI Server (for retrieving vLEI credential schemas)

## Running
1. Install Docker and Docker Compose.
2. Clone the repository and switch to one of the following tags (the latest tag for each major version):
   * v1.x: Uses container images with demo witnesses provided by WebOfTrust.
   * (Work in Progress) v2.x: Uses `keripy` directly to launch a group of five witnesses.
       - Issue: [Update repository with v2.0 witness deployment using direct keripy setup](https://github.com/GMO-GlobalSign-Holdings-K-K-CTO-office/keria-witness-vlei_schema/issues/1)
3. Run `docker-compose up -d` to start the containers.

## Reference Code
[https://github.com/WebOfTrust/signify-ts/blob/main/docker-compose.yaml](https://github.com/WebOfTrust/signify-ts/blob/main/docker-compose.yaml)
