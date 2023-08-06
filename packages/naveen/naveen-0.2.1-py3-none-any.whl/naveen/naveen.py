import json
import re
import os
import sys
import argparse
import time
from typing import List
from copy import deepcopy
from naveen.data.pipe_cleaner import PipeCleaner
from naveen.data.scrapers.html_extractor import HTMLExtractor
from naveen.data.scrapers.html_tag_stripper import HTMLTagStripper
from bs4 import BeautifulSoup
from naveen.experiment.config.dynamic_experiment_config_maker import DynamicExperimentConfigMaker  # noqa: E501
from naveen.experiment.experiment_group_runner import ExperimentGroupRunner  # type: ignore # noqa: E501
from naveen.experiment.experiment_runner import ExperimentRunner  # type: ignore # noqa: E501


from naveen.utils.ngram_maker import NgramMaker


def pages() -> None:
    '''
    Input is assumed to be a url list

    An exclusion list of urls is required
    '''
    import argparse
    from naveen.data.page_maker import PageMaker

    parser = argparse.ArgumentParser()
    parser.add_argument('-b',
                        '--b',
                        '-base',
                        '--base',
                        '--baseurl',
                        type=str,
                        dest="baseurl",
                        required=True)
    parser.add_argument('-m',
                        '--m',
                        '-max',
                        '--max',
                        '--max_pages',
                        type=int,
                        dest="max_pages",
                        required=True)
    args = parser.parse_args()
    urls: List[str] = PageMaker.make_pages(args.baseurl, args.max_pages)
    for url in urls:
        print(url)


def filter() -> None:
    '''
    Input is assumed to be a url list

    An exclusion list of urls is required
    '''
    import argparse
    import sys
    from typing import Set

    if sys.stdin.isatty():  # no pipe
        print("- You must pipe input to filter")
        import os
        os._exit(0)

    parser = argparse.ArgumentParser()
    parser.add_argument('-e',
                        '--e',
                        '-exclude',
                        '--exclude',
                        type=str,
                        dest="excluded",
                        required=True)
    args = parser.parse_args()

    # assume args.excluded is a text file with urls
    with open(args.excluded, "r") as inf:
        excluded_urls: Set[str] = set(o.replace("\n", "") for o in inf)

    for line in sys.stdin:
        url: str = line  # type: ignore
        url = url.replace("\n", "")
        if url in excluded_urls:
            pass
        else:
            print(url)


def stream() -> None:
    from naveen.data.url_streamer import stream_url
    import sys

    if sys.stdin.isatty():  # no pipe
        print("- You must pipe input to stream")
        import os
        os._exit(0)

    for line in sys.stdin:  # for line in pipe
        line = line.replace('\n', '')
        stream_url(line)


def urls() -> None:
    import sys
    # https://www.geeksforgeeks.org/python-check-url-string/
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"  # noqa: E501

    for line in sys.stdin:
        urls = re.findall(regex, line)
        for url in urls:
            url = url[0].rstrip("\\").strip()
            url = url.replace('\n', '')
            if "," in url:
                url = url.split(",")[0]
            if '"' in url:
                url = url.split('"')[0]
            if url[-1] == "\\":
                url = url[0:-1]
            print(url)


def html2text() -> None:
    '''take raw html and turn it into a string'''

    for line_str in sys.stdin:
        line: dict = json.loads(line_str)
        soup = BeautifulSoup(line["html"], 'lxml')
        line["html"] = soup.text
        print(json.dumps(line))


def remove() -> None:
    import argparse

    import json
    msg = "Strip an html element from the dom"
    parser = argparse.ArgumentParser(msg)

    parser.add_argument("-e", "--e", '-element', "--element",
                        default="div",
                        dest="element", type=str,
                        required=True)

    args = parser.parse_args()

    for line_str in sys.stdin:
        line: dict = json.loads(line_str)
        html = line['html']  # type: ignore
        tag_stripper = HTMLTagStripper(html, args.element)
        line["html"] = tag_stripper.strip()
        print(json.dumps(line))


def pluck() -> None:
    import argparse
    import sys
    import json
    msg = "Pluck html elements with certain properties from a dom"
    parser = argparse.ArgumentParser(msg)
    parser.add_argument("-e", "--e", '-element', "--element",
                        default="div",
                        dest="element", type=str,
                        required=True)
    parser.add_argument("-a", "--a", '-attr', "--attribute",
                        dest="attribute", type=str,
                        default="class", required=True)
    parser.add_argument("-v", "--v", '-value', "--value",
                        dest="value", type=str,
                        default="class_name", required=True)
    args = parser.parse_args()

    for line_str in sys.stdin:
        line: dict = json.loads(line_str)
        assert "html" in line
        assert "url" in line
        extractor: HTMLExtractor = HTMLExtractor(line['html'])  # type: ignore
        messages = extractor.select_by_attr(attr=args.attribute,
                                            html_element=args.element,
                                            attr_value=args.value)
        for i, message in enumerate(messages):
            out: dict = deepcopy(line)
            out['html'] = str(message)
            print(json.dumps(out))


