FROM node:25-alpine AS base
RUN npm install -g pnpm

# Stage 1: install dependencies
FROM base AS deps
WORKDIR /usr/src/app

# Only copy package files first for caching
COPY ./hub/package.json ./hub/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY hub .

# Stage 2: runner
FROM base AS runner
WORKDIR /usr/src/app

# Copy dependencies and package.json for scripts
COPY hub .
COPY --from=deps /usr/src/app/node_modules ./node_modules
COPY --from=deps /usr/src/app/package.json ./package.json

