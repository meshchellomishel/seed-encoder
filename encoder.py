#!/usr/bin/env python3


import os
import argparse
import errno


class Words:
    def __init__(self, words, words2i):
        self.words = words
        self.words2i = words2i


def get_words(filename: str) -> tuple:
    with open(filename, "r") as file:
        words = file.read().split('\n')
        return Words(words, {words[i] : i for i in range(len(words))})
    

def get_encoded(words, seed, key, index):
    return words.words[(words.words2i[seed.words[index]] + key) % len(words.words)]


def minus_by_module(num, dec, module):
    num = num % module
    dec = dec % module
    if num - dec < 0:
        return num + module - dec
    return num - dec


def get_decoded(words, seed, key, index):
    return words.words[minus_by_module(words.words2i[seed.words[index]], key, len(words.words))]


def process(args, decode):
    words = get_words(args.words)
    seed = get_words(args.seed)
    out = []
    key = str(args.key)

    if len(seed.words) not in (12, 24):
        raise(ValueError(f"Invalid seed phrase length: {len(seed.words)}"))

    for i in range(len(seed.words)):
        word = seed.words[i]

        if not words.words2i[word]:
            raise ValueError(f"Word '{word}' is not exist standard")
        if decode:
            out.append(get_decoded(words, seed, int(key[i % len(key)]) + i, i))
        else:
            out.append(get_encoded(words, seed, int(key[i % len(key)]) + i, i))
    
    with open(args.output, "w+") as file:
        for i in range(len(out) - 1):
            file.write(out[i] + '\n')
        file.write(out[len(out) - 1])


def seed_encode(args):
    process(args, False)


def seed_decode(args):
    process(args, True)


def main():
    parser = argparse.ArgumentParser(
                prog='seed-encoder',
                description='Cesar alghorithm encoder')
    parser.add_argument('-s', '--seed',
                        required=True)
    parser.add_argument('-k', '--key',
                        required=True, type=int)
    parser.add_argument('-w', '--words',
                        default='BIP-39.txt')
    parser.add_argument('-o', '--output',
                        default='output.txt')
    parser.add_argument('-d', '--decode',
                        action='store_true')
    parser.add_argument('-v', '--verbose',
                        default = False, action='store_true')
    args = parser.parse_args()

    try:
        if not args.decode:
            seed_encode(args)
            return
        seed_decode(args)

    except FileNotFoundError as e:
        print(e)
        os._exit(errno.ENODEV)
    except ValueError as e:
        print(e)
        os._exit(errno.EINVAL)
    # except Exception as e:
    #     print(e)
    #     os._exit(1)

main()


