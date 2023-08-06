import re


class HTMLTagStripper(object):
    '''
    removes elements with a given tag from html string
    See below
    '''

    def __init__(self, html_str: str, tag_to_strip: str):
        self.html_str = html_str
        self.tag_to_strip = tag_to_strip

    def strip(self) -> str:
        '''
        Sample input:
        <p>I\'m in the same spot as you. <abbr title="Licensed Practice Nurse">LPN</abbr>, needing to work from home </p> # noqa: E501
        Sample output:
        <p>I\'m in the same spot as you, needing to work from home </p>
        '''
        regex = "<{}(.|\n)*?</{}>".format(self.tag_to_strip,
                                          self.tag_to_strip)
        return re.sub(regex, "", str(self.html_str))


if __name__ == "__main__":

    with open("test/fixtures/blockquote.html", "r") as inf:
        html = inf.read()

    tag_stripper = HTMLTagStripper(html, "blockquote")

    print(tag_stripper.strip())
