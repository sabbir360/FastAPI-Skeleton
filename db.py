from peewee import PostgresqlDatabase
from functools import lru_cache
from config import config


class DatabaseManager:
    _db_instance = None

    @classmethod
    def get_database(cls):
        """
        Gets the database instance. If the instance does not exist, it creates
        a new one using the configuration provided in the config.yaml file.

        Returns:
            peewee.PostgresqlDatabase: The database instance.
        """

        

        db_config = config['database']
        if db_config.get('name') is None:
            raise ValueError(
                'Database name is not specified in the config.yaml file.')
        if cls._db_instance is None:
            cls._db_instance = PostgresqlDatabase(
                db_config['name'],
                user=db_config['username'],
                password=db_config['password'],
                host=db_config['host'],
                port=db_config['port']
            )
        return cls._db_instance

# Dependency for FastAPI


@lru_cache
def get_db():
    """
    Retrieve a cached instance of the database connection.

    Utilizes an LRU cache to store and retrieve the database connection, 
    ensuring that the same instance is used throughout the application 
    lifetime unless the cache is cleared.

    Returns:
        PostgresqlDatabase: A singleton instance of the database connection.
    """

    return DatabaseManager.get_database()


def clear_get_db_cache():
    get_db.cache_clear()
