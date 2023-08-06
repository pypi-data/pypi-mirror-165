from .caller import Caller
from .extractor import extract
from .tables.inserter import Inserter
from .tables.updater import Updater

insert = Inserter()
update = Updater()


class Dumper:
    def __init__(self, ticker, tag, form):
        self.ticker = ticker
        caller = Caller(ticker)
        call = caller.call_fact(tag)
        self.extracted = extract(call, form)

        self.tag = tag

    def dump_fact(self):
        """
        For each value, accession, end, year, quarter, form, and filed in the extracted list, insert the
        value, accession, end, year, quarter, form, and filed into the database
        """
        [
            insert.value(
                self.ticker,
                self.tag,
                value,
                accession,
                end,
                year,
                quarter,
                form,
                filed,
            )
            for value, accession, end, year, quarter, form, filed in self.extracted
        ]

def dump_fact(ticker, tag, form):
    dumper = Dumper(ticker, tag, form)
    dumper.dump_fact()