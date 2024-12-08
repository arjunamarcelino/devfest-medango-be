# Use an official Python runtime as a parent image
FROM python:3.12.1-alpine 

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Install Python dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r  requirements.txt

ENV APP_HOME /root
WORKDIR $APP_HOME
COPY /app $APP_HOME/app

# Expose the port FastAPI will run on
EXPOSE 8080

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
