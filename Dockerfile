FROM python:3.13-alpine3.23

# Set environment variables to avoid interactive prompts during package installation
ENV RUNNING_IN_DOCKER=true
ENV PYTHONUNBUFFERED=1

EXPOSE 4000

COPY requirements.txt Gemfile /tmp/

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
RUN pip install -r /tmp/requirements.txt

# Install Ruby dependencies
RUN grep ^gem /tmp/Gemfile | cut -d ' ' -f 2- | sed 's/, / -v /' | xargs gem install --no-document

# Initialize non-root user
ENV USER=developer
ENV GROUPNAME=$USER
ENV UID=1000
ENV GID=$UID

RUN addgroup \
    --gid "$GID" \
    "$GROUPNAME" \
&&  adduser \
    --disabled-password \
    --gecos "" \
    --ingroup "$GROUPNAME" \
    --home /home/developer \
    --uid "$UID" \
    $USER

USER $USER

WORKDIR /workspace
COPY . /workspace

# Metadata
LABEL org.opencontainers.image.source=https://github.com/netbeheer-nederland/stelsel
LABEL org.opencontainers.image.description="Nederland environment for modeling national energy registers and generating documentation and schemas."
LABEL org.opencontainers.image.licenses=Apache-2.0
