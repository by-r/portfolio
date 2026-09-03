FROM node:20-alpine AS dependencies

WORKDIR /app

COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

# Used by compose.dev.yml. Source is bind-mounted for Vite HMR.
FROM dependencies AS development

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# Used by nginx/Dockerfile to create the production SPA bundle.
FROM dependencies AS build

COPY frontend/ ./

# Empty means requests use same-origin /api.
ARG VITE_API_URL=""
ENV VITE_API_URL=${VITE_API_URL}

RUN npm run build
