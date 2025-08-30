# use Debian image with uv, no need for system Python
FROM ghcr.io/astral-sh/uv:debian AS build

# explicit work dir is important
WORKDIR /src

# copy all files needed for the build
COPY pyproject.toml .
# COPY requirements.txt .
COPY src ./src
COPY content ./content

# install Python with uv
RUN uv python install 3.12

# run build process
RUN uv run python -m src.build

# serve with Caddy
FROM caddy:alpine

# copy Caddy config
COPY Caddyfile /etc/caddy/Caddyfile

# copy generated static site from the build stage
COPY --from=build /src/output /srv/
