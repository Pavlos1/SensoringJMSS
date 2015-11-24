#!/usr/local/bin/python
# A utility for logging in to the Monash network, based loosely on:
# https://gist.github.com/eduvik/1e2289d0fa86b2a79798
# Written by Pavel
# License: BSD

import urllib
import urllib2
import cookielib
import os

print "Please enter your Authcate credentials..."
username = raw_input("Username: ")
password = raw_input("Password: ")
print "Processing, please wait..."

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

location_request = urllib2.Request("https://my.monash.edu.au")
location = opener.open(location_request).geturl()
data = { "UserName": "Monash\\"+username,
         "Password": password,
         "AuthMethod": "FormsAuthentication" }
         
headers = { "Referer": location,
            "Location": location }
            
req = urllib2.Request(location, urllib.urlencode(data), headers)
resp = opener.open(req)
req2 = urllib2.Request("https://my.monash.edu.au", None, headers)
resp2 = opener.open(req2)
html = resp2.read()

print "Login completed. The resulting page has been saved in ~/misc/login.html"
fp = open(os.path.expanduser("~/misc/login.html"), "w")
fp.write(html)
fp.close()
