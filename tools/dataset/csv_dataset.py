import csv
from decimal import Decimal

from catalog.config import config
from .dataset import Dataset


class CsvDataset(Dataset):
    """Represents a csv a dataset structured as a list of dictionaries."""

    def __init__(self, dataset, columns_mapping, column_to_add_to_group):
        super().__init__(dataset, columns_mapping, column_to_add_to_group)
        self.dataset_source = config.DATASET_SOURCE_CSV
        self.log.debug('Reading a csv dataset')

    def _process(self, dataset):
        """Overrides _process to process the dataset from a csv resource.
        Transforms the given dataset to a list of ordered dictionaries.
        """
        rows = csv.DictReader(dataset.splitlines(True), delimiter=config.DELIMITER_CSV)
        for row in rows:
            self._map_column_names(row)
            self._clean_row(row)
            self._correct_columns(row)
            if row[self.column_to_add_to_group.column1] and row[self.column_to_add_to_group.column2]:
                row[self.column_to_add_to_group.new_column] = f"{row[self.column_to_add_to_group.column1]}" \
                                                         f"{config.DELIMITER}" \
                                                         f"{row[self.column_to_add_to_group.column2]}"
            else:
                row[self.column_to_add_to_group.new_column] = ''
            yield row

    def _correct_amount(self, amount):
        """Overrides _correct_amount to correct an amount field.
        Converts field amount to a Decimal object correcting its decimal separator if needed.
        """
        if config.DECIMAL_SEPARATOR_CSV == '.':
            return Decimal(str(amount).replace(config.THOUSANDS_SEPARATOR_CSV, ''))
        return Decimal(str(amount).replace(config.THOUSANDS_SEPARATOR_CSV, '')
                       .replace(config.DECIMAL_SEPARATOR_CSV, '.'))
