from .utils import _value_handlers, nodupes
from .utils._extractor_utils import _replace_string_in_period, _make_into_date


class Extractor:
    def __init__(self, call) -> None:
        self.call = call

    def _extract(self, key, entries, no_duplicates=True):
        """
        It takes a list of dictionaries, and returns a list of values for a given key

        :param key: the key to extract from the dictionary
        :param entries: a list of dictionaries
        :param no_duplicates: If True, the extracted values will be unique, defaults to True (optional)
        :return: A list of all the values for the key 'name' in the entries list.
        """
        extracted = [entry[key] for entry in entries]
        if no_duplicates:
            extracted = nodupes(extracted)

        return extracted

    def _extract_values(self, entries):
        """
        It takes a list of dictionaries and returns a list of the values of the key "val" in each dictionary

        :param entries: a list of dictionaries, each of which contains the following keys:
        :return: A list of values from the entries.
        """
        return self._extract("val", entries)

    def _extract_accession_nums(self, entries):
        """
        It takes a list of entries, and returns a list of accession numbers

        :param entries: a list of dictionaries, each dictionary is a single entry from the blast output
        :return: A list of accession numbers.
        """
        return self._extract("accn", entries)

    def _extract_ends(self, entries):
        """
        It takes a list of entries, extracts the end dates, and converts them into datetime objects

        :param entries: a list of dictionaries, each of which represents a single entry in the calendar
        :return: A list of dates
        """
        extracted = self._extract("end", entries)
        return list(map(_make_into_date, extracted))

    def _extract_years(self, entries, no_duplicates=True):
        """
        It takes a list of entries and returns a list of years

        :param entries: a list of dictionaries, each of which represents a single entry in the database
        :param no_duplicates: If True, only unique values are returned, defaults to True (optional)
        :return: A list of years.
        """
        return self._extract("fy", entries, no_duplicates)

    def _extract_quarters(self, entries):
        """
        It takes a list of entries, extracts the quarters from them, and returns a list of quarters

        :param entries: the list of entries to extract from
        :return: A list of tuples, where each tuple is a pair of strings.
        """
        extracted = self._extract("fp", entries, no_duplicates=False)
        return list(map(_replace_string_in_period, extracted))

    def _extract_forms(self, entries):
        """
        It extracts all the forms from the entries, and returns them as a list

        :param entries: a list of dictionaries, each of which represents a single entry in the dictionary
        :return: A list of all the forms in the entries.
        """
        return self._extract("form", entries, no_duplicates=False)

    def _extract_filed(self, entries):
        """
        It extracts the "filed" field from the entries, and converts the strings into dates

        :param entries: a list of dictionaries, each of which represents a single entry in the log file
        :return: A list of dates
        """
        extracted = self._extract("filed", entries)
        return list(map(_make_into_date, extracted))

    def _extract_entries(self, form):
        """
        It returns a list of all the entries in the call that have the given form and are not frames

        :param form: The form of the word to extract
        :return: A list of entries that have the form "verb" and do not have a frame.
        """
        return [
            entry
            for entry in self.call
            if entry["form"] == form and "frame" not in entry
        ]

    def extract(self, form):
        """
        It takes a form type, extracts the relevant information from the HTML, and returns a list of tuples
        containing the information

        :param form: The form type you're looking for
        :return: A list of tuples.
        """
        entries = self._extract_entries(form)
        values = self._extract_values(entries)
        accession = self._extract_accession_nums(entries)
        ends = self._extract_ends(entries)
        years = self._extract_years(entries)
        if form == "10-Q":
            years = self._extract_years(entries, no_duplicates=False)
        quarters = self._extract_quarters(entries)
        forms = self._extract_forms(entries)
        filed = self._extract_filed(entries)

        values, years = _value_handlers.years(values, years)
        return list(zip(values, accession, ends, years, quarters, forms, filed))


def extract(call, form):
    """
    It takes a callable and a form, and returns a dictionary of the values extracted from the form

    :param call: The callable to be wrapped
    :param form: The form to extract from
    :return: A list of tuples.
    """
    return Extractor(call).extract(form)
