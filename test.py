#!/usr/bin/env python3


import random as rd
import encoder as e


class Empty():
    pass


def main():
    words = e.get_words('BIP-39.txt')
    for key in range(1235):
        seed = []

        for i in range(12):
            seed.append(words.words[rd.randint(0, len(words.words) - 1)])
        
        encoded = e.process(words, e.Words(seed), key, False)
        decoded = e.process(words, e.Words(encoded), key, True)

        for i in range(len(seed)):
            if not decoded[i] == seed[i]:
                raise ValueError(f"Test failed on {seed} -> {encoded} -> {decoded}, key: {key}")

main()


        