
# Download official Docker Python Image
FROM python:3.9-slim-bullseye

# By default, listen on port 5000
EXPOSE 5000/tcp

# Set working dir
WORKDIR /code

# Copy Dependency Files
COPY requirements.txt .

# Install Dependencies
RUN pip install requirements.txt

# Copy Source code to WORKDIR
COPY src/ .

# Run Container
CMD [ "python", "./app.py" ]