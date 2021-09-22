# provider info
NAME = "streams100 [UPPERCASE][B][COLOR pink](soccer)[/COLOR][/B][/UPPERCASE]"
KEY = "streams100"

# page info
ROOT_URL = "https://soccerstreams-100.tv"

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
    key = key.replace(",", "/")
    def itemMaker(source, fn):
        li = ListItem("[%s] [B]%s[/B] (%s)" % (
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
    url = "%s%s/" % (ROOT_URL, key)
    html = http_get(url, headers = headers)
    soup = BeautifulSoup(html.text, 'html.parser')
    rows = soup.find_all(class_="MuiTableRow-root jss21 MuiTableRow-hover")

    all = []
    for r in rows:
        url = r.get("href")
        columns = list(r.children)

        streamer = columns[0].getText().strip()
        channel = columns[2].getText().strip()
        lang = columns[4].getText().strip()

        all.append({
            "streamer": streamer,
            "channel": channel,
            "lang": lang,
            "url": url
        })
    return all

def parse_match(match, league_name):
    url = match.get("href")
    key = url.replace("/", ",")

    divs = list(next(match.children).children)

    home = divs[0]
    home_team = home.find("p").getText().strip()
    thumb = home.find("img").get("src").replace("?w=32&h=32", "")

    away = divs[2]
    away_team = away.find("p").getText().strip()

    score = divs[1].getText().strip()

    return {
        "url": url,
        "key": key,
        "name": "{} [COLOR red]{}[/COLOR] {}".format(home_team, score, away_team),
        "league": league_name,
        "thumb": thumb
    }

def get_all_events():
    html = http_get(ROOT_URL)
    soup = BeautifulSoup(html.text, 'html.parser')
    leagues = soup.find_all(class_="MuiPaper-root MuiAccordion-root jss16 Mui-expanded MuiAccordion-rounded MuiPaper-elevation1 MuiPaper-rounded")
    all = []
    for l in leagues:
        league_name = l.find(class_="MuiTypography-root MuiCardHeader-title MuiTypography-body2 MuiTypography-displayBlock").getText().strip()
        matches = l.find_all(class_="MuiButtonBase-root MuiListItem-root jss18 MuiListItem-gutters MuiListItem-button")
        for match in matches:
            all.append(parse_match(match, league_name))
    return all

def get_all_events_fake():
    return [{
            "name": "Sampdoria vs Napoli",
            "category": "Serie A",
            "date": "February 3, 2020 ",
            "thumb": "https://www.sofascore.com/images/team-logo/football_2675.png",
            "url": "https://streams100.net/event/sampdoria-vs-napoli-match-preview/",
            "key": "sampdoria-vs-napoli-match-preview"
    }]

if __name__ == "__main__":
    def test_get_all_events():
        r = get_all_events()
        print(r)

    def test_get_all_sources():
        r = get_all_sources("/game/fra-1/609466")
        print(r)

    test_get_all_sources()
