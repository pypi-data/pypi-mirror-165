import os

import fire

from automapdb.db import AutoMapDB
from automapdb.manager import TableManager
from automapdb.mapper import TableMapper
from automapdb.utils import format_return, set_logger


class FireCLI:
    def __init__(
        self,
        db_url: str = None,
        log_level: str = None,
        mapping_file: str = "tables.json",
    ):
        # Get log level in the order: arg, env or default
        set_logger(log_level or os.getenv("LOG_LEVEL", "INFO"))
        # Get connection string in the order: arg, env or default
        db = AutoMapDB(db_url or os.getenv("DB_URL", ""))
        self.mapper = TableMapper(db, mapping_file)
        self.table = TableManager(db, mapping_file)


@format_return()
def main(fmt="str"):
    fire.Fire(FireCLI)


if __name__ == "__main__":
    main()
