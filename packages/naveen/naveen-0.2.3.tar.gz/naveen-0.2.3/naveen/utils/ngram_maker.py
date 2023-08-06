import argparse
import sys
from typing import List


class NgramMaker(object):

    def __init__(self, n: int = 5) -> None:
        self.n = n

    def get_ngrams_from_whitespace_delimited_text(self,
                                                  text: str) -> List[str]:
        words = text.split()
        out: List[str] = []
        for gm in zip(*[words[i:] for i in range(self.n)]):
            gram = " ".join(gm)
            out.append(gram)
        return out


if __name__ == "__main`__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", help="how many grams",
                        type=int,
                        default=7)
    args = parser.parse_args()
    ngram_maker = NgramMaker(args.n)

    if sys.stdin.isatty():  # no pipe
        print("- You must pipe input to ngrams")
        import os
        os._exit(0)

    for line in sys.stdin:  # for line in pipe
        line = line.replace('\n', '')
        ngrams = ngram_maker.get_ngrams_from_whitespace_delimited_text(line)
        print(ngrams)
        for n in ngrams:
            print(n)
