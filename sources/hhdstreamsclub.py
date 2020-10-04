"""
hhdstreams.club

method:
first iframe
search for m3u8
"""

NAME = "hhdstreams.club"
KEY = "hhdstreamsclub"
BASE = "hhdstreams.club"

if __name__ == "__main__":
    import sys
    import os
    import json
    # ugly hack, but oh well
    sys.path.append("%s/.kodi/addons/plugin.video.tide" % os.getenv("HOME"))

try:
    from router import PLUGIN, path_for_source
    from helpers import http_get, header_random_agent, log
    from common import add_headers, add_items, parse_url
except Exception as e:
    print(e)

import urllib
import re
from bs4 import BeautifulSoup 

def can_handle(url):
    p_url = parse_url(url)
    return p_url.netloc.strip("www.") == BASE

@PLUGIN.route("%s/<url>" % path_for_source(KEY))
def root(url):
    ref_url = urllib.unquote(url).decode('utf8')
    urls = get_urls(ref_url)
    add_items(urls, ref_url, PLUGIN)

def get_urls(url):
    headers = header_random_agent()
    p_url = parse_url(url)
    html = http_get(url, headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')
    iframe = soup.find("iframe")
    iframe_url = iframe.get("src")
    html = http_get(iframe_url, headers=headers)
    m3u8 = re.search(r"source: \'(.*)\'", html.text).group(1)
    return [m3u8]

if __name__ == "__main__":
    def test(url):
        vid_urls = get_urls(url)
        print(vid_urls)

    def test_can_handle(url):
        print(can_handle(url))

    test("http://hhdstreams.club/hd/ch5.php")
    test_can_handle("http://hhdstreams.club/hd/ch5.php")
