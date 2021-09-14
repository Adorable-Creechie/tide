"""
reddit-streams.blogspot.com

method:
search for atob
decode base64
"""

NAME = "reddit-streams.blogspot.com"
KEY = "redditstreamsblogspotcom"
BASE = "reddit-streams.blogspot.com"

try:
    from router import PLUGIN, path_for_source
    from helpers import http_get, header_random_agent
    from .common import gen_can_handle, gen_root
except Exception as e:
    print(e)

import urllib
import base64

can_handle = gen_can_handle(BASE)

@PLUGIN.route("%s/<url>" % path_for_source(KEY))
def root(url):
    gen_root(url, get_urls)

def get_urls(url):
    headers = header_random_agent()
    html = http_get(url, headers=headers)
    b64_str = re.search(r"atob\('(.*?)'\)", html.text).group(1)
    de_str = base64.b64decode(b64_str).decode("utf-8") 
    return [de_str]

if __name__ == "__main__":
    def test(url):
        vid_urls = get_urls(url)
        print(vid_urls)

    def test_can_handle(url):
        print(can_handle(url))

    test("https://reddit-streams.blogspot.com/p/blog-page_86.html")
    test_can_handle("https://reddit-streams.blogspot.com/p/blog-page_86.html")
