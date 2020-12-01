ARG PYTHON_VERSION="3.9.0"
FROM python:$PYTHON_VERSION-slim as build

ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Upgrade pip and then install build tools
RUN pip install -U pip && \
    pip install -U wheel setuptools wheel check-wheel-contents

WORKDIR /code/

# Build The Application and validate wheel contents
COPY . .
RUN python setup.py bdist_wheel && \
    find dist/ -type f -name *.whl -exec check-wheel-contents {} \;

# For debugging the Build Stage    
CMD ["bash"]



## App Stage
ARG PYTHON_VERSION="3.9.0"
FROM python:$PYTHON_VERSION-slim as app

# Define workdir
ENV HOME="/app"
WORKDIR $HOME

# Define env vars
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_NO_CACHE_DIR=1
ENV PATH="$HOME/.local/bin:${PATH}"

# Run as a non-root user
RUN addgroup appgroup && useradd appuser -g appgroup --home-dir "$HOME" && \
    chown -R appuser:appgroup .
USER appuser

# Upgrade pip
RUN pip install --user --upgrade pip && \
    pip install --user --upgrade wheel setuptools

# Install requirements
COPY --from=build /code/requirements.txt ./
RUN pip install -r requirements.txt && \
    rm requirements.txt

# Copy artifacts and requirements.txt from Build Stage
COPY --from=build /code/dist/ ./

# Install the application from local wheel package
RUN find . -type f -name *.whl -exec pip install --user {} \; -exec rm {} \;
CMD ["gitlab_stats"]
