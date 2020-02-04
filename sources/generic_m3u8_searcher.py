NAME = "GenericM3U8Searcher"
KEY = "genericm3u8searcher"

if __name__ == "__main__":
    import sys
    import os
    import json

    # ugly hack, but oh well
    sys.path.append("%s/.kodi/addons/plugin.video.tide" % os.getenv("HOME"))
else:
    import xbmc
    from xbmcplugin import (
        addDirectoryItem,
        addDirectoryItems,
        endOfDirectory,
    )
    from xbmcgui import (
        ListItem,
    )

try:
    from router import PLUGIN, path_for_source
    from helpers import http_get, log
except Exception as e:
    print(e)

try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse
import urllib
import re
from bs4 import BeautifulSoup 

def can_handle(url):
    return False

@PLUGIN.route("%s/<url>" % path_for_source(KEY))
def root(url):
    r_url = urllib.unquote(url).decode('utf8')
    urls = get_urls(r_url)
    for i in range(len(urls)):
        title = "Source %d" % i
        li = ListItem(title)
        li.setInfo('video', {'title': title,
                                    'mediatype': 'video'})
        m3u8_url = urllib.quote(urls[i], safe="%/:=&?~#+!$,;'@()*[]")
        addDirectoryItem(PLUGIN.handle, add_headers(m3u8_url, r_url), li)
    if (len(urls) == 0):
        li = ListItem("No playable sources found")
        addDirectoryItem(PLUGIN.handle, "", li)
    endOfDirectory(PLUGIN.handle)

def add_headers(url, referer, origin = None):
    if not origin:
        origin = referer
    return "%s|referer=%s|origin=%s" % (url, referer, origin)

def get_urls(url):
    parsed_url = urlparse(url)
    html = http_get(url)
    urls = re.findall(r'(?:https?:)?//.*?\.m3u8', html.text)
    formatted = []
    for u in urls:
        if u.startswith("//"):
            formatted.append("%s:%s" % (parsed_url.scheme, u))
        else:
            formatted.append(u)
    return formatted

if __name__ == "__main__":
    def test(url):
        vid_urls = get_urls(url)
        print(vid_urls)

    test("https://videojs.github.io/videojs-contrib-hls/")
