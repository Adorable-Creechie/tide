"""
streamspass.com

hazmo.watch front
"""

NAME = "streamspass.com"
KEY = "streamspasscom"
BASE = "www.streamspass.com"

try:
    from sources.hazmowatch import get_urls
    from router import PLUGIN, path_for_source
    from sources.common import gen_can_handle, gen_root
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

if __name__ == "__main__":
    def test(url):
        vid_urls = get_urls(url)
        print(vid_urls)

    def test_can_handle(url):
        print(can_handle(url))

    test("https://www.streamspass.com/team/aston-villa")
    test_can_handle("https://www.streamspass.com/team/aston-villa")
