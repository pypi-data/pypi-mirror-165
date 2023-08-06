'''
Stream a url piped in
'''
import sys
import json
import subprocess
from naveen.logger import get_logger


def stream_url(url: str, timeout: int = 3) -> None:
    '''time out unit is seconds, not ms!'''

    out = subprocess.run(["wget", url, "-q",
                          "--timeout={}".format(str(timeout)),
                          "-O", "-"],
                         capture_output=True)
    # returns std out as a unicode string, "return code is wget return code"
    # https://www.gnu.org/software/wget/manual/html_node/Exit-Status.html
    # exit code 0 means no problem
    logger = get_logger()
    try:
        print(json.dumps({"url": url,
                          "returncode": out.returncode,
                          "html": out.stdout.decode("utf-8")}))
    except UnicodeDecodeError:
        logger.error(
            "[*] Error, could not decode {} and so skipping it".format(url))


if __name__ == "__main__":

    url = sys.argv[1]
    url = url.replace('\n', '')
    stream_url(url)
