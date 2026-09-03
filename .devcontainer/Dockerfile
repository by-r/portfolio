FROM mcr.microsoft.com/devcontainers/python:1-3.13-bookworm

# Keep the development container on the same uv release as the application image.
COPY --from=ghcr.io/astral-sh/uv:0.12.9 /uv /uvx /bin/
