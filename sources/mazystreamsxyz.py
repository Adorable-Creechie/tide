"""
mazystreams.xyz

method:
generic/get_urls
"""

NAME = "mazystreams.xyz"
KEY = "mazystreamssxyz"
BASE = "mazystreams.xyz"

try:
    from sources.generic_m3u8_searcher import get_urls
    from router import PLUGIN, path_for_source
    from helpers import http_get, header_random_agent
    from sources.common import gen_can_handle, gen_root
except Exception as e:
    print(e)

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

    test("http://mazystreams.xyz/event/atalanta-vs-udinese/s1.php")
    test_can_handle("http://mazystreams.xyz/event/atalanta-vs-udinese/s1.php")
