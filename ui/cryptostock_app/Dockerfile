FROM node:14-alpine AS builder

WORKDIR /app

COPY package.json /app
RUN npm install

COPY . .
RUN npm run build

FROM nginx:1.21-alpine

ARG fe_build_path=/opt/fe/

RUN rm /etc/nginx/conf.d/default.conf

COPY --from=builder /app/build ${fe_build_path}
COPY nginx/nginx.conf /etc/nginx/conf.d
