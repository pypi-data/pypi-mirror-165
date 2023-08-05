import csv
from argparse import Namespace
from typing import Iterable

from transformers_lightning.adapters.file_adapter import FileAdapter
from transformers_lightning.utils import strip_lines


class CSVAdapter(FileAdapter):
    r"""
    An Adapter to load data from a CSV file. Only adds a `filepath` parameter.
    Use kwargs to pass parameters directly to the csv reader, like `delimiter` or `quotechar`.
    """

    def __init__(self, hyperparameters: Namespace, filepath: str, **kwargs):
        super().__init__(hyperparameters, filepath)
        self.csv_kwargs = kwargs

    def __iter__(self) -> Iterable:
        r"""
        Return a generator of parsed lines.
        """
        with open(self.filepath, "r") as fi:
            # use utils.strip_lines to emulate skip_blank_lines of pd.DataFrame
            reader = csv.reader(strip_lines(fi), **self.csv_kwargs)
            yield from reader
