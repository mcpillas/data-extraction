# Use an official Python runtime as a parent image
FROM python:3.13.1-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install required Python packages from requirements.txt
RUN pip install --no-cache-dir -r requirement/data_extraction.txt

# Expose port 8888 for Jupyter Notebook
EXPOSE 8888

# Define environment variable to ensure unbuffered output
ENV PYTHONUNBUFFERED=1

# Run Jupyter Notebook when the container starts
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
