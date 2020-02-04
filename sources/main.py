if __name__ == "__main__":
    import sys
    import os
    import json

    # ugly hack, but oh well
    sys.path.append("%s/.kodi/addons/plugin.video.tide" % os.getenv("HOME"))

import generic_m3u8_searcher

# list of sources
all_sources = [
    generic_m3u8_searcher
]

def url_to_source(url, fallback = generic_m3u8_searcher):
    for s in all_sources:
        if s.can_handle(url):
            return s
    return fallback

if __name__ == "__main__":
    # ugly hack, but oh well
    sys.path.append("%s/.kodi/addons/plugin.video.tide" % os.getenv("HOME"))

    def test_60fps_live():
        url = "http://60fps.live/sampdoria-vs-napoli/?link=1&utm_source=soccer100"
        r = url_to_source(url)
        print(r)

    test_60fps_live()
