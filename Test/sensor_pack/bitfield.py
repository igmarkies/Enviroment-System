import micropython


@micropython.native
def _bitmask(start: int, stop: int) -> int:
    """returns a bit mask based on the bits.
    start - number of the least significant bit of the mask (0..31).
    stop - the high bit number of the mask (0..31)."""
    res = 0
    for i in range(start, 1 + stop):
        res |= 1 << i
    return res


def check(start: int, stop: int):
    if start > stop:
        raise ValueError(f"Invalid start: {start}, stop value: {stop}")


class BitField:
    """Class for convenient work with a bit field."""

    def __init__(self, start: int, stop: int, alias: [str, None]):
        """alias - alias (for convenience, for example "work_mode3:0")
        start - number of the least significant bit from which the bit field starts.
        start - the high bit number where the bit field ends
        """
        check(start, stop)
        self.alias = alias
        self.start = start
        self.stop = stop
        self.bitmask = _bitmask(start, stop)

    def put(self, source: int, value: int) -> int:
        """Writes value to source's bit range"""
        src = source & ~self.bitmask
        src |= (value << self.start) & self.bitmask
        return src

    def get(self, source: int) -> int:
        """Returns a value in the bit range of source"""
        return (source & self.bitmask) >> self.start 


@micropython.native
def put(start: int, stop: int, source: int, value: int) -> int:
    """Writes value to source's bit range"""
    check(start, stop)
    bitmask = _bitmask(start, stop)
    src = source & bitmask
    src |= (value << start) & bitmask
    return src
