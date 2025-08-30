# use Debian image with uv, no need for system Python
FROM ghcr.io/astral-sh/uv:debian AS build

# Use /app as the conventional working directory
WORKDIR /app

# copy all files needed for the build
COPY pyproject.toml .
COPY src ./src
COPY content ./content
COPY templates ./templates
COPY static ./static
COPY pages ./pages

# install Python with uv
RUN uv python install 3.12

# This one command does everything:
# 1. Creates a temporary virtual environment.
# 2. Reads pyproject.toml and installs all dependencies (Jinja2, etc.).
# 3. Runs our main build script using `python -m src.main`.
RUN uv run python -m src.main

# serve with Caddy
FROM caddy:alpine

# copy Caddy config
COPY Caddyfile /etc/caddy/Caddyfile

# copy generated static site from the build stage
COPY --from=build /app/output /srv/
