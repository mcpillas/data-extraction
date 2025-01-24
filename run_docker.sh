#!/bin/bash

# Build the Docker image
docker build -t meteorite-analysis .

# Run the Docker container and map port 8888 for Jupyter Notebook
docker run -p 8888:8888 meteorite-analysis
