"""
myoplay.live

method:
search for iframe https://angelthump.com/{id}/embed
m3u8 = https://video-cdn.angelthump.com/hls/{id}.m3u8
"""

NAME = "myoplay.live"
KEY = "myoplaylive"
BASE = "myoplay.live"
M3U8_URL = "https://video-cdn.angelthump.com/hls/%s.m3u8"

if __name__ == "__main__":
    import sys
    import os
    import json
    # ugly hack, but oh well
    sys.path.append("%s/.kodi/addons/plugin.video.tide" % os.getenv("HOME"))

try:
    from router import PLUGIN, path_for_source
    from helpers import http_get, header_random_agent, log
    from common import add_headers, add_items, parse_url
except Exception as e:
    print(e)

import re
import urllib

def can_handle(url):
    p_url = parse_url(url)
    return p_url.netloc == BASE

@PLUGIN.route("%s/<url>" % path_for_source(KEY))
def root(url):
    ref_url = urllib.unquote(url).decode('utf8')
    urls = get_urls(ref_url)
    add_items(urls, ref_url, PLUGIN)

def get_urls(url):
    headers = header_random_agent()
    html = http_get(url, headers=headers)
    angel_id = re.search(r"angelthump.com/(.*?)/embed", html.text).group(1)
    headers.update({
        "Referer": url,
        "Origin": url,
    })
    return [M3U8_URL % angel_id]

if __name__ == "__main__":
    def test(url):
        vid_urls = get_urls(url)
        print(vid_urls)

    def test_can_handle(url):
        print(can_handle(url))

    test("https://myoplay.live/oplive/")
    test_can_handle("https://myoplay.live/oplive/")
