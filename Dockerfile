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

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Move to src directory where manage.py is located
WORKDIR /app/src

# Run gunicorn for production
CMD ["gunicorn", "fetch_rewards.wsgi:application", "--bind", "0.0.0.0:8000"]