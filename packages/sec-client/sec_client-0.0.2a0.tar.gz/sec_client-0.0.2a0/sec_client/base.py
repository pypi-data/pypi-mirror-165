from sec_edgar_api import EdgarClient
from fake_useragent import UserAgent
from .tables import Query
from functools import lru_cache

query = Query()


class BaseClient:
    def __init__(self, ticker):
        ua = UserAgent()
        edgar = EdgarClient(ua.ie)

        cik = query.get_cik(ticker)
        self.ticker = ticker
        self._enter = edgar.get_company_facts(cik)

    @lru_cache(maxsize=5)
    def _base_call(self, taxonomy) -> dict:
        """
        > The function `_base_call` is a private function that returns the facts for a given taxonomy

        :param taxonomy: The taxonomy you want to get the facts for
        :return: A dictionary of the facts for the taxonomy.
        """
        return self._enter["facts"][taxonomy]

    @lru_cache(maxsize=5)
    def _call_gaap(self) -> dict:
        """
        It calls the API and returns the data as a dictionary
        :return: A dictionary of the data from the API call.
        """
        return self._base_call("us-gaap")

    @lru_cache(maxsize=5)
    def _call_dei(self) -> dict:
        """
        It calls the API and returns the data as a dictionary
        :return: A dictionary of the data from the API call.
        """
        return self._base_call("dei")
