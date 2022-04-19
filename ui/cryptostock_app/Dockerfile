FROM node:14-alpine

WORKDIR /app
RUN npm set timeout 240000
COPY package.json /app

RUN npm install

COPY . .
RUN ls -a

RUN npm run build

RUN mv /app/build /opt/fe/
