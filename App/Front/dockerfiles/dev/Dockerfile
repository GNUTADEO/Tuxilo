# ============================
# Build stage
# ============================
FROM oven/bun:1 AS build
WORKDIR /app

COPY ../front/package.json ../front/bun.lock ./
RUN bun install

COPY ../front/ .
ENV NODE_ENV=development
CMD ["bun", "run", "dev"]
