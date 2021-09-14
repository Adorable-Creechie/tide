"""
hhdstreams.club

method:
first iframe
search for m3u8
"""

NAME = "hhdstreams.club"
KEY = "hhdstreamsclub"
BASE = "hhdstreams.club"

try:
    from .generic_m3u8_searcher import get_urls as gen_get_urls
    from router import PLUGIN, path_for_source
    from helpers import http_get, header_random_agent, log
    from .common import add_headers, add_items, parse_url, gen_can_handle, gen_root
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
    return gen_get_urls(iframe_url)

if __name__ == "__main__":
    def test(url):
        vid_urls = get_urls(url)
        print(vid_urls)

    def test_can_handle(url):
        print(can_handle(url))

    test("http://hhdstreams.club/hd/ch5.php")
    test_can_handle("http://hhdstreams.club/hd/ch5.php")
