
# Download official Docker Python Image
FROM python:3.9-slim-bullseye

# Set working dir
WORKDIR /code

# Copy Dependency Files
COPY Pipfile* .

# Install Dependencies
RUN pip install pipenv && \
    pipenv install

# Copy Source code to WORKDIR
COPY src/ .

# Run Container
CMD [ "python", "./app.py" ]