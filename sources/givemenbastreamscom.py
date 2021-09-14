"""
givemenbastreams.com

method:
second iframe -> m3u8
"""

NAME = "givemenbaststreams.com"
KEY = "givemenbastreamscom"
BASE = "givemenbastreams.com"

try:
    from .generic_m3u8_searcher import get_urls as gen_get_urls
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
    second_iframe_url = soup.find_all("iframe")[1].get("src")
    return gen_get_urls(second_iframe_url)

if __name__ == "__main__":
    def test(url):
        vid_urls = get_urls(url)
        print(vid_urls)

    def test_can_handle(url):
        print(can_handle(url))

    test("http://givemenbastreams.com/nba/man-utd-live-stream")
    test_can_handle("http://givemenbastreams.com/nba/man-utd-live-stream")
