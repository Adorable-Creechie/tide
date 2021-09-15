# provider info
NAME = "soccerstreamshd [UPPERCASE][B][COLOR pink](soccer)[/COLOR][/B][/UPPERCASE]"
KEY = "soccerstreamshd"

# page info
ROOT_URL = "https://reddit.soccerstreamshd.com/"
EVENT_URL = "https://reddit.soccerstreamshd.com/match/"

if __name__ != "__main__":
    import xbmc
    from xbmcplugin import (
        addDirectoryItem,
        addDirectoryItems,
        endOfDirectory,
    )
    from xbmcgui import (
        ListItem,
    )
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
    table = soup.find(class_="table-streams")
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
    url = match.get("datatype")
    key = url.strip("/").split("/")[-1]
    columns = match.find_all("div")

    home = columns[0]
    home_team = home.getText().strip()
    thumb = home.find("img").get("src")

    score = columns[1]
    home_score = score.find(class_="home-score").getText().strip()
    status = score.find("a").getText().strip()
    away_score = score.find(class_="away-score").getText().strip()
    score = "{} [COLOR red]{}[/COLOR] {}".format(home_score, status, away_score)

    away = columns[2]
    away_team = away.getText().strip()

    return {
        "name": "{} {} {}".format(home_team, score, away_team),
        "thumb": thumb,
        "url": url,
        "key": key
    }

def get_all_events():
    html = http_get(ROOT_URL)
    soup = BeautifulSoup(html.text, "html.parser")
    container = soup.find(class_="timeline-left")
    els = container.find_all("div")

    all = []
    league = None
    match = {}
    for el in els:
        classes = el.get("class")
        is_league = "timeline-breaker" in classes
        is_details = "timeline-item" in classes
        is_time = "timeline-start-time" in classes

        if is_league:
            league = el.getText().strip()
        elif is_details:
            match = parse_match(el)
        elif is_time:
            time = el.getText().strip()
            match["name"] += " [{}]".format(time)
            match["league"] = league
            all.append(match)

    return all

if __name__ == "__main__":
    def test_get_all_events():
        r = get_all_events()
        print(r)

    def test_get_all_sources():
        r = get_all_sources("9757737")
        print(json.dumps(r))

    test_get_all_events()
