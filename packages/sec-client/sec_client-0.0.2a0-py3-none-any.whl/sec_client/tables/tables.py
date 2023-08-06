import os

import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

db_path = os.path.abspath("sec_client/tables/DATABASE.db")
engine = db.create_engine(f"sqlite:///{db_path}")


class Ticker(Base):
    __tablename__ = "ticker"
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(7), unique=True)
    company = db.Column(db.VARCHAR(20))
    cik = db.Column(db.Integer())

    xtag = relationship("XBRLTag", back_populates="ticker")

    def __repr__(self) -> str:
        return f"Ticker(ticker={self.ticker}, company={self.company})"


class XBRLTag(Base):
    __tablename__ = "xbrl_tag"
    id = db.Column(db.Integer, primary_key=True)
    xtag = db.Column(db.VARCHAR(20))
    value = db.Column(db.Integer)
    accession = db.Column(db.VARCHAR)
    end = db.Column(db.Date)
    year = db.Column(db.Integer)
    quarter = db.Column(db.SmallInteger)
    form = db.Column(db.VARCHAR)
    filed = db.Column(db.Date)

    ticker_id = db.Column(db.Integer, db.ForeignKey("ticker.id"), nullable=False)

    ticker = relationship("Ticker", back_populates="xtag")
    line_item = relationship(
        "LineItem", back_populates="xtag", cascade="all, delete-orphan"
    )


class LineItem(Base):
    __tablename__ = "line_item"
    id = db.Column(db.Integer, primary_key=True)
    line_item = db.Column(db.String())
    statement = db.Column(db.String(20))

    xbrl_tag_id = db.Column(db.Integer, db.ForeignKey("xbrl_tag.id"), nullable=False)
    xtag = relationship("XBRLTag", back_populates="line_item")


class Statement(Base):
    __tablename__ = "statement"
    id = db.Column(db.Integer, primary_key=True)

    balance_sheet = relationship(
        "BalanceSheet", back_populates="statement", cascade="all, delete-orphan"
    )

    income_statement = relationship(
        "IncomeStatement", back_populates="statement", cascade="all, delete-orphan"
    )

    cash_flow_statement = relationship(
        "CashFlowStatement", back_populates="statement", cascade="all, delete-orphan"
    )


class BalanceSheet(Base):
    __tablename__ = "balance_sheet"
    id = db.Column(db.Integer, primary_key=True)
    statement_id = db.Column(db.Integer, db.ForeignKey("statement.id"))
    statement = relationship("Statement", back_populates="balance_sheet")


class IncomeStatement(Base):
    __tablename__ = "income_statement"
    id = db.Column(db.Integer, primary_key=True)
    statement_id = db.Column(db.Integer, db.ForeignKey("statement.id"))
    statement = relationship("Statement", back_populates="income_statement")


class CashFlowStatement(Base):
    __tablename__ = "cash_flow_statement"
    id = db.Column(db.Integer, primary_key=True)
    statement_id = db.Column(db.Integer, db.ForeignKey("statement.id"))
    statement = relationship("Statement", back_populates="cash_flow_statement")
