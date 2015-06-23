require "coffee-script"
require("buffertools").extend()
net = require "net"
express = require "express"
http = require "http"
connect = require "connect"

# prepare variables
streamOK = false
offlineSince = new Date()
onlineSince = null
silenceSince = new Date()

# Retrieve config from environment
streamUrl = process.env.STREAM_URL
silenceThreshold = process.env.SILENCE_THRESHOLD or -12
httpPort = process.env.HTTP_PORT or 8000

unless streamUrl
  console.log "Error: STREAM_URL must be set in environment"
  process.exit()
  
  
# function that returns the current info as object
getStatus = () =>
  now = new Date()
  result =
    url: streamUrl
    silenceThreshold: silenceThreshold
    status: if streamOK then "OK" else "ERROR"
    now: now
    onlinceSince: onlineSince
    onlineDuration: if onlineSince then Math.floor((now.getTime() - onlineSince.getTime()) / 1000) else 0
    offlinceSince: offlineSince
    offlineDuration: if offlineSince then Math.floor((now.getTime() - offlineSince.getTime()) / 1000) else 0
    silenceSince: silenceSince
    silenceDuration: Math.floor((now.getTime() - silenceSince.getTime()) / 1000)
    

# Create web app
app = express()
app.set "json spaces", 2
server = http.Server(app)
server.listen 8000

# Root document returns entire status
app.get "/", (req, res, next) ->
  res.jsonp getStatus()

# Other URLs return single fields from the status
app.get "/:key", (req, res, next) ->
  res.sendStatus getStatus()[req.params.key]


console.log "Stream monitor for %s started on port %d", streamUrl, httpPort
