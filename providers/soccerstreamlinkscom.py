# provider info
NAME = "soccerstreamlinks [UPPERCASE][B][COLOR pink](soccer)[/COLOR][/B][/UPPERCASE]"
KEY = "soccerstreamlinks"

# page info
ROOT_URL = "https://redditz.soccerstreamlinks.com/sports/football/0"
EVENT_URL = "https://redditz.soccerstreamlinks.com/detail-match/"

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

from router import PLUGIN, path_for_provider
from providers.common import league_color
from helpers import http_get, header_random_agent
from sources import url_to_source

import urllib
from bs4 import BeautifulSoup

@PLUGIN.route(path_for_provider(KEY))
def root():
    def itemMaker(event):
        li = ListItem("[B][COLOR %s]%s[/COLOR][/B] | %s" % (
            league_color(event.get("league", "")),
            event.get("league", ""),
            event.get("name", ""),
        ))
        li.setArt({'thumb': event.get("thumb", None),
                'fanart': event.get("fanart", None)})
        return li
    events = get_all_events()
    items = list(map(lambda e: (PLUGIN.url_for(event, key=e["key"]), itemMaker(e), True), events))
    addDirectoryItems(PLUGIN.handle, items)
    endOfDirectory(PLUGIN.handle)

@PLUGIN.route("%s/events/<key>" % path_for_provider(KEY))
def event(key):
    def itemMaker(source, fn):
        li = ListItem("[%s][%s] [B]%s[/B] (%s)" % (
            source.get("quality", "XY"),
            source.get("lang", "Xyz"),
            source.get("channel", "UNKNOWN"),
            fn.NAME,
        ))
        return li
    sources = get_all_sources(key)
    sources_dec = []
    for s in sources:
        source_fn = url_to_source(s["url"])
        sources_dec.append({"el": s, "fn": source_fn})
    items = list(map(lambda s: (PLUGIN.url_for(s["fn"].root,
                                            url=urllib.parse.quote(s["el"]["url"].encode('utf8'), safe='')),
                                itemMaker(s["el"], s["fn"]), True), sources_dec))
    if (len(sources) == 0):
        li = ListItem("No playable sources found")
        addDirectoryItem(PLUGIN.handle, "", li)
    addDirectoryItems(PLUGIN.handle, items)
    endOfDirectory(PLUGIN.handle)

def get_all_sources(key):
    headers = header_random_agent()
    headers.update({"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"})
    url = "%s%s/" % (EVENT_URL, key)
    html = http_get(url, headers = headers)
    soup = BeautifulSoup(html.text, 'html.parser')
    table = soup.find(id="package-live-stream")
    table_body = table.find("tbody")
    rows = table_body.find_all("tr")
    all = []
    for r in rows:
        try:
            streamer_info = r.find("th")
            url = streamer_info.find("a").get("href")
            streamer_name = streamer_info.find(class_="media-body").getText().strip(),

            columns = r.find_all("td")
            quality = columns[4].getText().strip()
            channel_name = columns[0].getText().strip()
            lang = columns[1].getText().strip()
            all.append({
                "streamer": streamer_name,
                "quality": quality,
                "channel": channel_name,
                "lang": lang,
                "url": url
            })
        except:
            pass
    return all

def parse_match(match):
    columns = match.find_all("td")

    home_and_score = columns[0]
    url = home_and_score.find("a").get("href")
    key = url.strip("/").split("/")[-1]
    home_team = home_and_score.find("a").find("span").getText().strip()
    thumb = home_and_score.find("img").get("src")
    score = home_and_score.find(class_="record").getText().strip()

    away = columns[1]
    away_team = away.find("a").find("span").getText().strip()

    time = columns[2]
    time = time.getText().strip()

    location = columns[3]
    location = location.getText().strip()

    return {
        "name": "{} {} {} [{}] ({})".format(home_team, score, away_team, time, location),
        "thumb": thumb,
        "url": url,
        "key": key
    }

def get_all_events():
    html = http_get(ROOT_URL)
    soup = BeautifulSoup(html.text, "html.parser")
    schedules = soup.find_all(class_="responsive-table-wrap")
    captions = soup.find_all(class_="table-caption")
    all = []
    for (caption, schedule) in zip(captions, schedules):
        league = caption.getText().strip()
        table_body = schedule.find("tbody")
        matches = table_body.find_all("tr")
        for match in matches:
            parsed_match = parse_match(match)
            parsed_match["league"] = league
            all.append(parsed_match)
    return all

if __name__ == "__main__":
    def test_get_all_events():
        r = get_all_events()
        print(r)

    def test_get_all_sources():
        r = get_all_sources("9576168")
        print(json.dumps(r))

    test_get_all_sources()
