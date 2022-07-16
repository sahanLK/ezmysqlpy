
import mysql.connector as mc
try:
    from .exceptions import (ServerConnectionError,
                             DatabaseSelectionError,
                             DatabaseCreateError,
                             DatabaseDropError,
                             TableCreateError,
                             RecordAddingError,
                             TableNotFoundError,
                             TableAccessError)
except ImportError:
    from exceptions import (ServerConnectionError,
                            DatabaseSelectionError,
                            DatabaseCreateError,
                            DatabaseDropError,
                            TableCreateError,
                            RecordAddingError,
                            TableNotFoundError,
                            TableAccessError)


class MySQLPy:

    def __init__(self, host, user, pwd):
        """
        Establishes a connection to the database server.
        :param host: Database Host
        :param user: Username
        :param pwd: Password
        """
        self.host = host
        self.user = user
        self.pwd = pwd

        self.db = None

        # Database server object to run server related querirs only.
        self.db_server_conn = None

        # Database connection object to run all database related queries.
        self.db_conn = None

        self.__connect_db_server()

    def __connect_db_server(self) -> None:
        """
        Connects to the MySQL Database Server.
        """
        try:
            self.db_server_conn = mc.connect(
                host=self.host,
                user=self.user,
                password=self.pwd)
            print("Connected to database server")
        except Exception:
            raise ServerConnectionError

    # Database Related methods.

    def select_db(self, database: str) -> None:
        """
        Connects to a specified MySQL Database.
        :param database: Database name.
        :return:
        """
        cursor = self.db_server_conn.cursor()
        self.db = database.lower()
        try:
            self.db_conn = mc.connect(
                host=self.host,
                user=self.user,
                password=self.pwd,
                database=self.db, )
            cursor.execute(f"USE {database};")
            print(f"Database Selected: {self.db}.")
        except Exception:
            raise DatabaseSelectionError

    def get_all_dbs(self) -> list:
        """
        Returns a list of all available datbases in the server.
        :return:
        """
        cursor = self.db_server_conn.cursor()
        cursor.execute("SHOW DATABASES;")
        all_dbs = [db[0].lower() for db in cursor]
        return all_dbs

    def db_exists(self, database: str) -> bool:
        """
        Checks if specified database exists or not.
        :param database: Database name.
        :return: bool
        """
        if database.lower() in self.get_all_dbs():
            print(f"Database exists: {database}")
            return True
        else:
            print(f'Database does not exists: {database}')
            return False

    def create_db(self, database: str) -> None:
        """
        Creates a Database.
        :param database: Database name.
        :return:
        """
        cursor = self.db_server_conn.cursor()
        try:
            cursor.execute(f"CREATE DATABASE {database};")
            print(f'Database Created: {database}')
        except Exception as e:
            msg = "Database already exists" if self.db_exists(database) else None
            raise DatabaseCreateError(msg=msg)

    def delete_db(self, database: str) -> None:
        """
        Removes the specified database from the server.
        :param database: Database name.
        :return:
        """
        cursor = self.db_server_conn.cursor()
        try:
            cursor.execute(f"DROP DATABASE {database};")
            print(f"Database dropped: {database}")
        except Exception:
            msg = "Database does not exist" if not self.db_exists(database) else None
            raise DatabaseDropError(msg=msg)

    def __check_db_selection(self) -> None:
        """
        checks if database is selected or not. If not raise an error.
        :return:
        """
        if not self.db:
            raise DatabaseSelectionError(msg="No database selected.")

    # Tables Related Methods.

    def get_all_tbs(self) -> list:
        """
        Returns a list of all available tables in the selected database.
        :return:
        """
        self.__check_db_selection()
        cursor = self.db_conn.cursor()
        cursor.execute(f"SHOW TABLES;")
        all_tables = [tb[0] for tb in cursor]
        return all_tables

    def tb_exists(self, table: str) -> bool:
        """
        Check if the specified table exists or not in the database.
        :param table: Table Name
        :return:
        """
        self.__check_db_selection()
        if table in self.get_all_tbs():
            return True
        return False

    def clear_tb(self, table: str) -> None:
        """
        Delete all the records from the specified table.
        :param table:
        :return:
        """
        self.__check_db_selection()
        if not self.tb_exists(table):
            raise TableNotFoundError

        cursor = self.db_conn.cursor()
        try:
            cursor.execute(f"DELETE FROM {table};")
            print(f"Table Cleared: {table}")
        except Exception:
            raise TableAccessError(msg="Error when deleting table records.")

    def delete_tb(self, table: str) -> None:
        """
        Delete the specified table from the database.
        :param table:
        :return:
        """
        self.__check_db_selection()
        if not self.tb_exists(table):
            raise TableNotFoundError

        cursor = self.db_conn.cursor()
        try:
            cursor.execute(f"DROP TABLE {table}")
            print(f"Table Deleted: {table}")
        except Exception:
            raise TableAccessError(msg="Error when deleting table.")

    def create_tb(self, table: str, cols: dict, primary_key: str = '') -> None:
        """
        Creates a table in the selected database.
        :param primary_key: Primary key of the table.
        :param cols: A dictionary: {column1: data_type(max_length), column2: data_type(max_length)}
        :param table: Table name.
        :return:
        """
        self.__check_db_selection()
        if self.tb_exists(table):
            raise TableCreateError(msg=f"Table '{table}' already exists.")

        # Generate cols
        if not cols:
            raise TableCreateError(msg="At least one column required.")

        col_str = ''
        prim_key_set = False
        for col_name, data_type in cols.items():
            if col_name.lower() == primary_key.lower():
                prim_key_set = True
                data_type = f"{data_type} PRIMARY KEY"
            col_str += f"{col_name} {data_type},"
        col_str = col_str.strip(col_str[-1])

        if primary_key and not prim_key_set:
            raise TableCreateError(msg=f"Invalid primary key: {primary_key}")

        cursor = self.db_conn.cursor()
        try:
            cursor.execute(f"CREATE TABLE {table} ({col_str});")
            print(f"Table Created: {table}")
        except Exception:
            raise TableCreateError

    def __explain_tb(self, table: str) -> list:
        """
        Explains the table definition.
        :param table: Table name.
        :return:
        """
        self.__check_db_selection()
        if not self.tb_exists(table):
            raise TableNotFoundError

        cursor = self.db_conn.cursor()
        cursor.execute(f"EXPLAIN {table};")
        columns = [col for col in cursor]
        return columns

    def get_tb_cols(self, table: str) -> list:
        """
        Returns a list of table column names.
        :param table: Table name.
        :return:
        """
        defs = self.__explain_tb(table)
        cols = [col[0] for col in defs]
        return cols

    def add_record(self, table: str, values: list) -> None:
        """
        Add a new record to the specified table.
        :param table: Table name.
        :param values: A list of values corresponding to the column names.
        :return:
        """
        self.__check_db_selection()
        if not self.tb_exists(table):
            raise TableNotFoundError

        cursor = self.db_conn.cursor()
        cols = self.get_tb_cols(table)
        no_of_params = ''
        for i in range(len(cols)):
            no_of_params += '%s,'
        no_of_params = no_of_params.strip(no_of_params[-1])

        try:
            cursor.execute(f"INSERT INTO {table} VALUES ({no_of_params})", values)
            self.db_conn.commit()
            print(f"New Record added into: {table}")
        except Exception as e:
            raise RecordAddingError(msg=e.__str__())

    def update_tb(self, table: str, column: str, value: str, condition: str) -> None:
        """
        Updates an existing table record.
        WARNING: If condition is empty all the records in the table, will be updated.
        :param table: Table name.
        :param column: Column name.
        :param value: New value to be updated.
        :param condition: Condition to select only specific rows.
        :return:
        """
        self.__check_db_selection()
        if not self.tb_exists(table):
            raise TableNotFoundError

        # Setting up condition query
        cond_str = ''
        if condition:
            cond_str = f'WHERE {condition}'

        cursor = self.db_conn.cursor()
        try:
            cursor.execute(F"UPDATE {table} SET {column}='{value}' {cond_str};")
            self.db_conn.commit()
            print(f"{cursor.rowcount} row(s) affected.")
        except Exception as e:
            raise TableAccessError(msg=e)

    def select_all(self, table: str, sort_by: dict = None, limit: int = None, offset: int = None) -> list:
        """
        Returns all the records in the specified table.
        :param offset: From which position the results should be taken.
        :param limit: How many results should be returned.
        :type sort_by: A dictionary: {column_name: asc_or_desc}
        :param table: Table name.
        :return:
        """
        self.__check_db_selection()
        if not self.tb_exists(table):
            raise TableNotFoundError

        # Sort the results.
        sort_query = ""
        for key, val in sort_by.items():
            if key and val:
                sort_query = f"ORDER BY {key} {val}"
            if not key and val:
                sort_query = f"ORDER BY {key} '{val}'"

        # Limit the no. of results that returns.
        limit_str = ''
        if limit:
            limit_str = f"LIMIT {limit}"

        # Set offset position.
        offset_str = ''
        if offset:
            offset_str = f"OFFSET {offset}"

        cursor = self.db_conn.cursor()
        try:
            cursor.execute(f"SELECT * FROM {table} {sort_query} {limit_str} {offset_str};")
            return cursor.fetchall()
        except Exception:
            raise TableAccessError

    def select_filtered(self, table: str,
                        cols: list, conditions: str = '', limit: int = None, offset: int = None) -> list:
        """
        Selects records that match the given conditions.
        :param offset: From which position the results should be taken.
        :param limit: How many results should be returned.
        :param conditions: Conditions to be matched.
        :param table: Table name.
        :param cols: A list of column names.
        :return:
        """
        self.__check_db_selection()
        if not self.tb_exists(table):
            raise TableNotFoundError

        cursor = self.db_conn.cursor()

        # Setting up required columns.
        if cols:
            col_str = ''
            for col in cols:
                col_str += f"{col},"
            col_str = col_str.strip(col_str[-1])
        else:
            col_str = '*'

        # Setting up conditions with "WHERE" statement.
        cond_str = ''
        if conditions:
            cond_str = f"WHERE {conditions}"

        # Limit the no. of results that returns.
        limit_str = ''
        if limit:
            limit_str = f"LIMIT {limit}"

        # Set offset position.
        offset_str = ''
        if offset:
            offset_str = f"OFFSET {offset}"

        try:
            cursor.execute(f"SELECT {col_str} FROM {table} {cond_str} {limit_str} {offset_str};")
            records = cursor.fetchall()
            return records
        except Exception:
            raise TableAccessError

    def delete_records(self, table: str, conditions: str) -> None:
        self.__check_db_selection()
        if not self.tb_exists(table):
            raise TableNotFoundError

        cursor = self.db_conn.cursor()
        try:
            cursor.execute(f"DELETE FROM {table} WHERE {conditions};")
            self.db_conn.commit()
            print(f"{cursor.rowcount} Record(s) Deleted.")
        except Exception:
            raise TableAccessError(msg="Error when Deleting the record")
