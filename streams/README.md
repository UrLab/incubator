# UrLaB Live Stream

A simple flow is the following:

OBS Studio --rtmp--> Node-Media-Server --https--> Browsers

## Configuration

Update the url in the template according to the stream you want to display.

## Streaming server

Install [Node-Media-Server [1]](https://github.com/illuspas/Node-Media-Server) 
on a server with enough upload bandwidth for all viewers (depending on the emitter
settings, usually between 500kbps/2Mbps * number of viewers).

You can run it using Docker:
```shell
docker run --name nms -d -p 1935:1935 -p 8000:8000 illuspas/node-media-server
```

[1] https://github.com/illuspas/Node-Media-Server
