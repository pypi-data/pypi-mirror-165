import datetime as dt
from .tables import *
from sqlalchemy.orm import Session
from .classifiers import classifier


class Inserter:
    def __init__(self):
        pass

    def ticker(self, ticker: str, cik: int, company: str = ""):
        """
        > This function takes in a ticker, cik, and company name and adds it to the database

        :param ticker: The ticker symbol of the company
        :type ticker: str
        :param cik: Central Index Key, a unique identifier for a company
        :type cik: int
        :param company: The name of the company
        :type company: str
        """
        with Session(engine) as session:
            ticker = Ticker(ticker=ticker, company=company, cik=cik)
            session.add(ticker)

            session.commit()

    def value(
        self,
        ticker: str,
        xtag: str,
        value,
        accession: str,
        end: dt.datetime,
        year: int,
        quarter: int,
        form: str,
        filed: dt.datetime,
    ):
        """
        > This function takes in a bunch of arguments and creates a new XBRLTag object, which is then
        appended to the xtag list of the Ticker object

        :param ticker: The ticker of the company
        :type ticker: str
        :param xtag: the XBRL tag
        :type xtag: str
        :param value: the value of the tag
        :param accession: The SEC's unique identifier for the filing
        :type accession: str
        :param end: The end date of the period for which the value is reported
        :type end: dt.datetime
        :param year: int
        :type year: int
        :param quarter: 1, 2, 3, 4
        :type quarter: int
        :param form: the form type, e.g. 10-Q, 10-K, etc
        :type form: str
        :param filed: the date the filing was made
        :type filed: dt.datetime
        """
        line_item, statement = classifier(xtag)
        with Session(engine) as session:
            stmt = db.select(Ticker).where(Ticker.ticker == ticker)
            obj = session.scalars(stmt).one()
            obj.xtag.append(
                XBRLTag(
                    xtag=xtag,
                    value=value,
                    accession=accession,
                    end=end,
                    year=year,
                    quarter=quarter,
                    form=form,
                    filed=filed,
                    line_item=[LineItem(line_item=line_item, statement=statement)],
                )
            )
            session.commit()
