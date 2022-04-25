FROM fe_build AS builder

FROM nginx:1.21-alpine

ARG fe_build_path=/opt/fe/

RUN rm /etc/nginx/conf.d/default.conf

COPY --from=builder /app/build ${fe_build_path}
COPY nginx.conf /etc/nginx/conf.d
