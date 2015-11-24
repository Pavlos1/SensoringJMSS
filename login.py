#!/usr/local/bin/python
# A utility for logging in to the Monash network, based loosely on:
# https://gist.github.com/eduvik/1e2289d0fa86b2a79798
# Written by Pavel
# License: BSD

import urllib
import urllib2

print "Please enter your Authcate credentials..."
username = raw_input("Username: ")
password = raw_input("Password: ")
print "Processing, please wait..."

location = urllib2.urlopen('https://my.monash.edu.au').geturl()
data = { "UserName": "Monash%5C"+username,
         "Password": password,
         "AuthMethod": "FormsAuthentication" }
req = urllib2.Request(location, urllib.urlencode(data))
resp = urllib2.urlopen(req)
html = resp.read()

print "Login completed. The resulting page has been saved in ~/misc/login.html"
fp = open("~/login.html", "w")
fp.write(html)
fp.close()
