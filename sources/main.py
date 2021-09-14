from helpers import log

from . import generic_m3u8_searcher
from . import ovostreamscom
from . import liveonscorenet
from . import liveonscoretv
from . import hdstreamsclub
from . import techobestcom
from . import hazmowatch
from . import footballstreamto
from . import soccer24hdcom
from . import dubsstreamzcom
from . import papahdlive
from . import myoplaylive
from . import b9streamclub
from . import redsoccerinfo
from . import worldstreamsnet
from . import buffstreamlive
from . import streamfoottk
from . import redditstreamsblogspotcom
from . import hhdstreamsclub
from . import buffstream1com
from . import mazystreamsxyz
from . import alexsportslive
from . import streamsportpro
from . import allsportsmedialive
from . import streamspasscom
from . import nflgamezonecom
from . import techoreelscom
from . import sportnewsto
from . import dubzstreamscom
from . import sportingliveco
from . import bdnewszhcom
from . import daddyliveme
from . import hockeywebsite
from . import thecyclingentertainmentcom
from . import nflscoopnet
from . import uhdstreamsclub
from . import weakstreamscom
from . import myoplayclub
from . import givemenbastreamscom
from . import blacktiesportsnet

# list of sources
all_sources = [
    generic_m3u8_searcher,
    ovostreamscom,
    liveonscorenet,
    liveonscoretv,
    hdstreamsclub,
    techobestcom,
    hazmowatch,
    footballstreamto,
    soccer24hdcom,
    dubsstreamzcom,
    papahdlive,
    myoplaylive,
    b9streamclub,
    redsoccerinfo,
    worldstreamsnet,
    buffstreamlive,
    streamfoottk,
    redditstreamsblogspotcom,
    hhdstreamsclub,
    buffstream1com,
    mazystreamsxyz,
    alexsportslive,
    streamsportpro,
    allsportsmedialive,
    streamspasscom,
    nflgamezonecom,
    techoreelscom,
    sportnewsto,
    dubzstreamscom,
    sportingliveco,
    bdnewszhcom,
    daddyliveme,
    hockeywebsite,
    thecyclingentertainmentcom,
    nflscoopnet,
    uhdstreamsclub,
    weakstreamscom,
    myoplayclub,
    givemenbastreamscom,
    blacktiesportsnet,
]

def url_to_source(url, fallback = generic_m3u8_searcher):
    for s in all_sources:
        if s.can_handle(url):
            return s
    return fallback

if __name__ == "__main__":
    def test():
        url = "http://www.sportstream.pw/football6/index.html"
        r = url_to_source(url)
        print(r)

    test()
