class QueryParser:
    def __init__(self):
        pass

    def _parse_ticker(self, scalar) -> str:
        """
        > The function `_parse_ticker` takes a `scalar` argument and returns a string

        :param scalar: The scalar object that is being parsed
        :return: The ticker of the stock
        """
        return scalar.ticker

    def _parse_cik(self, scalar) -> int:
        """
        It takes a `scalar` argument, which is a `Scalar` object, and returns the `cik` attribute of that
        object

        :param scalar: The scalar value that was passed in
        :return: The cik number of the company
        """
        return scalar.cik

    def _parse_xtags(self, scalars: list) -> dict:
        """
        It takes a list of scalars and returns a dictionary of lists

        :param scalars: list of scalars
        :type scalars: list
        :return: A dictionary with the following keys:
            xtag
            value
            accession
            end
            year
            quarter
            form
            filed
        """
        cols = [
            (
                scalar.xtag,
                scalar.value,
                scalar.accession,
                scalar.end,
                scalar.year,
                scalar.quarter,
                scalar.form,
                scalar.filed,
            )
            for scalar in scalars
        ]
        xtags, values, accessions, ends, years, quarters, forms, filed = list(
            map(list, list(zip(*cols)))
        )
        return {
            "xtag": xtags,
            "value": values,
            "accession": accessions,
            "end": ends,
            "year": years,
            "quarter": quarters,
            "form": forms,
            "filed": filed,
        }
