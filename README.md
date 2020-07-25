# streammonitor

streammonitor constantly monitors a Shoutcast/Icecast stream (only MP3 supported right now), and 
offers a simple HTTP API which returns basic information about the stream, how long it has
been online/offline, and the current duration of silence (signal below a certain threshold).

## Installation

streammonitor is designed to run as a Docker container.

To build the container, download/clone this repository, and run:

    docker build -t mairlist/streammonitor .

Then run the container, binding the HTTP port (8000), and passing the stream URL and silence threshold 
(in dBFS) as environment variables:

    docker run -p 8000:8000 -e STREAM_URL=http://sender.eldoradio.de:8000/192 \
                            -e SILENCE_THRESHOLD=-20 -e CHECK_INTERVAL=1000 \
                            mairlist/streammonitor 

``STREAM_URL`` is a required parameter. ``SILENCE_THRESHOLD`` can be ommited, in which case
-20 dBFS is assumed. ``CHECK_INTERVAL`` is also optional and defaults to 1000 ms.

The stream URL must be the actual URL for the stream (where the MP3 data is delivered),
**not** the URL of a pls/m3u file.

## HTTP Interface

When streammonitor is running, you can access the HTTP interface on the port you have
configured, e.g. at ``http://localhost:8000``.

Under the root URL, streammonitor returns a JSON object with all data about the current stream:

    {
      "url": "http://sender.eldoradio.de:8000/192",
      "silenceThreshold": -20,
      "status": "OK",
      "now": "2015-06-23T12:53:22.091Z",
      "onlinceSince": "2015-06-23T12:53:05.629Z",
      "onlineDuration": 16,
      "offlinceSince": null,
      "offlineDuration": 0,
      "silenceSince": "2015-06-23T12:53:21.903Z",
      "silenceDuration": 0
    }
    
Meaning of the individual fields:

- ``url`` and ``silenceThreshold`` are what you specified when you started streammonitor.
- ``status`` is either ``OK`` (stream is connected) or ``ERROR`` (stream is offline)
- ``now`` is the date/time this page was generated, for reference
- ``onlineSince`` is the date/time streammonitor (re-)connected to the stream, or ``null`` if the stream is offline
- ``onlineDuration`` is the number of seconds between ``onlineSince`` and ``now``, or 0 if the stream is offline
- ``offlineSince`` is the date/time streammonitor lost connection to the, or ``null`` if the stream is online
- ``offlineDuration`` is the number of seconds between ``offlineSince`` and ``now``, or 0 if the stream is online
- ``silenceSince`` is the date/time streammonitor received a sample louder than the specified silence threshold
- ``silenceDuration`` is the number of seconds between ``silenceSince`` and ``now``

You can also make an HTTP GET call to ``http://localhost:8000/value/<key>`` (where ``<key>`` is one of the field names above) to retrieve only a single field, as a plain text string (no JSON).

## License

streammonitor is released under the GNU AGPL v3.0.

Commercial licenses are available on request.

## Monitoring plugin for e.g. Nagios, Icinga, CheckMK, Shinken
Basic monitoring plugin in python3
You need to specify the url of the streammonitor you want to check. You can specify values for changing the state if the silence is longer than CRIT seconds or if you want an alarm for WARN seconds after a 
reconnection of the stream.  

- usage 

    ./check_streammonitor.py -h
    usage: check_streammonitor.py [-h] -u URL [-c CRIT] [-w WARN]    
    optional arguments:
      -h, --help            show this help message and exit
      -u URL, --url URL     URL to streammonitor
      -c CRIT, --crit CRIT  seconds of silence after which silence gets critical. Default=1800
      -w WARN, --warn WARN  seconds after reconnect the check should stay in WARN state. Default=0

- example output:

    ./check_streammonitor.py -u http://localhost:8000 -w 1800 -c 3600
    OK - Stream http://sender.eldoradio.de:8000/192 is connected and playing since 1:41:15 (h:m:s)| silenceDuration=0s;;3600;;; onlineDuration=6075s;1800;;;; offlineDuration=0s;;;;;

