if __name__ == "__main__":
    import sys
    import os
    import json

    # ugly hack, but oh well
    sys.path.append("%s/.kodi/addons/plugin.video.tide" % os.getenv("HOME"))

import generic_m3u8_searcher
import ovostreams
import liveonscorenet
import hdstreamsclub
import streamcr7net
import techobestcom

# list of sources
all_sources = [
    generic_m3u8_searcher,
    ovostreams,
    liveonscorenet,
    hdstreamsclub,
    streamcr7net,
    techobestcom
]

def url_to_source(url, fallback = generic_m3u8_searcher):
    for s in all_sources:
        if s.can_handle(url):
            return s
    return fallback

if __name__ == "__main__":
    def test_techobestcom():
        url = "http://techobest.com/soccer5?utm_source=soccer100"
        r = url_to_source(url)
        print(r)

    test_techobestcom()
