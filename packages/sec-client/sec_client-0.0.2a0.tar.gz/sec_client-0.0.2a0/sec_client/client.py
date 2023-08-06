from .utils import current_year
from .dumper import dump_fact
from .loader import load_fact
from .formatter import Formatter

formatter = Formatter()


class SecClient:
    def __init__(self):
        pass

    def get_fact(
        self,
        ticker: str,
        tag: str,
        form: str = '10-K',
        start: int = 0,
        end: int = current_year(),
    ):
        """
        `def call_fact(self, ticker: str, tag: str, form: str, start: int = 0, end: int = current_year()):`

        The function takes in a ticker, a tag, a form, a start year, and an end year. The function then
        tries to load the fact from the database. If it fails, it dumps the fact into the database. If it
        succeeds, it formats the fact and returns it

        :param ticker: the stock ticker
        :type ticker: str
        :param tag: the name of the fact you want to get
        :type tag: str
        :param form: the form of the fact, e.g. 10-K, 10-Q
        :type form: str
        :param start: int = 0, end: int = current_year(), defaults to 0
        :type start: int (optional)
        :param end: int = current_year()
        :type end: int
        :return: A dictionary of the form {'ticker': ticker, 'tag': tag, 'form': form, 'start': start,
        'end': end, 'data': data}
        """
        try:
            fact = load_fact(ticker, tag, form, start, end)
        except ValueError:
            dump_fact(ticker, tag, form)
            return self.get_fact(ticker, tag, start, end)

        if isinstance(fact, dict):
            return formatter.format_fact(fact, tag)
