# Use the official Python image as the base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Install uv
# COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy requirements.txt to the working directory
COPY requirements.txt ./

# Create virtual environment
# RUN uv venv
# RUN source .venv/bin/activate

# Install the application dependencies
# RUN uv pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Command to run the application
CMD ["scrapy", "crawl", "cincyhub_crawler"]
