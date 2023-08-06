from functools import lru_cache

from sqlalchemy.orm import Session

from ..tables import *
from ...utils import current_year


class BaseQuery:
    def __init__(self):
        pass

    @lru_cache(maxsize=5)
    def _ticker(self, ticker: str) -> "ticker":
        """
        > The function `ticker` takes a string `ticker` and returns the first row of the `Ticker` table
        where the `ticker` column is equal to the `ticker` argument

        :param ticker: The ticker symbol of the stock you want to get data for
        :type ticker: str
        :return: The first row of the Ticker table that matches the ticker argument.
        """
        with Session(engine) as session:
            stmt = db.select(Ticker).where(Ticker.ticker == ticker)
            return session.scalars(stmt).one()

    def _cik(self, ticker: str) -> "cik":
        """
        > `cik` returns the CIK of a company given its ticker

        :param ticker: The ticker symbol of the company you want to get the CIK for
        :type ticker: str
        :return: The cik of the ticker
        """
        return self._ticker(ticker)

    def _xtags(self, ticker: str) -> list:
        """
        > Given a ticker, return the list of tags associated with that ticker

        :param ticker: The ticker symbol of the stock you want to get the data for
        :type ticker: str
        :return: A list of strings.
        """
        with Session(engine) as session:
            stmt = db.select(XBRLTag).join(Ticker).where(Ticker.ticker == ticker)
            return session.scalars(stmt).all()

    def _xtag(
        self, ticker: str, xtag: str, form, start=0, end=current_year()
    ) -> "xtag":
        """
        > Get all the values of a given XBRL tag for a given ticker, form, and time period

        :param ticker: the ticker symbol of the company you want to get data for
        :type ticker: str
        :param xtag: the tag you want to get
        :type xtag: str
        :param form: the form type, e.g. 10-K, 10-Q, etc
        :param start: the start year of the data you want to retrieve, defaults to 0 (optional)
        :param end: The year to end the query on
        :return: A list of tuples.
        """
        with Session(engine) as session:
            stmt = (
                db.select(XBRLTag)
                .join(Ticker)
                .where(Ticker.ticker == ticker)
                .where(XBRLTag.form == form)
                .where(XBRLTag.xtag == xtag)
                .where(XBRLTag.year >= start)
                .where(XBRLTag.year <= end)
                .order_by(db.asc(XBRLTag.year))
            )
            return session.scalars(stmt).all()
