"""
liveonscore.to

method:
get vidgstream variable
GET HLS_URL
json data {
 "idgstream": UrlID, "serverid": ""
}
where UrlID: vidgstream 
"""

NAME = "liveonscore.to"
KEY = "liveonscoreto"
BASE = "liveonscore.to"
HLS_URL = "http://liveonscore.to/gethls"

if __name__ == "__main__":
    import sys
    import os
    import json
    # ugly hack, but oh well
    sys.path.append("%s/.kodi/addons/plugin.video.tide" % os.getenv("HOME"))

try:
    from router import PLUGIN, path_for_source
    from helpers import http_get, header_random_agent, log
    from .common import add_headers, add_items, parse_url
except Exception as e:
    print(e)

import urllib
import re
from bs4 import BeautifulSoup 

def can_handle(url):
    p_url = parse_url(url)
    return p_url.netloc == BASE

@PLUGIN.route("%s/<url>" % path_for_source(KEY))
def root(url):
    ref_url = urllib.parse.unquote(url)
    urls = get_urls(ref_url)
    add_items(urls, ref_url, PLUGIN)

def get_urls(url):
    headers = header_random_agent()
    p_url = parse_url(url)
    html = http_get(url, headers=headers)
    vidgstream = re.search(r'var vidgstream = \"(.*)\"', html.text).group(1)
    params = {
        "idgstream": vidgstream,
        "serverid": "",
    }
    headers.update({"Referer": url, "Origin": url, "Accept-Encoding": "compress"})
    resp = http_get(HLS_URL, params = params, headers = headers)
    json = resp.json()
    rawUrl = json["rawUrl"]
    if rawUrl == 'null':
        return []
    return [rawUrl]

if __name__ == "__main__":
    def test(url):
        vid_urls = get_urls(url)
        print(vid_urls)

    def test_can_handle(url):
        print(can_handle(url))

    test("http://liveonscore.to/soccer-streams/serie-a/sampdoria-vs-inter/32417/")
    test_can_handle("http://liveonscore.to/soccer-streams/serie-a/sampdoria-vs-inter/32417/")
