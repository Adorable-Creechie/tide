"""
uhdstreams.club

method:
generic/first_iframe_get_urls
"""

NAME = "uhdstreams.club"
KEY = "uhdstreamsclub"
BASE = "uhdstreams.club"

try:
    from sources.generic_m3u8_searcher import first_iframe_get_urls as get_urls
    from router import PLUGIN, path_for_source
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

    test("http://uhdstreams.club/hd/ch1.php")
    test_can_handle("http://uhdstreams.club/hd/ch1.php")
