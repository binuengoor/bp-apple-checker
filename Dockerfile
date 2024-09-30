# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the timezone to US Eastern Time
RUN apt-get update && apt-get install -y tzdata
ENV TZ=America/New_York

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port 3767 to the world outside this container
EXPOSE 3767

# Set the entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Run main.py when the container launches
CMD ["python", "/usr/src/app/main.py"]