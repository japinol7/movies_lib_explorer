from decimal import Decimal
from collections import OrderedDict

from ...config import config
from .dataset import Dataset


class JsonDataset(Dataset):
    """Represents a json a dataset structured as a list of dictionaries."""

    def __init__(self, dataset, columns_mapping, column_to_add_to_group):
        super().__init__(dataset, columns_mapping, column_to_add_to_group)
        self.dataset_source = config.DATASET_SOURCE_JSON
        self.log.debug('Reading a json dataset')

    def _process(self, dataset):
        """Overrides _process to process the dataset from a json resource.
        Transforms the given dataset to a list of ordered dictionaries.
        """
        dataset = (OrderedDict(x.items()) for x in dataset)
        for row in dataset:
            self._map_column_names(row)
            self._clean_row(row)
            self._correct_columns(row)
            yield row

    def _correct_amount(self, amount):
        """Overrides _correct_amount to correct an amount field.
        Converts field amount to a Decimal object.
        """
        return Decimal(str(amount))
