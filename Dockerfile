FROM python:3.11

# Install system dependencies
RUN apt-get update && apt-get install -y \
    default-mysql-client \
    default-libmysqlclient-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 8000

# Run gunicorn for production with custom configuration and enable logging
CMD ["gunicorn", "fetch_rewards.wsgi:application", "--config", "gunicorn_config.py", "--log-level", "info"]