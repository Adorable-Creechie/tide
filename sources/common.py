import urllib
import re
try:
    from urllib.parse import urlparse, urljoin
except ImportError:
     from urlparse import urlparse, urljoin
try:
    import xbmc
    from xbmcplugin import (
        addDirectoryItem,
        addDirectoryItems,
        endOfDirectory,
    )
    from xbmcgui import (
        ListItem,
    )
except:
    pass

def add_headers(url, referer, origin = None):
    if not origin:
        origin = referer
    return "%s|referer=%s|origin=%s" % (url, referer, origin)

def add_items(urls, ref_url, PLUGIN):
    no_duplicates = list(dict.fromkeys(urls))
    for i in range(len(no_duplicates)):
        title = "Source %d" % (i + 1)
        li = ListItem(title)
        li.setInfo('video', {'title': title,
                                    'mediatype': 'video'})
        m3u8_url = urllib.parse.quote(urls[i], safe="%/:=&?~#+!$,;'@()*[]")
        addDirectoryItem(PLUGIN.handle, add_headers(m3u8_url, ref_url), li)
    if (len(urls) == 0):
        li = ListItem("No playable sources found")
        addDirectoryItem(PLUGIN.handle, "", li)
    endOfDirectory(PLUGIN.handle)

def parse_url(url):
    return urlparse(url)

def join_url(a, b):
    return urljoin(a, b)

def wstreamto(html):
    eval_f = re.search(r"<script>(eval.*?)</script>", html, re.MULTILINE | re.DOTALL).group(1)
    f = re.search(r"eval\((.*)\)", eval_f, re.MULTILINE | re.DOTALL).group(1)
    p = re.search(r"(\d{10}.*)\|setAttribute", f).group(1).split('|')
    m3u8_url = "%s://%s.%s.%s:%s/%s/%s.%s?s=%s&e=%s" % (
        p[4], p[5], p[6], p[7], p[8], p[2], p[9], p[11], p[-1], p[0]
    )
    return m3u8_url


def dubzalgo(url, nth_iframe=0):
    """
method:
nth iframe
var rSI : string = ""
var tlc : [string]
var mn : int
for each s in tlc:
    b64 = base64.b64decode(s).decode("utf-8")
    str = re.sub('\D', '', b64)
    str_n = int(str)
    str_n -= 61751400
    rSI += chr(str_n)
search_and_format(rSI)
"""
    from .generic_m3u8_searcher import search_and_format
    from helpers import http_get, header_random_agent
    from bs4 import BeautifulSoup 
    import base64

    headers = header_random_agent()
    p_url = parse_url(url)
    html = http_get(url, headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')
    iframe_url = soup.find_all("iframe")[nth_iframe].get("src")
    headers.update({"Referer": url})
    html = http_get(iframe_url, headers=headers)
    text = html.text

    regex = r" = \[(.*)\]"
    rSI = ""
    tlc = re.search(regex, text, re.MULTILINE | re.DOTALL).group(1)
    tlc = re.sub('\s', '', tlc)
    tlc = tlc.split(",")
    tlc = list(map(lambda x: x.strip('"'), tlc))
    mn = re.search(r"\)\) - (\d+)\);", text).group(1).strip()
    mn = int(mn)
    for s in tlc:
        b64 = base64.b64decode(s).decode("utf-8")
        str = re.sub('\D', '', b64)
        if (str):
            str_n = int(str)
            str_n -= mn
            rSI += chr(str_n)

    return search_and_format(rSI)
