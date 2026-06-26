from rich.color import Color


def blend_colors(*colors: Color) -> Color:
    if not colors:
        return Color.from_rgb(0, 0, 0)
    if len(colors) == 1:
        return colors[0]
    r = sum(c.triplet.red if c.triplet else 0 for c in colors) // len(colors)
    g = sum(c.triplet.green if c.triplet else 0 for c in colors) // len(colors)
    b = sum(c.triplet.blue if c.triplet else 0 for c in colors) // len(colors)
    return Color.from_rgb(int(r), int(g), int(b))
