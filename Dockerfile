# Use linuxserver/python as a parent image
FROM linuxserver/python:latest

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 3767 to the world outside this container
EXPOSE 3767

# Run main.py when the container launches
CMD ["python", "main.py"]