#!/usr/bin/env python3


import os
import argparse
import errno


class Words:
    def __init__(self, words):
        self.words = words
        self.words2i = {words[i] : i for i in range(len(words))}


log_enable = False
def log(msg):
    if log_enable:
        print(msg)


def get_words(filename: str) -> tuple:
    with open(filename, "r") as file:
        words = file.read().split('\n')
        return Words(words)
    

def get_encoded(words, seed, key, index):
    now_index = words.words2i[seed.words[index]]
    res_index = (now_index + key) % len(words.words)
    log(f"encode {seed.words[index]}({now_index}) -> {words.words[res_index]}({res_index})")
    return words.words[res_index]


def minus_by_module(num, dec, module):
    num = num % module
    dec = dec % module
    if num - dec < 0:
        return num + module - dec
    return num - dec


def get_decoded(words, seed, key, index):
    now_index = words.words2i[seed.words[index]]
    res_index = minus_by_module(now_index, key, len(words.words))
    log(f"decode {seed.words[index]}({now_index}) -> {words.words[res_index]}({res_index})")
    return words.words[res_index]


def process(words, seed, key, decode):
    out = []
    _key = str(key)

    if len(seed.words) not in (12, 24):
        raise(ValueError(f"Invalid seed phrase length: {len(seed.words)}"))

    for i in range(len(seed.words)):
        word = seed.words[i]

        if words.words2i[word] == None:
            raise ValueError(f"Word '{word}' is not exist standard")
        if decode:
            out.append(get_decoded(words, seed, int(_key[i % len(_key)]) + i, i))
        else:
            out.append(get_encoded(words, seed, int(_key[i % len(_key)]) + i, i))
    
    return out


def seed_encode(args):
    words = get_words(args.words)
    seed = get_words(args.seed)
    return process(words, seed, args.key, False)


def seed_decode(args):
    words = get_words(args.words)
    seed = get_words(args.seed)
    return process(words, seed, args.key, True)


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
                        default = False, action='store_true')
    parser.add_argument('-v', '--verbose',
                        default = False, action='store_true')
    args = parser.parse_args()

    global log_enable
    log_enable = args.verbose

    try:
        out = []

        if args.decode:
            out = seed_decode(args)
        else:
            out = seed_encode(args)
        
        with open(args.output, "w+") as file:
            for i in range(len(out) - 1):
                file.write(out[i] + '\n')
            file.write(out[len(out) - 1])

    except FileNotFoundError as e:
        print(e)
        os._exit(errno.ENODEV)
    except ValueError as e:
        print(e)
        os._exit(errno.EINVAL)
    # except Exception as e:
    #     print(e)
    #     os._exit(1)

if __name__ == "__main__":
    main()


