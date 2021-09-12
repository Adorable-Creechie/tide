if __name__ == "__main__":
    import sys
    import os
    import json
    # ugly hack, but oh well
    sys.path.append("%s/.kodi/addons/plugin.video.tide" % os.getenv("HOME"))


from helpers import log

from . import generic_m3u8_searcher
from . import ovostreamscom
from . import liveonscorenet
from . import liveonscoretv
from . import hdstreamsclub
from . import streamcr7net
from . import techobestcom
from . import hazmowatch
from . import footballstreamto
from . import soccer24hdcom
from . import dubsstreamzcom
from . import oomovienet
from . import papahdlive
from . import _60fpslive
from . import myoplaylive
from . import sportstreampw
from . import b9streamclub
from . import redsoccerinfo
from . import worldstreamsnet
from . import buffstreamlive
from . import streamfoottk
from . import redditstreamsblogspotcom
from . import daddylivelive
from . import fightpasssite
from . import mazymediascom
from . import hhdstreamsclub
from . import hockeynewssite
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
from . import liveonscoreto

# list of sources
all_sources = [
    generic_m3u8_searcher,
    ovostreamscom,
    liveonscorenet,
    liveonscoretv,
    hdstreamsclub,
    streamcr7net,
    techobestcom,
    hazmowatch,
    footballstreamto,
    soccer24hdcom,
    dubsstreamzcom,
    oomovienet,
    papahdlive,
    _60fpslive,
    myoplaylive,
    sportstreampw,
    b9streamclub,
    redsoccerinfo,
    worldstreamsnet,
    buffstreamlive,
    streamfoottk,
    redditstreamsblogspotcom,
    daddylivelive,
    fightpasssite,
    mazymediascom,
    hhdstreamsclub,
    hockeynewssite,
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
    liveonscoreto
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
