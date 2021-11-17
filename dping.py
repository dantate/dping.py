#!/usr/bin/python
import os
import sys
import subprocess
import time
import argparse
import datetime
 
sys.tracebacklimit = 0

# Initialize parser
parser = argparse.ArgumentParser()
#8parser.add_argument("-H", "--Host", help = "Host to Ping")
parser.add_argument("Host", help = "host")
parser.add_argument("-b", "--blocks", help = "Color Blocks Mode",
action="store_true")
parser.add_argument("-t", "--timestamp", help= "Timestamped Ping",
action="store_true")
parser.add_argument("-B", "--heartbeat", help= "Heartbeat", action="store_true")
parser.add_argument("-s", "--sleep", help= "Sleep for this long between pings",
        default=1)
args = parser.parse_args()
hostname = args.Host
if args.timestamp:
    print ("Timestamp mode selected")
    print ("Pinging host:", hostname)
    

    with open(os.devnull, 'wb') as devnull:
        response = subprocess.call(['/usr/sbin/ping', '-c1', '-W1', hostname ],
                stdout=devnull, stderr=subprocess.STDOUT)
    if response == 0:
        while 1:
            ct = datetime.datetime.now()
            print (ct,  "\033[1;32;40m" u"\u2588" "\033[0;37;40m", "Up", end='\n',
                flush=True )
            time.sleep(args.sleep)
    elif response == 1:
        while 1:
            ct = datetime.datetime.now()
            print (ct, "\033[1;31;40m" u"\u2588" "\033[0;37;40m", "Down", end='\n', flush=True )
            time.sleep(args.sleep)
    else:
        print (" Error code ", response )

if args.blocks:
    print ("Blocks mode selected")
    print ("Pinging host:", hostname)

    while 1:  
     with open(os.devnull, 'wb') as devnull:
         response = subprocess.call(['/usr/sbin/ping', '-c1', '-W1', hostname ],
         stdout=devnull, stderr=subprocess.STDOUT)
     if response == 0:
         print ( "\033[1;32;40m" u"\u2588" "\033[0;37;40m", end='', flush=True ) 
         time.sleep(args.sleep)
     elif response == 1:
         print ( "\033[1;31;40m" u"\u2588" "\033[0;37;40m", end='', flush=True ) 
         time.sleep(args.sleep)
     else: 
         print (" Error code ", response ) 

elif args.heartbeat:

    while 1:  
     with open(os.devnull, 'wb') as devnull:
        response = subprocess.check_call(['/usr/sbin/ping', '-c 1', hostname ],
                stdout=devnull, stderr=subprocess.STDOUT)
     if response == 0:
         print ( "\033[1;32;40m" u"\u2588" "\033[0;37;40m", end='\r' ) 
         time.sleep(args.sleep)
     else:
         print ( "\033[1;31;40m" u"\u2588" "\033[0;37;40m", end='', flush=True ) 
         time.sleep(args.sleep)
