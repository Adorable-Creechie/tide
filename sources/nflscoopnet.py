"""
nflscoop.net

method:
generic m3u8 searcher
"""

NAME = "nflscoop.net"
KEY = "nflscoopnet"
BASE = "nflscoop.net"

try:
    from .generic_m3u8_searcher import get_urls
    from router import PLUGIN, path_for_source
    from .common import gen_can_handle, gen_root
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

    test("https://nflscoop.net/25postday/gday1/")
    test_can_handle("https://nflscoop.net/25postday/gday1/")
