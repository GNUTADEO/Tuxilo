FROM node:25-alpine AS base
RUN npm install -g pnpm

# Stage 1: build
FROM base AS build
WORKDIR /usr/src/app

# Copy package files first for caching
COPY ./front/package.json ./front/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY front .

# Build the app
RUN pnpm run build

# Stage 2: runner
FROM base AS runner
WORKDIR /usr/src/app

# Copy built files & dependencies
COPY front .
COPY --from=build /usr/src/app/node_modules ./node_modules
COPY --from=build /usr/src/app/build ./build
COPY --from=build /usr/src/app/.svelte-kit ./.svelte-kit
COPY --from=build /usr/src/app/package.json ./package.json

# Production server
CMD ["pnpm", "run", "start", "--port", "${PORT_FRONT:-3000}"]