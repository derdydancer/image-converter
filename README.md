# image-converter

## Installation
if you want to build the image directly from the GitHub repository without cloning it locally, you need to modify your Docker Compose file as follows:

### Docker Compose File:
```
version: '3'

services:
  image-converter:
    build:
      context: https://github.com/derdydancer/image-converter.git
    volumes:
      - /path/to/input_directory:/input
      - /path/to/output_directory:/output
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
