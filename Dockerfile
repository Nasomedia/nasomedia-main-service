FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Install Poetry
ENV POETRY_VERSION=1.1.11 
RUN pip install "poetry==$POETRY_VERSION"

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /app/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

ENV PYTHONPATH=/