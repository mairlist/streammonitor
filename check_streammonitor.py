#!/usr/bin/env python3
# author Marcus Aßhauer <github@asshaueronline.de>
# version: 0.1

# import needed functions
import urllib.request
import datetime
import json
import argparse

# function to get the JSON data from Streammonitor
def getResponse(url):
    operUrl = urllib.request.urlopen(url)
    if(operUrl.getcode()==200):
        data = operUrl.read()
        jsonData = json.loads(data)
    else:
        # UNKNOWN state if Streammonitor is not reachable
        print("UNKOWN - Error receiving data", operUrl.getcode())
        exit(3)
    return jsonData

def main():
    # argparser for handling commandline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="URL to streammonitor",required=True)
    parser.add_argument("-c", "--crit", default=1800, type=int, help="seconds of silence after which silence gets critical. Default=1800",required=False)
    parser.add_argument("-w", "--warn", default=0, type=int, help="seconds after reconnect the check should stay in WARN state. Default=0",required=False)
    args = parser.parse_args()
    jsonData = getResponse(args.url)

    # generate more human readable time ranges for online-, offline-, and silenceDuration
    # this will be only used in check output
    onlineSince=datetime.timedelta(seconds=jsonData["onlineDuration"])
    offlineSince=datetime.timedelta(seconds=jsonData["offlineDuration"])
    silenceSince=datetime.timedelta(seconds=jsonData["silenceDuration"])
    

    # checking the state
    if jsonData["status"] == "OK":
        # if stream is silent and not longer than crit value make it WARN state
        if jsonData["silenceDuration"] > 0 and jsonData["silenceDuration"] < args.crit:
            print(f'WARN - Stream {jsonData["url"]} is connected but silent since {silenceSince} (h:m:s)!| silenceDuration={jsonData["silenceDuration"]}s;;{args.crit};;; onlineDuration={jsonData["onlineDuration"]}s;{args.warn};;;; offlineDuration={jsonData["offlineDuration"]}s;;;;;')
            exit(1)
        # if stream is silent longer than crit vaule make it CRIT state
        elif jsonData["silenceDuration"] > args.crit: 
            print(f'CRIT - Stream {jsonData["url"]} is connected but silent since {silenceSince} (h:m:s)!| silenceDuration={jsonData["silenceDuration"]}s;;{args.crit};;; onlineDuration={jsonData["onlineDuration"]}s;{args.warn};;;; offlineDuration={jsonData["offlineDuration"]}s;;;;;')
            exit(2)
        # if stream is newly connected it will be WARN state until args.warn seconds
        if jsonData["onlineDuration"] < args.warn:
            print(f'WARN - Stream {jsonData["url"]} is connected but less than {args.warn} seconds!| silenceDuration={jsonData["silenceDuration"]}s;;{args.crit};;; onlineDuration={jsonData["onlineDuration"]}s;{args.warn};;;; offlineDuration={jsonData["offlineDuration"]}s;;;;;')
            exit(1)
        # if status ok and stream is not silent everything is OK
        print(f'OK - Stream {jsonData["url"]} is connected and playing since {onlineSince} (h:m:s)| silenceDuration={jsonData["silenceDuration"]}s;;{args.crit};;; onlineDuration={jsonData["onlineDuration"]}s;{args.warn};;;; offlineDuration={jsonData["offlineDuration"]}s;;;;;')
        exit(0)
    else:
        # if stream is not connected make it CRIT state
        print(f'CRIT - Stream {jsonData["url"]} is not connected! since {offlineSince} (h:m:s)| silenceDuration={jsonData["silenceDuration"]}s;;{args.crit};;; onlineDuration={jsonData["onlineDuration"]}s;{args.warn};;;; offlineDuration={jsonData["offlineDuration"]}s;;;;;')
        exit(2)

if __name__ == '__main__':
    main()
