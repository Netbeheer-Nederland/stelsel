FROM python:3.13-alpine3.23

# Set environment variables to avoid interactive prompts during package installation
ENV RUNNING_IN_DOCKER=true
ENV PYTHONUNBUFFERED=1

EXPOSE 4000

WORKDIR /workspace
COPY . /workspace

# Install required packages
RUN apk add --no-cache \
    build-base \
    bash=5.3.3-r1 \
    bc=1.08.2-r0 \
    git=2.52.0-r0 \
    github-cli=2.83.0-r2 \
    ruby=3.4.8-r0 \
    ruby-dev=3.4.8-r0 \
    ruby-bundler=2.6.9-r0

# Install Python project dependencies
RUN pip install -r requirements.txt

# Install Ruby dependencies
RUN gem install --no-document just-the-docs -v '~> 0.7.0'

# Metadata
LABEL org.opencontainers.image.source=https://github.com/netbeheer-nederland/stelsel
LABEL org.opencontainers.image.description="Nederland environment for modeling national energy registers and generating documentation and schemas."
LABEL org.opencontainers.image.licenses=Apache-2.0
