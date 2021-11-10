# pull official base image
FROM python:3

# set environment variables
ENV PYTHONUNBUFFERED=1

# set work directory
WORKDIR /code


COPY pyproject.toml poetry.lock /code/

# Upgrade pip and install python packages for code
RUN pip install --upgrade --no-cache-dir pip poetry \
    && poetry --version \
    # Configure to use system instead of virtualenvs
    && poetry config virtualenvs.create false \
    && poetry install --no-root \
    # Remove installer
    && pip uninstall -y poetry virtualenv-clone virtualenv

# copy project
COPY . /code/

# EXPOSE 8050