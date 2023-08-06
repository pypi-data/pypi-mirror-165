#!/usr/bin/python3
# -*- coding: utf-8 -*-
import dataclasses
import inspect
from typing import List, Dict

import fire
import sqlalchemy
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.orm.exc import NoResultFound

from automapdb.db import AutoMapDB
from automapdb.mapper import TableMapper
from automapdb.utils import filter_dict, format_return, joinsep, log

USAGE_TEMPLATE = """\
ERROR: Missing fields: {}
Usage: automapdb {action} {} {} [{}]

For detailed information on this command, run:
    automapdb {action} --help"""


@dataclasses.dataclass
class TableManager:
    """Convenient interface to PostgreSQL database objects"""

    db: AutoMapDB  # AutoMapDB object for SQLAlchemy connection
    mapping_file: str = "tables.json"
    mapper: TableMapper = None  # Ma
    sa_table: DeclarativeMeta = None  # SQLAlchemy Table
    path: str = None  # Dotted path to table, eg. public.my_table
    schema: str = None  # Schema mapping_name, eg. public
    columns: list = None  # List of columns in table
    shortcut: str = None  # User given mapping_name as in mapper
    set_args: List[str] = None  # Args needed to add data (NOT NULL)
    get_args: List[str] = None  # Args needed to query data (PRIMARY KEY)
    opt_args: List[str] = None  # Optional args
    default_values: Dict[str, str] = None

    def __post_init__(self):
        """
        Note:
        This class is called only once and its attributes overwritten each
        time a new table is select by a public method.

        All public methods must call "_init_table()" to correctly set the
        table attributes on this object.
        """
        if self.mapper is None:
            self.mapper = TableMapper(self.db, self.mapping_file)
        if self.default_values is None:
            self.default_values = {}

    def __repr__(self):
        return self.__dict__

    def _init_table(self, table: str) -> None:
        """Map attributes from TableMapping and ProxyTable to this instance"""
        # Set shortcut as given by user
        self.shortcut = table
        # Get Mapping from TableMapper by shortcut and inherit attributes
        self.__dict__.update(self.mapper[table])
        # Get ProxyTable from Database by path
        proxy_table = self.db.get_table(self.path)
        # Inherit attributes of ProxyTable to this instance
        self.__dict__.update(proxy_table.__dict__)

    def _query(self, table: str, *args) -> dict:
        """Construct raw SQL query for a table.

        Called by add, update, delete, list.
        Args are mapped to not nullable fields on postgres table
        Args:
            table (str): sa_table mapping_name from mapper to query
            args (str): Values for get_args required to find row
        """
        self._init_table(table)
        # Validate args against table fields from table def
        self._check_args(args, self.get_args)
        query = self.db.session.query(self.sa_table)
        # Concatenate required and optional args
        for index, arg in enumerate(self.get_args):
            # If local arg is a valid column in the table:
            if arg in self.columns:
                # Get local column attribute from ORM class
                table_column = getattr(self.sa_table, arg)
                # Concatenate excl statement
                # (sa_table.column == arg) to query
                query = query.filter(table_column == args[index])
        log.debug(str(query)[:40] + str(query)[-40:-1])
        return query

    def _check_args(self, args: tuple, mandatory_args: list, opt_args=None):
        """Create usage message with missing args for given table"""
        opt_args = opt_args or []
        action = inspect.stack()[1][3]
        usage = USAGE_TEMPLATE.format(
            joinsep(mandatory_args[len(args) :]),
            self.shortcut,
            joinsep(mandatory_args, sep=" "),
            joinsep(opt_args, sep="|"),
            action=action,
        )
        if len(args) < len(mandatory_args):
            raise fire.core.FireError(usage)

    @format_return()
    def list(
        self,
        table: str,
        fields: list = None,
        like: dict = None,
        ilike: dict = None,
        **kwargs,
    ) -> list:
        """Open query to table with kwargs as WHERE filters
        Args:
            table: Table to list rows of
            fields: List of column names to include in result
            ilike: Dictionary of column name and filter value for a SQL ILIKE statement
        """
        self._init_table(table)
        # Query only table to get all the rows
        query = self.db.session.query(self.sa_table)
        if like is not None:
            for key, value in like.items():
                if key in self.columns:
                    table_column = getattr(self.sa_table, key)
                    query = query.filter(table_column.like(value))
        if ilike is not None:
            for key, value in ilike.items():
                if key in self.columns:
                    table_column = getattr(self.sa_table, key)
                    query = query.filter(table_column.ilike(value))
        # Iterate kwargs to construct filters
        for key, value in kwargs.items():
            # use only kwargs that are valid columns
            if key in self.columns:
                # Get kwarg as Column object
                table_column = getattr(self.sa_table, key)
                # Filter where Column == Value
                query = query.filter(table_column == value)
        log.debug(query)
        return [filter_dict(q, incl=fields) for q in query.all()]

    @format_return()
    def list_fields(self, table, fmt=None) -> list:
        """
        Shows the name, datatype, primary_key and nullable flags
        for the columns of given Table
        """
        self._init_table(table)
        filter = ["type", "nullable", "primary_key", "name"]
        return [filter_dict(c, incl=filter) for c in self.columns]

    @format_return()
    def get(self, table, *args, fields=None, n="one", fmt="") -> list or dict:
        """Query database for one/multiple rows.
        Use args to provide the primary keys

        Args:
            table (str): Name of table to query
            n (str): Amount of results as string (all/one)
            *args (list): List of values to excl for
            fields (list): Fields which are shown by the query
        """
        fields = fields or []
        log.debug(f"GET: {table} {args} {fields} {n}")
        if n == "one":
            try:
                query = self._query(table, *args).one()
            except NoResultFound as err:
                raise NoResultFound(f"{err}: {table}: {args}")
            data = filter_dict(query, incl=fields)
        else:
            query = self._query(table, *args).all()
            data = [filter_dict(q, incl=fields) for q in query]
        return data

    def add(self, table, *args):
        """
        Add row to table, with args mapped to the table's not_nullable fields
        """
        log.debug(f"ADD: {table} {args}")
        self._init_table(table)
        u_args = self.set_args + list(self.default_values.keys())
        self.opt_args = [c.name for c in self.columns if c.name not in u_args]
        # If number of args doesn't match number of required args
        self._check_args(args, self.set_args, self.opt_args)
        new_row_data = {}
        # Iterate ORM table & write values from default_columns to a new dict
        for col in self.columns:
            new_row_data[col.name] = self.default_values.get(col.name, None)
        # Iterate over required + optional arg names with an index
        for index, arg in enumerate(self.set_args + self.opt_args):
            # If local arg is a valid column in the table:
            if arg in self.columns:
                try:
                    # Get user arg value by index,
                    # map mapping_name: value to new dict
                    new_row_data.update({arg: args[index]})
                except IndexError:
                    # If not all optional fields are filled, use None
                    new_row_data.update({arg: None})
        # Create new SQL Table with unpacked data as kwargs
        new_row = self.sa_table(**new_row_data)
        # Add
        self.db.add(new_row)

    def update(self, table, *args):
        """Update row with args mapped to the table's not_nullable fields"""
        log.debug(f"UPDATE: {table} {args}")
        # Get raw query
        query = self._query(table, *args)
        # Add column + value to update
        arg_list = self.get_args + ["key", "value"]
        self._check_args(args, arg_list)
        # Dict from last and second to last args {key: value}
        update_data = {args[-2]: args[-1]}
        log.debug(str(update_data))
        if len(query.all()) == 0:
            raise sqlalchemy.orm.exc.NoResultFound("")
        self.db.update(query, update_data)

    def delete(self, table, *args):
        """Delete row from table"""
        log.debug(f"DEL: {table} {args}")
        query = self._query(table, *args).all()
        log.debug(str(query))
        if not query:
            return False
        for q in query:
            self.db.delete(q)
        return True

    def query_dict(self, table, data):
        """Query a table by passing a dict of key:values  to filter for"""
        self._init_table(table)
        query = self.db.session.query(self.sa_table)
        query = query.filter_by(**data)
        log.debug(str(query)[:40] + str(query)[-40:-1])
        return query
