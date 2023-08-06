from ...utils import current_year
from .base_query import BaseQuery
from .query_parser import QueryParser

parser = QueryParser()


class Query(BaseQuery):
    def __init__(self):
        super().__init__()

    def get_ticker(self, ticker: str) -> "ticker":
        query = self._ticker(ticker)
        return parser._parse_ticker(query)

    def get_cik(self, ticker: str) -> "cik":
        query = self._cik(ticker)
        return parser._parse_cik(query)

    def get_xtags(self, ticker: str) -> list:
        query = self._xtags(ticker)
        return parser._parse_xtags(query)

    def get_xtag(
        self,
        ticker: str,
        xtag: str,
        form: str,
        start: int = 0,
        end: int = current_year(),
    ) -> "xtag":
        query = self._xtag(ticker, xtag, form, start, end)
        return parser._parse_xtags(query)
