# 1. Use a more recent and supported base image
FROM python:3.11-slim-bookworm

# Set the working directory
WORKDIR /app

# 2. Install packages efficiently and clean up in a single layer
#    --no-install-recommends keeps the image smaller
RUN apt-get update && apt-get install -y --no-install-recommends \
    cron \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy cronjob file
# IMPORTANT: Ensure your 'cronjob' file has a blank line at the end!
COPY cronjob /etc/cron.d/my-cronjob

# 3. Simplify cron setup: Give correct permissions. `crontab` command is not needed.
RUN chmod 0644 /etc/cron.d/my-cronjob

# Copy the rest of the application code
COPY . .

# Grant execute permissions to the entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 5000

# 4. Use an entrypoint script to properly start both services
ENTRYPOINT ["entrypoint.sh"]