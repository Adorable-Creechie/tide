"""
bdnewszh.com

method:
first iframe
search for m3u8
"""

NAME = "bdnewszh.com"
KEY = "bdnewszhcom"
BASE = "bdnewszh.com"

try:
    from . import generic_m3u8_searcher
    from router import PLUGIN, path_for_source
    from helpers import http_get, header_random_agent
    from sources.common import parse_url, gen_can_handle, gen_root
except Exception as e:
    print(e)

import urllib
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
    iframe = soup.find("iframe")
    iframe_url = iframe.get("src")
    if iframe_url.startswith("//"):
        iframe_url = u"https:{}".format(iframe_url)
    return generic_m3u8_searcher.get_urls(iframe_url)

if __name__ == "__main__":
    def test(url):
        vid_urls = get_urls(url)
        print(vid_urls)

    def test_can_handle(url):
        print(can_handle(url))

    test("https://bdnewszh.com/watch/soccer/stream5/")
    test_can_handle("https://bdnewszh.com/watch/soccer/stream5/")
