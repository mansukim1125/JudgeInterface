import mariadb
import configparser

config = configparser.ConfigParser()
config.read('../../DB.ini')

def create_connection_pool():
    pool = mariadb.ConnectionPool(
        user=config['DB']['USER'],
        password=config['DB']['PASSWORD'],
        host=config['DB']['HOST'],
        port=config['DB']['PORT'],
        pool_name=config['DB']['POOL_NAME'],
        pool_size=config['DB']['POOL_SIZE']
    )
    return pool

pool = create_connection_pool()

class Connection:
    pconn = None
    def __init__(self) -> None:
        try:
            self.pconn = pool.get_connection()

        except mariadb.PoolError as e:
            self.pconn = mariadb.connection(
                user=config['DB']['USER'],
                password=config['DB']['PASSWORD'],
                host=config['DB']['HOST'],
                port=config['DB']['PORT']
            )

    def cursor(self):
        return self.pconn.cursor(dictionary=True)

    def commit(self):
        self.pconn.commit()

    def close(self):
        self.pconn.close()

    def rollback(self):
        self.pconn.rollback()

    def __del__(self) -> None:
        self.close()
