import random
import urllib2
import re
import os
import subprocess
import time

# Given the HTML for a OHC page, attempts to grab the theme from that page.
# Might fail on weird weeks.
def find_theme(html):
    theme = re.findall('(Tonights|Tonight\'s|Todays|Today\'s|This weeks) theme (is|will be):? "(.*)"', html)
    if len(theme) > 0:
        return theme[0][2]
    return "???"

# Given an OHC # and a ranking from the top of the page, returns the path to
# the song at that rank.
def get_ohc_url(which_ohc):
    idx = 0
    result = ""

    # Download OHC page
    response = urllib2.urlopen('http://compo.thasauce.net/rounds/view/OHC%s' % which_ohc)
    html = response.read()
    
    result += "{"
    result += "num: %s," % which_ohc
    result += "theme: '%s'," % find_theme(html)
    
    # skip over "Materials" section, if there is one
    while True:
        i = html.find('a href="/files/', idx)
        if html.find('Download', idx) - i > 100:
            idx = html.find('a href="/files/', idx) + 1
        else: 
            break
    
    url = ""

    # Hack our way through the top 5
    for x in range(5):
        # hack the title
        starttitle = html.find('item_head">', idx) + len('item_head">\n')
        endtitle = html.find('<span>', starttitle)
        title = html[starttitle:endtitle]
        title = title.replace('"', '') 

        result += 'title%d: "%s",' % (x, html[starttitle:endtitle])

        # hack the user
        # beautifulsoup? what's that?
        user = html.find('">', endtitle) + len('">')
        enduser = html.find('</a>', user)
        result += "user%d: '%s'," % (x, html[user:enduser])

        idx = html.find('a href="/files/', idx + 1)
        endidx = html.find('">Download', idx)
        url = "http://compo.thasauce.net" + html[idx + len('a href="'):endidx ]
        result += "url%d: '%s'" % (x, url)
    result += "},"

    return result

for ohc in range(229):
  ohc_num = str(ohc).zfill(3)
  json = get_ohc_url(ohc_num)
  if len(json) > 10000: continue
  print json
