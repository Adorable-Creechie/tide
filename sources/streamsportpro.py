"""
streamsport.pro

method:
first iframe -> m3u8
"""

NAME = "streamsport.pro"
KEY = "streamsportpro"
BASE = "streamsport.pro"

try:
    from router import PLUGIN, path_for_source
    from helpers import http_get, header_random_agent
    from .common import parse_url, gen_can_handle, gen_root
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
    f_iframe_1_url = soup.find("iframe").get("src")
    headers.update({"Referer": url})
    html = http_get(f"http:{f_iframe_1_url}", headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')
    source = re.search(r"source:'(.*?)',", html.text).group(1)
    return [source]

if __name__ == "__main__":
    def test(url):
        vid_urls = get_urls(url)
        print(vid_urls)

    def test_can_handle(url):
        print(can_handle(url))

    test("http://streamsport.pro/live/s14.php")
    test_can_handle("http://streamsport.pro/live/s14.php")
