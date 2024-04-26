from pandas import DataFrame
from snowflake import connector
from snowflake.sqlalchemy import snowdialect

from mindsdb_sql.render.sqlalchemy_render import SqlalchemyRender
from mindsdb_sql.parser.ast.base import ASTNode

from mindsdb.integrations.libs.base import DatabaseHandler
from mindsdb.integrations.libs.response import (
    HandlerStatusResponse as StatusResponse,
    HandlerResponse as Response,
    RESPONSE_TYPE
)
from mindsdb.utilities import log

logger = log.getLogger(__name__)


class SnowflakeHandler(DatabaseHandler):
    """
    This handler handles connection and execution of the Snowflake statements.
    """

    name = 'snowflake'

    def __init__(self, name, **kwargs):
        super().__init__(name)
        self.connection_data = kwargs.get('connection_data')
        self.is_connected = False
        self.connection = None

    def connect(self):
        """
        Establishes a connection to a Snowflake account.

        Raises:
            snowflake.connector.errors.Error: If an error occurs while connecting to the Snowflake account.

        Returns:
            snowflake.connector.connection.SnowflakeConnection: A connection object to the Snowflake account.
        """

        if self.is_connected is True:
            return self.connection
        
        # Mandatory connection parameters
        if not all(key in self.connection_data for key in ['account', 'user', 'password']):
            raise ValueError('Required parameters (account, user, password) must be provided.')

        config = {
            'account': self.connection_data.get('account'),
            'user': self.connection_data.get('user'),
            'password': self.connection_data.get('password')
        }

        # Optional connection parameters
        if 'database' in self.connection_data:
            config['database'] = self.connection_data.get('database')

        if 'schema' in self.connection_data:
            config['schema'] = self.connection_data.get('schema')

        if 'warehouse' in self.connection_data:
            config['warehouse'] = self.connection_data.get('warehouse')

        if 'role' in self.connection_data:
            config['role'] = self.connection_data.get('role')
        
        try:
            self.connection = connector.connect(**config)
            self.is_connected = True
            return self.connection
        except connector.errors.Error as e:
            logger.error(f'Error connecting to Snowflake, {e}!')
            raise

    def disconnect(self):
        """
        Closes the connection to the Snowflake account if it's currently open.
        """

        if self.is_connected is False:
            return
        self.connection.close()
        self.is_connected = False

    def check_connection(self) -> StatusResponse:
        """
        Checks the status of the connection to the Snowflake account.

        Returns:
            StatusResponse: An object containing the success status and an error message if an error occurs.
        """

        response = StatusResponse(False)
        need_to_close = self.is_connected is False
        try:
            # Execute a simple query to test the connection
            connection = self.connect()
            with connection.cursor() as cur:
                cur.execute('select 1;')
            response.success = True
        except connector.errors.Error as e:
            logger.error(f'Error connecting to Snowflake, {e}!')
            response.error_message = str(e)

        if response.success and need_to_close:
            self.disconnect()

        elif not response.success and self.is_connected:
            self.is_connected = False
            
        return response

    def native_query(self, query: str) -> Response:
        """
        Receive SQL query and runs it
        :param query: The SQL query to run in Snowflake
        :return: returns the records from the current recordset
        """
        need_to_close = self.is_connected is False
        connection = self.connect()
        from snowflake.connector import DictCursor
        with connection.cursor(DictCursor) as cur:
            try:
                cur.execute(query)
                result = cur.fetchall()
                if result:
                    response = Response(
                        RESPONSE_TYPE.TABLE,
                        DataFrame(
                            result,
                            columns=[x[0] for x in cur.description]
                        )
                    )
                else:
                    response = Response(RESPONSE_TYPE.OK)
            except Exception as e:
                logger.error(f'Error running query: {query} on {self.connection_data["database"]}!')
                response = Response(
                    RESPONSE_TYPE.ERROR,
                    error_message=str(e)
                )
        if need_to_close is True:
            self.disconnect()
        return response

    def get_tables(self) -> Response:
        """
        Get a list with all of the tabels in the current database or schema
        that the user has acces to
        """
        q = "SHOW TABLES;"
        result = self.native_query(q)
        result.data_frame = result.data_frame.rename(columns={'name': 'table_name'})
        return result

    def get_columns(self, table_name) -> Response:
        """
        List the columns in the tabels for which the user have access
        """
        q = f"SHOW COLUMNS IN TABLE {table_name};"
        result = self.native_query(q)
        return result

    def query(self, query: ASTNode) -> Response:
        """
        Retrieve the data from the SQL statement.
        """
        renderer = SqlalchemyRender(snowdialect.dialect)
        query_str = renderer.get_string(query, with_failback=True)
        return self.native_query(query_str)
