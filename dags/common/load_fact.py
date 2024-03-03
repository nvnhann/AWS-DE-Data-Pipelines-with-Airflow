from airflow.models import BaseOperator
from airflow.hooks.postgres_hook import PostgresHook

class LoadFactOperator(BaseOperator):
    ui_color = '#F98866'
    def __init__(
        self,
        connection_id: str,
        table: str,
        sql_query: str,
        is_truncated: bool = True,
        *args, **kwargs
    ):
        """
        Initializes the LoadFactOperator to load data into a fact table.

        :param connection_id: The Airflow connection ID to use for the PostgreSQL database.
        :param table: The name of the target fact table.
        :param sql_query: The SQL query to execute for loading data into the fact table.
        :param is_truncated: Flag to determine if the fact table should be truncated before loading new data.
        """
        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.connection_id = connection_id
        self.table = table
        self.sql_query = sql_query
        self.is_truncated = is_truncated

    def execute(self, context):
        postgres_hook = PostgresHook(postgres_conn_id=self.connection_id)
        self.log.info(f'Loading data into {self.table} fact table.')

        if self.is_truncated:
            self.log.info(f"Clearing data from {self.table} table...")
            postgres_hook.run(f"TRUNCATE TABLE {self.table}")
            self.log.info(f"Table {self.table} has been cleared.")

        insert_sql = f"INSERT INTO {self.table} {self.sql_query};"
        postgres_hook.run(insert_sql)

        self.log.info(f'Data has been loaded into {self.table} fact table.')
