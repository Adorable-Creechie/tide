"""
dubzstreams.com

method:
get first iframe
search for window.atob
decode base64
"""

NAME = "dubzstreams.com"
KEY = "dubzstreamscom"
BASE = "www.dubzstreams.com"

try:
    from router import PLUGIN, path_for_source
    from helpers import http_get, header_random_agent, log
    from sources.common import parse_url, join_url, gen_can_handle, gen_root
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
    iframe = soup.find("iframe")
    iframe_url = join_url(url, iframe.get("src"))
    html = http_get(iframe_url, headers=headers)
    b64_str = re.search(r"window\.atob\('(.*)'\)", html.text).group(1)
    de_str = base64.b64decode(b64_str).decode("utf-8") 
    return [de_str]

if __name__ == "__main__":
    def test(url):
        vid_urls = get_urls(url)
        print(vid_urls)

    def test_can_handle(url):
        print(can_handle(url))

    test("http://www.dubzstreams.com/livegames/2021/08/livesoccerx/psg-20aug/")
    test_can_handle("http://www.dubzstreams.com/livegames/2021/08/livesoccerx/psg-20aug/")
