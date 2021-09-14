"""
papahd.live

method:
soccer24hdcom
"""

NAME = "papahd.live"
KEY = "papahdlive"
BASE = "papahd.live"

try:
    from .soccer24hdcom import get_urls
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

    test("http://papahd.live/real-madrid-vs-real-sociedad/")
    test_can_handle("http://papahd.live/real-madrid-vs-real-sociedad/")
