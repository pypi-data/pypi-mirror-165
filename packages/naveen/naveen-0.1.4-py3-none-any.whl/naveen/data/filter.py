'''
Filter out a url piped in
'''
import sys
import json
from typing import Set


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-e',
                        '--e',
                        '-exclude',
                        '--exclude',
                        type=str,
                        dest="excluded",
                        required=True)
    args = parser.parse_args()

    if sys.stdin.isatty():  # no pipe
        print("- You must pipe input to filter")
        import os
        os._exit(0)

    # assume args.excluded is a text file with urls
    with open(args.excluded, "r") as inf:
        excluded_urls: Set[str] = set(o.replace("\n", "") for o in inf)

    for line in sys.stdin:
        line = json.loads(line)
        url: str = line["url"]  # type: ignore
        if url in excluded_urls:
            pass
        else:
            json.dumps(line)
