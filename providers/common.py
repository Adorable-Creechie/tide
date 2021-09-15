import hashlib

def league_color(league):
    colors = ["crimson", "orange", "yellow", "lime", "blue", "cyan", "pink", "tomato", "gold", "turquoise", "fuchsia"]
    color_ind = int(hashlib.sha256(league.encode('utf-8')).hexdigest(), 16) % len(colors)
    return colors[color_ind]
