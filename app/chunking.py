import re

MAX_CHUNK_CHARS = 300
BULLET_PREFIX = re.compile(r'^[\s\-–•*·▪●◦]+')


def _pack(pieces, max_chars):
    packed = []
    current = ""

    for piece in pieces:
        if current and len(current) + 1 + len(piece) > max_chars:
            packed.append(current)
            current = piece
        else:
            current = f"{current} {piece}" if current else piece

    if current:
        packed.append(current)

    return packed


def _split_long_line(line, max_chars):
    sentences = re.split(r'(?<=[.!?])\s+', line)
    result = []

    for piece in _pack(sentences, max_chars):
        if len(piece) > max_chars:
            result.extend(_pack(piece.split(), max_chars))
        else:
            result.append(piece)

    return result


def split_into_chunks(text, max_chars=MAX_CHUNK_CHARS):
    units = []

    for line in re.split(r'\n+', text):
        line = BULLET_PREFIX.sub('', line).strip()
        if not line:
            continue

        if len(line) > max_chars:
            units.extend(_split_long_line(line, max_chars))
        else:
            units.append(line)

    return _pack(units, max_chars)