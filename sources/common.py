import urllib
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
    for i in range(len(urls)):
        title = "Source %d" % i
        li = ListItem(title)
        li.setInfo('video', {'title': title,
                                    'mediatype': 'video'})
        m3u8_url = urllib.quote(urls[i], safe="%/:=&?~#+!$,;'@()*[]")
        addDirectoryItem(PLUGIN.handle, add_headers(m3u8_url, ref_url), li)
    if (len(urls) == 0):
        li = ListItem("No playable sources found")
        addDirectoryItem(PLUGIN.handle, "", li)
    endOfDirectory(PLUGIN.handle)

def parse_url(url):
    return urlparse(url)

def join_url(a, b):
    return urljoin(a, b)
