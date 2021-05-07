#!/usr/bin/python3

import os
import subprocess
import sys
import OpenSSL
import ssl, socket
import json
import logging
from datetime import datetime


# Set logging & othrs

logfile = os.path.dirname(os.path.realpath(__file__))+'/pepper.log'
outfile = os.path.dirname(os.path.realpath(__file__))+'/../html/pepper.json'
logging.basicConfig(filename=logfile, filemode='a', format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
dateformat = '%Y%m%d%H%M%SZ'

# Getting Hostnames
cmd = "grep -i ServerName "+sys.argv[1]+" | grep -v ^\# | xargs"
ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
output = ps.communicate()[0]
arr = (output.decode('utf-8').split("ServerName")) # get an array of all certs
arr.pop(0) # remove first entry as it will be empty
dist_arr = list(set(arr)) # converting to a set to remove dups
arr = [] # empty the original array to fill with Cert objects

# Function to fetch cert expiry date
def getExpiry(site, port):
    conn = ssl.create_connection((site, port))
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    sock = context.wrap_socket(conn, server_hostname=site)
    cert = ssl.DER_cert_to_PEM_cert(sock.getpeercert(True))
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert) 
    return datetime.strptime(x509.get_notAfter().decode(),dateformat).isoformat()


# Populating cert details
for x in dist_arr:
    x = x.strip()
    logging.info("\u25B6\uFE0F Fetching cert: "+ x)
    try:
        # append the json version to the array.
        arr.append({'hostname': x.split(":")[0], 'port': x.split(":")[1],'expiry': getExpiry(x.split(":")[0], x.split(":")[1])})
        logging.info("✅ Done!")
    except:
        logging.error("🚨 Error in fetching cert for: "+x+" ... Skipping")

f = open(outfile, "w")
f.write(json.dumps(arr))
f.close()