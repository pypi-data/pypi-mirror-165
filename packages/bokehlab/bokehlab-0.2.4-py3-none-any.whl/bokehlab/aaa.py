def parse_style(s, default_line_style, default_marker_style):
#    if not s:
#        return default_
    if s[0] in MARKER_STYLES:
        marker_style = s[0]
        line_style = s[1:]
        if line_style not in LINE_STYLES:
            raise ValueError(f'Unsupported line style: {line_style}')
    elif s[:2] in ('--', '-.'):
        line_style = s[:2]
        marker_style = s[2:]
        if marker_style not in MARKER_STYLES:
            raise ValueError(f'Unsupported marker style: {marker_style}')
    elif s[0] in ':-':
        line_style = s[:1]
        marker_style = s[1:]
        if marker_style not in MARKER_STYLES:
            raise ValueError(f'Unsupported marker style: {marker_style}')
    else:
        raise ValueError(f'Unsupported line style: {style}')
    return line_style, marker_style
