"""
redsoccer.info

method:
generic m3u8 searcher
"""

NAME = "redsoccer.info"
KEY = "redsoccerinfo"
BASE = "redsoccer.info"

try:
    from .generic_m3u8_searcher import get_urls
    from router import PLUGIN, path_for_source
    from .common import gen_can_handle, gen_root
except Exception as e:
    print(e)

import urllib

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

    test("http://redsoccer.info/xo_event/cricket/")
    test_can_handle("http://redsoccer.info/xo_event/cricket/")
