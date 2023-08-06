from bs4 import BeautifulSoup
from bs4.element import ResultSet
import json


class HTMLExtractor(object):

    def __init__(self, html_str: str) -> None:
        self.soup = BeautifulSoup(html_str, 'lxml')

    def select_by_attr(self,
                       attr: str = "class",  # type: ignore
                       html_element: str = "div",  # type: ignore
                       attr_value: str = "bbWrapper") -> ResultSet:
        '''
        e.g. to select all divs with data-role attribute equal to comment
        content do  extractor.select_by_class(attr="data-role",
                                             html_element="div",
                                             attr_value="commentContent")

        to select all p w/ class "A" do
                content do  extractor.select_by_class(attr="class",
                                             html_element="p",
                                             attr_value="A")
        '''
        out = self.soup.find_all(html_element, {attr: attr_value})
        return out


if __name__ == "__main__":
    with open("tmp/index.html", "r") as inf:
        html_doc = inf.read()
        extractor = HTMLExtractor(html_doc)
        messages = extractor.select_by_attr(attr="data-role",
                                            html_element="div",
                                            attr_value="commentContent")
        for i, message in enumerate(messages):
            print(json.dumps({"html": str(message), "i": i}))