def clean() -> None:
    '''
    # expected use
    # echo "test/fixtures/config/voss" | clean -e ".gz" =>
    # test/fixtures/config/voss.gz does not exist so print filename
    # echo "test/fixtures/config/voss" | clean -e ".json", prints "already exists"  # noqa: E501
    '''
    # returns a file name if the future file name does not yet exist
    parser = argparse.ArgumentParser(description="skip steps in pipe")

    parser.add_argument('-e', '--e', '--extension',
                        dest="extension",
                        default=None,
                        required=True,
                        help="extension; include the dot")
    parser.add_argument('-o', '-output_dir',
                        '--output_dir',
                        dest="output_dir",
                        default=None,
                        required=True,
                        help="output directory")

    parser.add_argument('-v',
                        '--verbose',
                        dest="verbose",
                        default=False,
                        action=argparse.BooleanOptionalAction)  # type: ignore

    args = parser.parse_args()

    pipe_cleaner: PipeCleaner = PipeCleaner(
        args.extension,
        args.output_dir,
        args.verbose)

    if sys.stdin.isatty():  # no pipe
        print("- You must pipe input to this program")
    else:
        for line in sys.stdin:  # for line in pipe
            line = line.replace('\n', '')
            already_exists: bool = pipe_cleaner.already_exists(line)
            if not already_exists:
                sys.stdout.write(line + "\n")
            else:
                # note writes to stderrr
                proposed = pipe_cleaner.get_proposed_filename(line)
                if args.verbose:
                    sys.stderr.write(
                        "[*] Already got {} => {}\n".format(line, proposed))


def ngrams() -> None:
    parser = argparse.ArgumentParser()
    help = "print all n-grams in a file to stdout; assume whitespace delimited"
    parser.add_argument("-n",
                        help=help,
                        type=int,
                        required=True)
    args = parser.parse_args()
    ngram_maker = NgramMaker(args.n)

    if sys.stdin.isatty():  # no pipe
        print("- You must pipe input to ngrams")
        import os
        os._exit(0)

    for line in sys.stdin:  # for line in pipe
        line = line.replace('\n', '')
        ngrams = ngram_maker.get_ngrams_from_whitespace_delimited_text(line)
        for n in ngrams:
            print(n)


def group() -> None:
    parser = argparse.ArgumentParser()
    help = "Run an experiment group from a config file"
    parser.add_argument("-c", "--config",
                        help=help,
                        type=str,
                        dest="config",
                        required=True)
    parser.add_argument("-p", "--package_name",
                        help=help,
                        type=str,
                        dest="package_name",
                        required=True)
    parser.add_argument("-o", "--outputdir",
                        type=str,
                        dest="outputdir",
                        default="results")
    args = parser.parse_args()

    sys.path.append(args.package_name)
    assert args.config.endswith("yaml"), "The group config must be YAML"
    runner = ExperimentGroupRunner(config_path=args.config)
    runner.run(outputdir=args.outputdir,
               package_name=args.package_name)


def experiment() -> None:
    parser = argparse.ArgumentParser()
    help = "Run an experiment from a config file"
    parser.add_argument("-c", "--config",
                        help=help,
                        type=str,
                        dest="config",
                        required=True)
    parser.add_argument("-p", "--package_name",
                        help=help,
                        type=str,
                        dest="package_name",
                        required=True)
    parser.add_argument("-o", "--outputdir",
                        type=str,
                        dest="outputdir",
                        default="results")
    args = parser.parse_args()

    sys.path.append(args.package_name)

    sys.path.append(os.getcwd())

    maker = DynamicExperimentConfigMaker()
    msg = "Your config {} must be json or yaml".format(args.config)
    assert args.config[-4] in ['yaml', 'json', '.yml'], msg
    if args.config[-4:] == "json":
        config = maker.from_json(args.config)
    else:
        config = maker.from_yaml(args.config)
    name = args.outputdir + "/" + config.name + str(int(time.time()))

    runner = ExperimentRunner(config,
                              package_name=args.package_name,
                              output_directory=name)
    runner.run()


if __name__ == "__main__":
    a = 5
    print(a)
