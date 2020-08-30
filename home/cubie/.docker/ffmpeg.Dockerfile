FROM armhf/alpine:latest

RUN apk add --no-cache ffmpeg

WORKDIR /ffmpeg

ENTRYPOINT ["ffmpeg"]
