
from typing import List


class PageMaker(object):

    @staticmethod
    def make_pages(baseurl: str, max_pages: int) -> List[str]:
        output: List[str] = []
        for i in range(1, max_pages + 1):
            output.append(baseurl + str(i))
        return output


if __name__ == "__main__":
    page_maker = PageMaker()
    base: str = "https://allnurses.com/search/?q=EHR&sortby=relevancy&page"
    max_: int = 54
    pages = page_maker.make_pages(base, max_)
