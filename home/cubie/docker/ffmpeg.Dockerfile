FROM arm32v7/alpine:latest

RUN apk add --no-cache ffmpeg

WORKDIR /app

ENTRYPOINT ["ffmpeg"]
