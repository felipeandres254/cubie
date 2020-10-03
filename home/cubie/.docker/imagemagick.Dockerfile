FROM arm32v7/alpine:latest

RUN apk add --no-cache imagemagick

WORKDIR /app
