'''
A utility for figuring out what can be skipped when piping lists
of file names. The assumption is that each step of the pipe adds
a new extension to the filename and may send the files to an
output directory
'''
import argparse
import sys
import os


class PipeCleaner(object):

    def __init__(self, extension: str,
                 output_dir: str,
                 verbose: bool = False) -> None:
        assert extension != "", (
            "You can't have an empty extension")
        assert output_dir is not None, (
            "You must specify and output dir")
        assert extension[0] == ".", (
            "Extension must start with a dot")
        assert extension != ".", (
            "You must have at least one character in extension")
        assert os.path.isdir(
            output_dir), "Must specify a valid output directory"
        self.extension = extension
        self.output_dir = output_dir
        self.verbose = verbose

    def get_proposed_filename(self, path_to: str) -> str:
        basename = os.path.basename(path_to)
        proposed_name = os.path.join(
            self.output_dir, basename + self.extension)
        if self.verbose:
            print("[*] proposed name {}".format(proposed_name))
        return proposed_name

    def already_exists(self, path_to: str) -> bool:
        proposed_name: str = self.get_proposed_filename(path_to)
        out: bool = os.path.isfile(proposed_name)
        if self.verbose:
            print("[*] proposed name {} exists? {}".format(proposed_name, out))
        return out


if __name__ == "__main__":
    # 'Simple utility that returns a file name if the extension is added
    parser = argparse.ArgumentParser(description="skip steps in pipe")

    parser.add_argument('-e', '--e', '--extension',
                        dest="extension",
                        default=None,
                        help="extension that piped process will add")
    parser.add_argument('-o', '-output_dir',
                        '--output_dir',
                        dest="output_dir",
                        default=None,
                        help="output directory")
    args = parser.parse_args()

    pipe_cleaner: PipeCleaner = PipeCleaner(args.extension, args.output_dir)

    '''
    # expected use
    # alias pipecleaner="python src/data/pipe_cleaner.py"
    # echo "test/fixtures/config/voss" | pipecleaner -e ".gz" =>
    # test/fixtures/config/voss.gz does not exist so print filename
    # echo "test/fixtures/config/voss" | pipecleaner -e ".json", prints "already exists"  # noqa: E501
    '''

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
                sys.stderr.write(
                    "[*] Already got {} => {}\n".format(line, proposed))
