"""
blacktiesports.net

method:
generic/dubzalgo
"""

NAME = "blacktiesports.net"
KEY = "blacktiesportsnet"
BASE = "blacktiesports.net"

try:
    from sources.generic_m3u8_searcher import dubzalgo as get_urls
    from router import PLUGIN, path_for_source
    from sources.common import gen_root, gen_can_handle
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

    test("http://blacktiesports.net/soccer1")
    test_can_handle("http://blacktiesports.net/soccer1")
