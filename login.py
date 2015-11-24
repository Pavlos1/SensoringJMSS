#!/usr/local/bin/python
# A utility for logging in to the Monash network, based loosely on:
# https://gist.github.com/eduvik/1e2289d0fa86b2a79798
# Written by Pavel
# License: BSD

import urllib
import urllib2
import os

print "Please enter your Authcate credentials..."
username = raw_input("Username: ")
password = raw_input("Password: ")
print "Processing, please wait..."

location_request = urllib2.Request("https://my.monash.edu.au")
location = urllib2.urlopen(location_request).geturl()
data = { "UserName": "Monash\\"+username,
         "Password": password,
         "AuthMethod": "FormsAuthentication" }
         
headers = { "Referer": location,
            "Location": location }
            
req = urllib2.Request(location, urllib.urlencode(data), headers)
resp = urllib2.urlopen(req)
html = resp.read()

print "Login completed. The resulting page has been saved in ~/misc/login.html"
fp = open(os.path.expanduser("~/misc/login.html"), "w")
fp.write(html)
fp.close()
