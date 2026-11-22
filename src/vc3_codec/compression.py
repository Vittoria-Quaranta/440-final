import zlib

import numpy as np

from vc3_codec.types_and_constants import (
    LITTLE_ENDIAN_4_BYTE_INT,
    LITTLE_ENDIAN_8_BYTE_INT,
    Int64Array,
)


def compress(data: Int64Array, byte_width: int) -> bytes:
    match byte_width:
        case 1 | 2:
            byte_width_str = LITTLE_ENDIAN_4_BYTE_INT
        case 4:
            byte_width_str = LITTLE_ENDIAN_8_BYTE_INT
        case _:
            raise ValueError(f"bad byte width: {byte_width}")
    raw = data.astype(byte_width_str).tobytes()
    # level 6 is default compression, level 9 is max
    packed = zlib.compress(raw, level=9)
    return packed

def decompress(packed: bytes, byte_width: int) -> Int64Array:
    match byte_width:
        case 1 | 2:
            byte_width_str = LITTLE_ENDIAN_4_BYTE_INT
        case 4:
            byte_width_str = LITTLE_ENDIAN_8_BYTE_INT
        case _:
            raise ValueError(f"bad byte width: {byte_width}")
    raw = zlib.decompress(packed)
    data = np.frombuffer(raw, dtype=byte_width_str).astype(np.int64)
    return data
