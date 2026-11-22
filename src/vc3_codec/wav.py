import wave

import numpy as np
from numpy.typing import NDArray

from vc3_codec.header import AudioHeader
from vc3_codec.types_and_constants import (
    LITTLE_ENDIAN_2_BYTE_INT,
    LITTLE_ENDIAN_4_BYTE_INT,
)


def write_wav(destination: str, header: AudioHeader, audios: NDArray[np.int64]):
    # interleave multiple channels
    audios = audios.ravel()
    match header.samp_width:
        case 1:
            data = (audios + 128).astype(np.uint8)
        case 2:
            data = audios.astype(LITTLE_ENDIAN_2_BYTE_INT)
        case 4:
            data = audios.astype(LITTLE_ENDIAN_4_BYTE_INT)
        case _:
            raise ValueError(f"bad sample width: {header.samp_width}")
    with wave.open(destination, "wb") as w:
        w.setnchannels(header.n_channels)
        w.setsampwidth(header.samp_width)
        w.setframerate(header.samp_rate)
        w.writeframes(data.tobytes())

def read_wav(source: str) -> tuple[AudioHeader, NDArray[np.int64]]:
    with wave.open(source, "rb") as w:
        samp_rate = w.getframerate()
        samp_width = w.getsampwidth()
        n_channels = w.getnchannels()
        n_frames = w.getnframes()
        raw = w.readframes(n_frames)
    match samp_width:
        case 1:
            audios = np.frombuffer(raw, dtype=np.uint8).astype(np.int64) - 128
        case 2:
            audios = np.frombuffer(raw, dtype=LITTLE_ENDIAN_2_BYTE_INT).astype(np.int64)
        case 4:
            audios = np.frombuffer(raw, dtype=LITTLE_ENDIAN_4_BYTE_INT).astype(np.int64)
        case _:
            raise ValueError(f"bad sample width: {samp_width}")
    header = AudioHeader(samp_rate, samp_width, n_channels, n_frames)
    # un-interleave multiple channels
    audios = audios.reshape(-1, n_channels)
    return header, audios
