from functools import reduce
from itertools import takewhile, zip_longest

from .constants import POSSIBLE_NOTES


def encode_lz77(string: str, window_size=100):
    encoded = string[: window_size + 1]
    i = window_size
    while i < len(string) - window_size:
        input_buffer = string[i: i + window_size + 1]
        window = string[i - window_size: i + window_size + 1]

        substring = max([reduce(lambda x, y: x + y,
                                map(lambda x: x[0],
                                    takewhile(lambda x: x[0] == x[1],
                                              zip_longest(string[i + j: i + window_size], input_buffer)
                                              )
                                    ),
                                '') for j in range(-window_size, 0)], key=len)

        if substring == '':
            i += 1
            encoded += f'0,0${string[i]}'
        else:
            i += len(substring)
            offset = window.find(substring)
            encoded += f'{str(offset)},{str(len(substring))}${string[i]}'

    return encoded


def encode_lz78(string: list):
    codes = dict()
    substring = ''
    index = 0
    encoded = ''

    for c in string:
        substring += c

        if substring not in codes:
            codes[substring] = index
            encoded += f'0,{c}' if substring == c else f'{str(codes[substring[:-1]])},{c}'
            index += 1
            substring = ''

    return encoded


def encode_lzw(string: list):
    codes = {c: i for i, c in enumerate(POSSIBLE_NOTES)}
    index = 4
    encoded = f'{codes[string[0]]},{codes[string[1]]},'
    substring = ''

    for c in string:
        substring += c

        if substring not in codes:
            index += 1
            codes[substring] = index
            encoded += str(codes[substring]) + ','
            substring = ''

    return encoded[:-1]
