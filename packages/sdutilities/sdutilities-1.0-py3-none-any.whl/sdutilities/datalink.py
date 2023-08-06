'''
 #####
#     #  ####   ####  #   ##   #      #      #   #
#       #    # #    # #  #  #  #      #       # #
 #####  #    # #      # #    # #      #        #
      # #    # #      # ###### #      #        #
#     # #    # #    # # #    # #      #        #
 #####   ####   ####  # #    # ###### ######   #

######
#     # ###### ##### ###### #####  #    # # #    # ###### #####
#     # #        #   #      #    # ##  ## # ##   # #      #    #
#     # #####    #   #####  #    # # ## # # # #  # #####  #    #
#     # #        #   #      #####  #    # # #  # # #      #    #
#     # #        #   #      #   #  #    # # #   ## #      #    #
######  ######   #   ###### #    # #    # # #    # ###### #####
'''

import json
import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy.exc import ProgrammingError
from psycopg2 import errors
from io import StringIO
from sdutilities.logger import SDLogger

"""
This module contains the DataLink class and its related functions.
"""


class DataLink(object):
    """
    Class provides an easy wrapper between Pandas and PostgreSQL

    Creates database connection and provides functionality for interacting
    with the database through python and Pandas.
    Also utilizes the SDLogger class.

    Attributes:
        _logger (SDLogger): Access the SDLogger object from the
            sdutilities.SDLogger class
        _cfg_name (String): Name of the database for the connection
        _db_file (String): File path of file containing database info,
            uname, pw, certificate
        _df_cfg (Dictionary): Database info, uname, pw, host
        _engine (Engine): Access the Engine instance from the
            sqlalchemy.create_engine() function
    """

    def __init__(self, cfg_name=None, db_file=None, log_level=None,
                 log_file=True, file_log_level=None, log_file_prefix=None):
        """
        Constructor

        Args:
            cfg_name (String, optional): Database for connection
                (Defaults to 'default')
            db_file (String, optional): File path for database info
                (Defaults to './private/db_cfg.json')
            log_level (String, optional): One of
                ['DEBUG', 'INFO', 'WARNING', 'ERROR']
            log_file (bool, optional): Flag to output a log file
                (Defaults to True)
            file_log_level (String, optional): One of
                ['DEBUG', 'INFO', 'WARNING', 'ERROR']
            log_file_prefix(String, optional): Set prefix of log file name.

            NOTE: See SDLogger documentation for more information about the
                  parameters and functions associated with this class.
        """
        self._logger = SDLogger(log_level, log_file, file_log_level,
                                log_file_prefix)
        self._set_cxn_info(cfg_name=cfg_name, db_file=db_file)
        self._connect_to_engine()

        self._cfg_name = cfg_name
        self._db_file = db_file

    def _set_cxn_info(self, cfg_name=None, db_file=None):
        """Sets connection settings in dictionary.

        If the given file is not found then a default configuration is
        created.

        Args:
            cfg_name (String, optional): Database for connection
                (Defaults to 'default')
            db_file (String, optional): File path for database info
                (Defaults to './private/db_cfg.json')
        """
        default_file = './private/db_cfg.json'
        db_file = default_file if db_file is None else db_file
        cfg_name = 'default' if cfg_name is None else cfg_name

        try:
            with open(db_file) as jfile:
                cfg_dict = json.load(jfile)
        except FileNotFoundError:
            self._logger.info(f'DB Configuration file not found')

            if os.path.isfile(default_file):
                self._logger.info(
                    f'Try using the default config file {default_file}.')
            else:
                self._logger.info(
                    f'Creating default config file: {default_file}.')
                self._logger.info(
                    f'Modify this file with the correct connection settings.')

                def_cfg_file = default_file
                if not os.path.exists('./private'):
                    self._logger.info('Creating private directory...')
                    os.makedirs('./private')
                self._db_cfg = {'default': {'uname': 'postgres',
                                            'pw': 'postgres2',
                                            'host': 'localhost',
                                            'db': 'SocialScape'}
                                }
                with open(def_cfg_file, 'w') as jfile:
                    json.dump(self._db_cfg, jfile, indent=2, sort_keys=True)

            raise FileNotFoundError(
                f'Cannot open the DB config file {db_file}.')

        if cfg_name in cfg_dict:
            self._db_cfg = cfg_dict[cfg_name]
        elif 'db' in cfg_dict:
            self._db_cfg = cfg_dict
        else:
            self._logger.info(f"Missing configuration")

    def _connect_to_engine(self):
        """Creates connection to database.

        Utilizes the create_engine() function from sqlalchemy.
        """
        etype = 'postgresql+psycopg2:'

        estr = etype + '//' + self._db_cfg['uname'] + ':' + self._db_cfg['pw'] + '@'
        estr += self._db_cfg['host'] + ':5432/' + self._db_cfg['db']
        self._engine = create_engine(estr)

    def _to_pg(self, df, table, schema):
        """Fast load of data via StringIO.

        Used in DataLink.upsert() function to load a DataFrame into the
        database as a table.

        Args:
            df (DataFrame): DataFrame to load into the table.
            table (String):  Table to load DataFrame into.
            schema (String):  Schema where the table will be located.
        """
        output = StringIO()
        df.to_csv(output, sep='\t', header=False, index=False)
        output.seek(0)

        connection = self._engine.raw_connection()
        cursor = connection.cursor()
        cursor.copy_from(output, f'{schema}.{table}', null='',
                         columns=(df.columns))
        connection.commit()
        cursor.close()

    def _check_exists(self, table=None, schema=None):
        """Checks for existence of table and schema in the database.

        Used in many functions to check for table and schema existence in the
        database before throwing informative errors.

        Args:
            table (String, Optional): Table to find in schema.
            schema (String, Optional): Schema to find in database.
        """

        insp = inspect(self._engine)

        if schema:
            if not self._engine.dialect.has_schema(self._engine, schema):
                db = self._db_cfg['db']
                raise ValueError(
                    f'The schema {schema} does not exist in {db}.')

        if table:
            if not insp.has_table(table, schema):
                raise ValueError(
                    f'The table {table} does not exist in {schema}.')

    def get_engine(self):
        """Returns the engine instance of the database connection.

        See sqlalchemy documentation for more information.

        Returns:
            _engine (Engine): Access the Engine instance from the
                _connect_to_engine() function call.
        """
        return self._engine

    def get_connection_info(self):
        """Returns the information from the database configuration file.

        Returns:
            _df_cfg (Dictionary): Database info, uname, pw, host.
        """
        return self._db_cfg

    def reset_connection(self):
        """Resets connection settings in dictionary.

        Makes a call to _set_cxn_info(), so the defaults for that function
        are used.
        """
        self._set_cxn_info(self._cfg_name, self._db_file)
        self._connect_to_engine()

    def run_sql(self, sql):
        """Executes an SQL statement.

        Args:
            sql (String): SQL statement to execute.
        """
        self._engine.execute(sql)

    def sql_to_df(self, sql):
        """Returns the output from an SQL statement as a DataFrame.

        Args:
            sql (String): SQL statement to execute.

        Returns:
            df (DataFrame): DataFrame containing SQL statement results.
        """
        return pd.read_sql_query(sql, self._engine)

    def build_where_clauses(self, constraints):
        """Creates SQL where clauses as strings for queries.

        Args:
            constraints (DataFrame or Columns of DataFrame): Constraints to
                build where clause.

        Returns:
            where_list (List of Strings): List of where clauses for queries.
        """
        constraints = constraints.drop_duplicates()
        where_list = []
        for val in constraints.values:
            cons = []
            if isinstance(constraints, pd.DataFrame):
                for c, v in zip(constraints.columns, val):
                    cons.append(f"{c}='{v}'")
            else:
                cons.append(f"{constraints.name}='{val}'")
            where_clause = ' AND '.join(cons)
            where_list.append(where_clause)
        return where_list

    def query_to_df(self, table, schema, index=None, cols='*',
                    where_clause=None, limit=None):
        """Returns the results of a select statement as a DataFrame.

        Args:
            table (String): Table to retrieve as a DataFrame.
            schema (String): Schema where the table is located.
            index (String or List of Strings, optional): Column(s) to set as
                index (defaults to None).
            cols (String or List of Strings, optional): Column(s) to select in
                SQL query (default set to '*')
            where_clause (String or List of Strings, optional): Where clause
                to use in SQL select statement (default set to None).
            limit (int, optional): Number of rows of the table to retrieve
                (default set to None).

        Returns:
            df (DataFrame): DataFrame containing SQL query results.
        """
        self._check_exists(table, schema)

        if not isinstance(cols, list):
            cols = [cols]

        if index:
            if not isinstance(index, list):
                index = [index]
            if not set(index) < set(cols) and '*' not in cols:
                raise ValueError(
                    f'The index list must be a subset of the columns.')

        cols = ','.join(cols)

        if limit:
            lim_str = f'LIMIT {limit}'
        else:
            lim_str = ''

        if where_clause:
            if isinstance(where_clause, list):
                where_str = 'WHERE ' + ' AND '.join(where_clause)
            else:
                where_str = f' WHERE {where_clause}'
        else:
            where_str = ''

        sql = f'SELECT {cols} FROM {schema}.{table} {where_str} {lim_str}'

        return pd.read_sql_query(sql, self._engine, index_col=index)

    def upsert(self, df, table, schema, constraint_cols=None,
               owner='sdrc_admins'):
        """ Completes an update or insert of a DataFrame to a table in
        the database.

        There are three possible actions:
            1. Table does not exist, it is created using the data from df.
            2. Table exists, but the df is new data. Data appended.
            3. Table exists, df is updated data. Rows dropped and re-added.

        Args:
            df (DataFrame): DataFrame to load into the table.
            table (String): Table to load DataFrame into.
            schema (String): Schema where the table will be located.
            constraint_cols (String or List of Strings): Columns of the
                DataFrame to build upsert where clause (default set to None).
            owner (String, optional): Name of the account to set as the owner
                of the table (default set to 'sdrc_admins').
        """
        self._check_exists(schema=schema)

        if constraint_cols:
            if not isinstance(constraint_cols, list):
                constraint_cols = [constraint_cols]
            if not set(constraint_cols) < set(df):
                raise ValueError(
                    'The constraints list must be a subset of the columns.')
        try:
            sql = pd.io.sql.get_schema(df, f'{schema}.{table}')
            sql = sql.replace('"', '')
            self._engine.execute(sql)
            self._to_pg(df, table, schema)
            self.update_owner(table, schema, owner)
            self._logger.info(f'Created {schema}.{table} with provided data.')
            self._logger.debug(f'Inserted data from {df}.')

        except ProgrammingError:
            if constraint_cols:
                where_list = self.build_where_clauses(df[constraint_cols])
                msg = 'Deleting entries for given constraints.'
                self._logger.info(
                    f'{schema}.{table} already exists. {msg}')
                self._logger.debug(f'Upsert delete where list: {where_list}.')

                for where_clause in where_list:
                    self.delete_rows(table, schema, where_clause)
            else:
                msg = 'No constraints provided, inserting data to table.'
                self._logger.info(
                    f'{schema}.{table} already exists. {msg}')

            self._logger.info(f'Writing dataframe to {schema}.{table}.')
            self._to_pg(df, table, schema)

    def delete_rows(self, table, schema, where_clause=None):
        """ Deletes rows from a table in the database.

        Args:
            table (String): Table to delete rows from.
            schema (String): Schema where the table is located.
            where_clause (String or List of Strings): Where clause to use in \
                SQL select statement (default set to truncate table).
        """
        self._check_exists(table, schema)

        try:
            if where_clause == '*':
                self._engine.execute(f'TRUNCATE {schema}.{table}')
                self._logger.info(
                    f"Where_clause = '*' provided. Deleting all entries")
            elif where_clause is None:
                self._logger.info(
                    f'No where_clause provided. No rows deleted.')
            else:
                sql = "DELETE FROM {}.{} WHERE {}".format(schema, table,
                                                          where_clause)
                self._engine.execute(sql)

        except ProgrammingError as sqla_error:
            try:
                raise sqla_error.orig
            except errors.UndefinedColumn:
                msg = 'Bad where_clause provided, column name does not exist.'
                raise ValueError(
                    f'Unable to delete rows from {schema}.{table}. {msg}') from None

    def drop_table(self, table, schema):
        """ Drops a table in the database.

        Args:
            table (String): Table to drop.
            schema (String): Schema where table is located.
        """
        self._check_exists(table, schema)

        try:
            self._engine.execute(f'DROP TABLE {schema}.{table}')
            self._logger.info(f'Dropping {schema}.{table}')

        except ProgrammingError:
            db = self._db_cfg['db']
            raise ValueError(
                f'Unable to drop {schema}.{table} from {db}.')

    def update_owner(self, table, schema, new_owner):
        """ Updates the owner of the given table.

        Args:
            table (String): Table to change owner.
            schema (String): Schema where table is located.
            new_owner (String): Name of account to set as new owner of table.
        """
        self._check_exists(table, schema)

        try:
            sql = 'ALTER TABLE ' + schema + '.' + table + ' OWNER TO ' + new_owner
            self._engine.execute(sql)
        except ProgrammingError:
            raise ValueError(
                f'Unable to change owner of {schema}.{table} to {new_owner}.')
