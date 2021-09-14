"""
hazmo.watch

method:
first iframes path correlates to final iframe with m3u8
site = https://hazmo.watch/sports/stream01.html
first iframe = https://jamunanews.net/soccer/01_stream.php
m3u8 page = https://hazmo.stream/soccer/01_stream.php
"""

NAME = "hazmo.watch"
KEY = "hazmowatch"
BASE = "hazmo.watch"
BASE_STREAM = "hazmo.stream"
BASE_STREAM_REF = "https://hazmolive.stream"

try:
    from . import generic_m3u8_searcher
    from router import PLUGIN, path_for_source
    from helpers import http_get, header_random_agent
    from .common import parse_url, gen_can_handle, gen_root
except Exception as e:
    print(e)

import urllib
import base64
import re
from bs4 import BeautifulSoup 

can_handle = gen_can_handle(BASE)

@PLUGIN.route("%s/<url>" % path_for_source(KEY))
def root(url):
    gen_root(url, get_urls)

def get_urls(url):
    headers = header_random_agent()
    p_url = parse_url(url)
    html = http_get(url, headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')
    first_iframe_url = soup.find("iframe").get("src")
    f_url = parse_url(first_iframe_url)
    m3u8_page_url = "%s://%s%s" % (p_url.scheme, BASE_STREAM, f_url.path)
    headers.update({"Referer": BASE_STREAM_REF})
    html = http_get(m3u8_page_url, headers=headers)
    urls = generic_m3u8_searcher.search(html.text)
    return urls

if __name__ == "__main__":
    def test(url):
        vid_urls = get_urls(url)
        print(vid_urls)

    def test_can_handle(url):
        print(can_handle(url))

    test("https://hazmo.watch/sports/stream01.html")
    test_can_handle("https://hazmo.watch/sports/stream01.html")
