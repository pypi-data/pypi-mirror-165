#!/usr/bin/python3.8
# -*- coding: utf-8 -*-

import atexit

from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.automap import AutomapBase, automap_base
from sqlalchemy.orm import DeclarativeMeta, Session
from sqlalchemy.orm.query import Query
from sqlalchemy.sql.base import ImmutableColumnCollection

from automapdb.utils import Singleton, log


class ProxyTable:
    def __init__(self, schema: str, name: str, sa_table: DeclarativeMeta):
        """Simple wrapper around the SQLAlchemy Table"""
        self.name: str = name
        self.schema: str = schema
        self.sa_table: DeclarativeMeta = sa_table
        self.columns: ImmutableColumnCollection = self.sa_table.__table__.columns
        self.path: str = f"{schema}.{name}"

    def primary_keys(self) -> list:
        """Get primary keys from table metadata"""
        return [c.name for c in self.columns if c.primary_key]

    def not_nullable(self) -> list:
        """Get not nullable fields from table metadata"""
        return [c.name for c in self.columns if not c.nullable]


class AutoMapDB(metaclass=Singleton):
    """Manage Basic Database connection"""

    def __init__(self, db_url: str, options: dict = None, autocommit: bool = False):
        """Create basic database session through SQLAlchemy"""
        log.debug(f"{self.__class__.__name__}")
        self.raise_on_rollback: bool = True
        self.autocommit: bool = autocommit
        self.metadata: MetaData = None
        self.commit: bool = False
        self.schema: str = None
        self.base: DeclarativeMeta = None

        # Instantiate engine, pass on options
        self.engine: Engine = create_engine(db_url, connect_args=options or {})
        log.debug(f"Connecting to database: {db_url}")

        # Open connection with engine
        self.connection: Connection = self.engine.connect()

        # Create session
        self.session: Session = Session(
            self.engine, autoflush=True, expire_on_commit=False
        )
        log.debug("Connection and Session opened.")

    def set_schema(self, schema: str):
        """
        Create metadata object from schema, map base to schema

        I found it impossible to map a base across all postgres schemas or
        use dotted table paths. Therefore an sa_table object needs to set
        which schema it belongs to before querying.
        """
        # Skip if schema is already set
        if self.schema == schema:
            return
        self.schema = schema

        # Create MetaData object with schema name
        self.metadata: MetaData = MetaData(schema=self.schema)
        # Obtain table metadata through reflection
        self.metadata.reflect(self.engine)
        # Create Base object
        self.base: AutomapBase = automap_base(metadata=self.metadata)
        # Create mapper from MetaData
        self.base.prepare()
        log.debug(f"Schema {self.schema} mapped")

    def get_table(self, path) -> ProxyTable:
        """Set schema and create ProxyTable from AutomapBase"""
        try:
            schema, tab_name = path.split(".")
        except ValueError:
            msg = f"Invalid path: '{path}'. Does it contain 'schema.table'?"
            raise Exception(msg)

        # Update database search path
        self.set_schema(schema)
        # Get SQLAlchemy sa_table object through db object
        sa_table = getattr(self.base.classes, tab_name)
        return ProxyTable(schema, tab_name, sa_table)

    def post_statement(self, force_commit: bool = None) -> bool:
        """Configurable hook called after each CRUD operation"""
        try:
            # Push pending operations to the database
            self.session.flush()
            # Set commit switch to trigger commit later
            self.commit = True
        # Catch SQL errors early
        except SQLAlchemyError as err:
            msg = f"{err.__cause__.__class__.__name__}: {err.__cause__}"
            log.error(msg.replace("\n", " "))
        except Exception as err:
            log.error(repr(err))
            self.session.rollback()
            self.commit = False
            log.warning("Rollback done!")
            if self.raise_on_rollback:
                raise err

        if force_commit or self.autocommit:
            try:
                log.info("Trying autocommit...")
                self.session.commit()
                return True
            except Exception as err:
                msg = f"{err.__cause__.__class__.__name__}: {err.__cause__}"
                log.error(msg.replace("\n", " "))
                self.session.rollback()
        return False

    def execute(self, query: Query, *args) -> bool:
        """Add `CREATE` query to psql session and flushes handler"""
        self.session.execute(query, *args)
        return self.post_statement()

    def add(self, query: Query) -> bool:
        """Add `CREATE` query to psql session and flushes handler"""
        self.session.add(query)
        return self.post_statement()

    def update(self, query: Query, data: dict) -> bool:
        """Add `UPDATE` query to the session and flushes the connection"""
        query.update(data)
        return self.post_statement()

    def delete(self, query: Query) -> bool:
        """Add `DELETE` query to psql session and flushes handler"""
        self.session.delete(query)
        return self.post_statement()


# Ugly hack to ensure transactions are committed on exit
@atexit.register
def post_db():
    try:
        db = AutoMapDB(None)
    except AttributeError:
        log.debug("Looks like no database is connected... Closing.")
        return
    log.debug(f"Closing {db.engine}...")
    if db.commit:
        try:
            db.session.commit()
        except SQLAlchemyError as err:
            log.error(err)
            print(err)
