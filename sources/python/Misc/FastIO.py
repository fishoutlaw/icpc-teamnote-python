"""원본: code/Misc/FastIO.cpp. Signed whitespace-separated integers.
read_ints: O(input bytes) time/memory, fast when input fits in memory.
iter_ints: O(input bytes) time, O(chunk_size) memory, slower Python loop.
write_lines: O(output size) time/memory. No import-time input/output.
"""

import sys


def read_ints(stream=None):
    if stream is None:
        stream = sys.stdin.buffer
    return list(map(int, stream.read().split()))


def iter_ints(stream=None, chunk_size=1 << 16):
    """Input must be valid decimal integers separated by whitespace."""
    if stream is None:
        stream = sys.stdin.buffer
    if chunk_size <= 0:
        raise ValueError('positive chunk size required')
    value, sign, active = 0, 1, False
    while True:
        chunk = stream.read(chunk_size)
        if not chunk:
            break
        for c in chunk:
            if 48 <= c <= 57:
                value = value * 10 + c - 48
                active = True
            elif c == 45:
                sign = -1
            else:
                if active:
                    yield sign * value
                value, sign, active = 0, 1, False
    if active:
        yield sign * value


def write_lines(values, stream=None):
    if stream is None:
        stream = sys.stdout
    stream.write('\n'.join(map(str, values)))
