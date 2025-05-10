# Use an official Python runtime as a parent image
FROM python:3.11.4-slim-bullseye

ENV PYTHONBUFFERED 1
ENV PORT 8080

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Run app.py when the container launches
CMD gunicorn base.wsgi:application --bind 0.0.0.0:"${PORT}"

# Make port 80 available to the world outside this container
EXPOSE ${PORT}
