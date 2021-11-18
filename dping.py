#!/usr/bin/python
import os
import sys
import subprocess
import time
import argparse
import datetime
import re
from itertools import islice
from subprocess import Popen, PIPE

 
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
parser.print_help()
args = parser.parse_args()
hostname = args.Host
if args.timestamp:
    print ("Timestamp mode selected")
    print ("Pinging host:", hostname)
    

    with open(os.devnull, 'wb') as devnull:
        response = Popen(['/usr/sbin/ping', '-c1', '-W1', hostname ],
                stdout=subprocess.PIPE, stderr=devnull)
        output=response.communicate()
        test_string = str(output)
        #print ("DEBUG: Output:", test_string)
        my_pattern='ttl'
        res=test_string.rstrip('\n\n').split(" ")
        ttl=re.sub(r'\\n\\n\',','', res[19])
        ttl_up=re.sub(r'\\n\\n\',','', res[11])
        #print ("DEBUG: res:", res) 
        #print("DEBUG: TTL:", ttl)

        #nprint ("DEBUG: Response:", response)
        # Establish pattern for getting return code of ping..
        pattern = 'returncode: 1'
        test_string2 = str(response)
        result = re.search(pattern, test_string2)
        count = 0 
        if result:
            #print("DEBUG: Pattern Found")
            while 1:

                ct = datetime.datetime.now()
                ctf = ct.strftime("%Y-%m-%d %H:%M:%S")
                print (ctf, "\033[1;31;40m" u"\u2588" "\033[0;37;40m", "Down | ttl", ttl, "count:", count, end='\n', flush=True )
                time.sleep(args.sleep)
                count = count+1
        else:
            #print("DEBUG: in else loop")
            while 1:
                ct = datetime.datetime.now()
                ctf = ct.strftime("%Y-%m-%d %H:%M:%S")
                print (ctf,  "\033[1;32;40m" u"\u2588" "\033[0;37;40m", "Up |",ttl_up, "count:", count, end='\n', flush=True )
                time.sleep(args.sleep)
                count = count+1
    #else:
     #   print (" Error code ", response )

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
