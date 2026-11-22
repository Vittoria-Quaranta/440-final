import numpy as np
from numpy.typing import NDArray

from vc3_codec.header import VC3_HEADER_STRUCT, AudioHeader
from vc3_codec.types_and_constants import LITTLE_ENDIAN_4_BYTE_INT


def write_vc3(destination: str, header: AudioHeader, seeds: NDArray[np.int64], packed: bytes):
    packed_header = header.to_vc3_header()
    packed_seeds = np.asarray(seeds).astype(LITTLE_ENDIAN_4_BYTE_INT).tobytes()
    with open(destination, "wb") as f:
        f.write(packed_header)
        f.write(packed_seeds)
        f.write(packed)

def read_vc3(source: str) -> tuple[AudioHeader, NDArray[np.int64], bytes] | None:
    with open(source, "rb") as f:
        packed_header = f.read(VC3_HEADER_STRUCT.size)
        header = AudioHeader.from_vc3_header(packed_header)
        if header is None:
            print(f"{source} is not a VC3 file")
            return None
        # each seed is 5 4-byte integers
        packed_seeds = f.read(header.n_channels * 5 * 4)
        seeds = np.frombuffer(
            packed_seeds, dtype=LITTLE_ENDIAN_4_BYTE_INT
        ).astype(np.int64).reshape(header.n_channels, 5)
        packed = f.read()
    return header, seeds, packed
