import csv
from abc import ABC, abstractmethod
from typing import Generator, List, Optional, Tuple


class BaseCorpus(ABC):
    @abstractmethod
    def get_data(self) -> Generator[Tuple[str, str], None, None]:
        raise NotImplementedError


class RusentimentCorpus(BaseCorpus):

    CSV_DELIMITER: str = ','
    CSV_QUOTECHAR: str = '"'

    LABELS: List[str] = [
        'positive',
        'negative',
        'neutral',
        'skip',
        'speech',
    ]

    def __init__(
        self,
        data_path: Optional[str],
    ):
        self.data_path = data_path

    def get_data(self) -> Generator[Tuple[str, str], None, None]:
        if not self.data_path:
            raise ValueError('data_path is None')
        with open(self.data_path, encoding='utf8') as source:
            reader = csv.reader(
                source,
                delimiter=self.CSV_DELIMITER,
                quotechar=self.CSV_QUOTECHAR,
            )
            for i, (label, text) in enumerate(reader):
                if i == 0:  # skip headers
                    continue
                yield text, label
