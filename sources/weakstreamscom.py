"""
weakstreams.com

method:
get vidgstream variable
GET HLS_URL
json data {
 "idgstream": UrlID, "serverid": ""
}
where UrlID: vidgstream 
"""

NAME = "weakstreams.com"
KEY = "weakstreamsto"
BASE = "weakstreams.com"
HLS_URL = "http://weakstreams.com/gethls.php"

try:
    from router import PLUGIN, path_for_source
    from helpers import http_get, header_random_agent
    from sources.common import parse_url, gen_can_handle, gen_root
except Exception as e:
    print(e)

import urllib
import re
from bs4 import BeautifulSoup 

can_handle = gen_can_handle(BASE)

@PLUGIN.route("%s/<url>" % path_for_source(KEY))
def root(url):
    gen_root(url, get_urls)

def get_urls(url):
    headers = header_random_agent()
    p_url = parse_url(url)
    html = http_get(url, headers=headers)
    vidgstream = re.search(r'var vidgstream = \"(.*)\"', html.text).group(1)
    params = {
        "idgstream": vidgstream,
        "serverid": "",
    }
    headers.update({"Referer": url, "Origin": url, "Accept-Encoding": "compress"})
    resp = http_get(HLS_URL, params = params, headers = headers)
    json = resp.json()
    rawUrl = json["rawUrl"]
    if rawUrl == 'null':
        return []
    return [rawUrl]

if __name__ == "__main__":
    def test(url):
        vid_urls = get_urls(url)
        print(vid_urls)

    def test_can_handle(url):
        print(can_handle(url))

    test("http://weakstreams.com/soccer-streams/uefa-europa-league/young-boys-vs-manchester-united/35995/")
    test_can_handle("http://weakstreams.com/soccer-streams/uefa-europa-league/young-boys-vs-manchester-united/35995/")
