NAME = "[COLOR orange]generic[/COLOR]"
KEY = "genericm3u8searcher"

try:
    from router import PLUGIN, path_for_source
    from helpers import http_get, header_random_agent
    from sources.common import add_items, parse_url
except Exception as e:
    print(e)

import urllib
import base64
import re
from bs4 import BeautifulSoup 

def can_handle(url):
    return False

@PLUGIN.route("%s/<url>" % path_for_source(KEY))
def root(url):
    ref_url = urllib.parse.unquote(url)
    urls = get_urls(ref_url)
    add_items(urls, ref_url, PLUGIN)

def get_urls(url, referer = ''):
    headers = header_random_agent()
    if referer != '':
        headers.update({"Referer": referer})
    parsed_url = parse_url(url)
    html = http_get(url, headers=headers)
    return search_and_format(html.text)

def nested_iframe_n_get_urls(url, nested_level = 1, nth_iframe = 0):
    headers = header_random_agent()
    cookies = {}
    p_url = parse_url(url)
    html = http_get(url, headers=headers)
    cookies.update(html.cookies)
    soup = BeautifulSoup(html.text, 'html.parser')
    iframe_url = soup.find_all("iframe")[nth_iframe].get("src")
    if nested_level == 0:
        return get_urls(iframe_url, url)
    else:
        return nested_iframe_n_get_urls(iframe_url, nested_level - 1, nth_iframe)

def nested_iframe_2_get_urls(url, nth_iframe = 0):
    return nested_iframe_n_get_urls(url, 1, nth_iframe)

def nth_iframe_get_urls(url, nth_iframe = 0):
    headers = header_random_agent()
    cookies = {}
    p_url = parse_url(url)
    html = http_get(url, headers=headers)
    cookies.update(html.cookies)
    soup = BeautifulSoup(html.text, 'html.parser')
    iframe_url = soup.find_all("iframe")[nth_iframe].get("src")
    return get_urls(iframe_url)

def first_iframe_get_urls(url):
    return nth_iframe_get_urls(url, 0)

def snd_iframe_get_urls(url):
    return nth_iframe_get_urls(url, 1)

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

if __name__ == "__main__":
    def test(url):
        vid_urls = get_urls(url)
        print(vid_urls)

    test("https://videojs.github.io/videojs-contrib-hls/")
