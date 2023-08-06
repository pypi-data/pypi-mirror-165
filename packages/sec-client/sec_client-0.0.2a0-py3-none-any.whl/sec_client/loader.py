from .utils import current_year
from .tables import Query


class Loader(Query):
    def __init__(self, ticker: str, tag: str):
        super().__init__()
        self.ticker = ticker
        self.tag = tag

    def load_fact(self, form, start=0, end=current_year()):
        """
        `fact` returns a pandas dataframe of the specified fact for the specified ticker, for the specified
        time period

        :param form: the form of the financial statement you want to retrieve
        :param start: the start year of the data you want, defaults to 0 (optional)
        :param end: The end date of the data you want
        :return: the value of the function xtag.
        """
        return self.get_xtag(self.ticker, self.tag, form, start, end)

def load_fact(ticker, tag, form, start=0, end=current_year()):
    loader = Loader(ticker, tag)
    return loader.load_fact(form, start, end)