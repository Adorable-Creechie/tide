"""
Searches for all .m3u8 urls in the page and returns them.
Not very sophisticated, eh?
"""

NAME = "[COLOR orange]generic[/COLOR]"
KEY = "genericm3u8searcher"

try:
    from router import PLUGIN, path_for_source
    from helpers import http_get, header_random_agent
    from sources.common import add_items, parse_url
except Exception as e:
    print(e)

import urllib
import re
from bs4 import BeautifulSoup 

def can_handle(url):
    return False

@PLUGIN.route("%s/<url>" % path_for_source(KEY))
def root(url):
    ref_url = urllib.parse.unquote(url)
    urls = get_urls(ref_url)
    add_items(urls, ref_url, PLUGIN)

def get_urls(url):
    headers = header_random_agent()
    parsed_url = parse_url(url)
    html = http_get(url, headers=headers)
    return search_and_format(html.text)

def search_and_format(html):
    urls = search(html)
    return format(urls)

def format(urls):
    formatted = []
    for u in urls:
        u = u.strip("\'")
        u = u.strip("\"")
        if u.startswith("//"):
            formatted.append("%s:%s" % (parsed_url.scheme, u))
        else:
            formatted.append(u)
    no_duplicates = list(dict.fromkeys(formatted))
    return no_duplicates

def search(text):
    return re.findall(r'(?:https?:)?//.*?\.m3u8|\'(?:https?:)?//.*?\.m3u8.*?\'|\"(?:https?:)?//.*?\.m3u8.*?\"', text)

if __name__ == "__main__":
    def test(url):
        vid_urls = get_urls(url)
        print(vid_urls)

    test("https://videojs.github.io/videojs-contrib-hls/")
