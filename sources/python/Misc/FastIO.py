# 공백으로 구분한 정수 입출력. 전체 읽기는 빠르고, 분할 읽기는 메모리를 절약한다.

import sys


def read_ints(stream=None):
    if stream is None:
        stream = sys.stdin.buffer
    return list(map(int, stream.read().split()))


def iter_ints(stream=None, chunk_size=1 << 16):
    # 입력은 공백으로 구분한 올바른 십진 정수여야 한다.
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
