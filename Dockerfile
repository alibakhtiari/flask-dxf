FROM python:3.11-slim-buster

WORKDIR /app

# Install cron and nano
RUN apt-get update && apt-get install -y cron nano

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy cronjob file
COPY cronjob /etc/cron.d/my-cronjob

# Give execute permission and apply the cronjob
RUN chmod 0644 /etc/cron.d/my-cronjob
RUN crontab /etc/cron.d/my-cronjob

# Copy the rest of the application code
COPY . .

EXPOSE 5000

# This command runs both cron and your Flask app
CMD cron && python app.py