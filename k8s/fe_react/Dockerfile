ARG FE_BUILD_IMAGE="fe-build:latest"
FROM ${FE_BUILD_IMAGE} AS builder

FROM nginx:1.21-alpine

COPY --from=builder /app/build/ /usr/share/nginx/html
