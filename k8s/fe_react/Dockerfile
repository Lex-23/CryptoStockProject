FROM fe-build:latest AS builder

FROM nginx:1.21-alpine

COPY --from=builder /app/build/ /usr/share/nginx/html
