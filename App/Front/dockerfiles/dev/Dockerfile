# ============================
# Build stage
# ============================
FROM oven/bun:1 AS build
WORKDIR /app

COPY ../front/package.json ../front/bun.lock ./
RUN bun install --frozen-lockfile

COPY ../front/ .
ENV NODE_ENV=production
# RUN bun run build
RUN NODE_OPTIONS="--trace-uncaught" bun run build


# ============================
# Runtime stage
# ============================
FROM oven/bun:1 AS runtime
WORKDIR /app

COPY --from=build /app/build ./build
COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/package.json ./

USER bun
EXPOSE 3000
CMD ["bun", "build/index.js"]
