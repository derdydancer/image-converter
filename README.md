# image-converter

## Installation
if you want to build the image directly from the GitHub repository without cloning it locally, you need to modify your Docker Compose file as follows:

### Docker Compose File:
```
version: '3'

services:
  image-processor:
    build: .
    volumes:
      - .:/usr/src/app
      - /path/to/input_directory:/input
      - /path/to/output_directory:/output
    environment:
      - WIDTH=800
      - QUALITY=85
```
In this configuration, the context directive under build points to the GitHub repository URL.

### Build and Run:
Execute the following command:
```
docker-compose up --build
```
Notes
- Update the volume paths (/path/to/input_directory and /path/to/output_directory) to the actual paths on your machine.
- If there are specific branches or tags you want to build from, you need to clone the repository locally or modify the context to point to the specific branch or tag.
