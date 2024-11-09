# Use a specific Python base image
FROM python:3.12-slim

# Maintainer info
LABEL maintainer="zhitinglu.com"

# Set environment variables for consistent Python behavior
ENV PYTHONDONTWRITEBYTECODE 1  # Prevents creation of .pyc files
ENV PYTHONUNBUFFERED 1        # Ensures stdout/stderr is unbuffered

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create a non-root user early
RUN adduser --disabled-password --no-create-home django-user

# Define build argument for development
ARG DEV=false

# Create virtual environment and install pip
RUN python -m venv /py && /py/bin/pip install --upgrade pip

# Add virtual environment to PATH
ENV PATH="/py/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy the requirements files into the image
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

# Install base dependencies
RUN /py/bin/pip install -r /tmp/requirements.txt

# Install development dependencies if DEV argument is set to true
RUN if [ "$DEV" = "true" ]; then /py/bin/pip install -r /tmp/requirements.dev.txt; fi

# Copy application code into the image and set ownership
COPY --chown=django-user:django-user ./app /app

# Switch to non-root user
USER django-user

# Expose port for the application
EXPOSE 8000

# Set the default command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]