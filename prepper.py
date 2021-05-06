#!/usr/bin/python3

import os
import subprocess
import sys
import OpenSSL

# Define the Cert class
class Cert:
    def __init__(self, name, expiry):
        self.name = name
        self.expiry = expiry

cmd = "grep -i SSLCertificateFile "+sys.argv[1]+" | grep -v ^\# | xargs"
ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
output = ps.communicate()[0]
# The following command prints as b'...'. We need to decode the bytes
# print(output)

arr = (output.decode('utf-8').split("SSLCertificateFile")) # get an array of all certs
arr.pop(0) # remove first entry as it will be empty
dist_arr = list(set(arr)) # converting to a set to remove dups
arr = [] # empty the original array to fill with Cert objects

for x in dist_arr:
    x = x.strip()
    with open(x, "r") as cert_file:
        cert_text = cert_file.read()
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_text)

    arr.append(Cert(x,x509.get_notAfter().decode('utf-8')))

for c in arr:
    print(c.name, c.expiry)
