import pandas as pd


class Formatter:
    def __init__(self) -> None:
        pass

    def format_fact(self, fact: tuple, xtag: str):
        value = fact["value"]
        year = fact["year"]
        return pd.Series(value, index=year, name=xtag).drop_duplicates()
