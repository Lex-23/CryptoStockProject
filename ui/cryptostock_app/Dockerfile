FROM node:14-alpine

WORKDIR /app

ARG REACT_APP_BASE_URL="http://127.0.0.1:8000/api/"

COPY package.json /app
RUN npm install

COPY . .
RUN npm run build
