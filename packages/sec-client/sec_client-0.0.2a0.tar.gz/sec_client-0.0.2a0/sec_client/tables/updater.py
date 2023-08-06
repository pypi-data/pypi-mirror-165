from .tables import *
from sqlalchemy.orm import Session
from .query import Query

query = Query()

class Updater:
    def __init__(self):
        pass

    def ticker(self, ticker: str, cik: int):
        """
        > This function takes a ticker and a cik and updates the cik in the database for the given ticker

        :param ticker: the ticker symbol of the company
        :type ticker: str
        :param cik: Central Index Key
        :type cik: int
        """
        with Session(engine) as session:
            query = session.query(Ticker).where(Ticker.ticker == ticker).first()
            query.cik = cik
            session.add(query)
            session.commit()

    def tags(self, ticker: str, tags: list):
        """
        > Add a list of tags to a ticker

        :param ticker: The ticker of the company you want to add tags to
        :type ticker: str
        :param tags: list of strings
        :type tags: list
        """
        query = Query.ticker(ticker)
        with Session(engine) as session:
            query.xtag.extend(tags)
            session.commit()

    def statement(self, xtag: str, _statement: str):
        """
        It takes an XBRL tag and a statement name, and updates the statement name for all line items with
        that XBRL tag

        :param xtag: The XBRL tag of the line item
        :type xtag: str
        :param _statement: The statement that the line item belongs to
        :type _statement: str
        """
        # sourcery skip: class-extract-method
        with Session(engine) as session:
            stmt = db.select(LineItem).join(XBRLTag).where(XBRLTag.xtag == xtag)
            obj = session.scalars(stmt).all()

            for _ in obj:
                _.statement = _statement

            session.commit()

    def line_item(self, xtag: str, _line_item: str):
        """
        > This function takes in an XBRL tag and a line item and updates the line item of the XBRL tag in
        the database

        :param xtag: the XBRL tag
        :type xtag: str
        :param _line_item: The line item you want to change
        :type _line_item: str
        """
        with Session(engine) as session:
            stmt = db.select(LineItem).join(XBRLTag).where(XBRLTag.xtag == xtag)
            obj = session.scalars(stmt).all()

            for _ in obj:
                _.line_item = _line_item

            session.commit()
