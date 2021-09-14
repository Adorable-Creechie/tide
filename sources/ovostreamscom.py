"""
ovostreams.com

method:
first iframe
search for m3u8
"""

NAME = "ovostreams.com"
KEY = "ovostreamscom"
BASE = "ovostreams.com"

try:
    from . import generic_m3u8_searcher
    from router import PLUGIN, path_for_source
    from helpers import http_get, header_random_agent
    from .common import parse_url, gen_can_handle, gen_root
except Exception as e:
    print(e)

import urllib
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
    return generic_m3u8_searcher.get_urls(iframe_url)

if __name__ == "__main__":
    def test(url):
        vid_urls = get_urls(url)
        print(vid_urls)

    def test_can_handle(url):
        print(can_handle(url))

    test("http://www.ovostreams.com/liverpool-vs-burnley.php")
    test_can_handle("http://www.ovostreams.com/liverpool-vs-burnley.php")
