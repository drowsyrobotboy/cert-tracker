#!/usr/bin/python3

# This one is out-dated

import os
import subprocess
import sys
import OpenSSL
import ssl, socket
from flask import Flask, request, json, jsonify

# Define the Cert class
class Cert:
    def __init__(self, hostname, port, expiry):
        self.hostname = hostname
        self.port = port
        self.expiry = expiry

cmd = "grep -i ServerName "+sys.argv[1]+" | grep -v ^\# | xargs"
ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
output = ps.communicate()[0]

arr = (output.decode('utf-8').split("ServerName")) # get an array of all certs
arr.pop(0) # remove first entry as it will be empty
dist_arr = list(set(arr)) # converting to a set to remove dups
arr = [] # empty the original array to fill with Cert objects

for x in dist_arr:
    x = x.strip()
    print("\u25B6\uFE0F Fetching cert: "+ x);
    try:
        cert_text=ssl.get_server_certificate((x.split(":")[0], x.split(":")[1]))
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_text)

        # append the json version of Cert object to the array. Using .__dict_ to convert the object to json_
        ct = Cert(x.split(":")[0], x.split(":")[1],x509.get_notAfter().decode('utf-8'))
        arr.append(ct.__dict__)
        print("✅ Done!")
    except:
        print("🚨 Error in fetching cert for: "+x+" ... Skipping")

# Web using Flaskapp
app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return jsonify(arr)

app.run()
