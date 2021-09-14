"""
daddylive.me

method:
first iframe -> m3u8
"""

NAME = "daddylive.me"
KEY = "daddyliveme"
BASE = "daddylive.me"

try:
    from .generic_m3u8_searcher import get_urls as gen_get_urls
    from router import PLUGIN, path_for_source
    from helpers import http_get, header_random_agent, log
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
    cookies = {}
    p_url = parse_url(url)
    html = http_get(url, headers=headers)
    cookies.update(html.cookies)
    soup = BeautifulSoup(html.text, 'html.parser')
    iframe_url = soup.find("iframe").get("src")
    return gen_get_urls(iframe_url)

if __name__ == "__main__":
    def test(url):
        vid_urls = get_urls(url)
        print(vid_urls)

    def test_can_handle(url):
        print(can_handle(url))

    test("https://daddylive.me/stream/stream-4.php")
    test_can_handle("https://daddylive.me/stream/stream-4.php")
