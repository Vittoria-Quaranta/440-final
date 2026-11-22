import struct

# define the VC3 file header
# - `<` means little-endian
# - `4s` is a 4-byte string (the type signature)
# - `I` is an unsigned 4-byte int
# - `H` is an unsigned 2-byte int
# thus the final header size is 16 bytes
VC3_HEADER_STRUCT = struct.Struct("<4sIHHI")
# the 4-byte type signature at the start of the file header
VC3_TYPE_SIGNATURE = b"VC3\0"

class AudioHeader:
    def __init__(self, samp_rate, samp_width, n_channels, n_frames):
        self.samp_rate = samp_rate
        self.samp_width = samp_width
        self.n_channels = n_channels
        self.n_frames = n_frames

    def to_vc3_header(self) -> bytes:
        return VC3_HEADER_STRUCT.pack(
            VC3_TYPE_SIGNATURE,
            self.samp_rate,
            self.samp_width,
            self.n_channels,
            self.n_frames,
        )

    @staticmethod
    def from_vc3_header(packed: bytes) -> AudioHeader | None:
        type_sig, samp_rate, samp_width, n_channels, n_frames = VC3_HEADER_STRUCT.unpack(packed)
        if type_sig != VC3_TYPE_SIGNATURE:
            # not a VC3 file
            return None
        return AudioHeader(samp_rate, samp_width, n_channels, n_frames)
