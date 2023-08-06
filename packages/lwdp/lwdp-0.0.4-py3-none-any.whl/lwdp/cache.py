import logging
from pathlib import Path
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)


class Cache:
    """ Cache object supporting reading and writing from a cache locale. Current only "local" supported."""

    @property
    def output_path(self):
        result = Path.home() / ".lwdp_cache"
        if self.subdir is not None:
            result = result / self.subdir
        if self.locale == 'local':
            result.mkdir(exist_ok=True)
            return result
        else:
            raise NotImplementedError("Anything other than local cacheing not implemented")

    def __init__(self, locale: str = 'local', format: str = 'csv', subdir=None):
        self.locale = locale
        self.format = format
        self.subdir = subdir

    def read(self, path: Path) -> Optional[pd.DataFrame]:
        """ Reads the filename with the given path (hash) and appended filename extension based on
        the cache format (csv, parquet, etc.)"""
        full_path = self.output_path / f"{path}.{self.format}"
        candidate_read_method = getattr(pd, f'read_{self.format}', None)
        if candidate_read_method is None:
            raise NotImplementedError(f"No method {self.format} to read using pandas")
        logger.info(f"Attempting cache read at {full_path}")
        if full_path.exists():
            return candidate_read_method(full_path)
        else:
            return None

    def write(self, pdf: pd.DataFrame, path: Path):
        final_output_path = self.output_path / f"{path}.{self.format}"
        candidate_write_method = getattr(pdf, f'to_{self.format}', None)
        if candidate_write_method is not None:
            logger.info(f"Writing cache to {final_output_path}")
            candidate_write_method(final_output_path)
        else:
            raise NotImplementedError(f"{self.format} not a support 'to_XXX' format by pandas!")
