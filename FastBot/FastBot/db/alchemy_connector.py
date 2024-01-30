from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from ..utils.logger import logger
from dotenv import load_dotenv
import os

load_dotenv()


class PostgreSQLDBConnection():

    distance_enabled = os.getenv("DISTANCE", "False").lower() == "true"

    def __init__(self, user, password, host, port, database):

        try:

            connection_string = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

            self.engine = create_engine(
                connection_string,
                connect_args={'connect_timeout': int(os.getenv('ALCHEMY_TIMEOUT'))},
                pool_size=int(os.getenv('ALCHEMY_POOL_SIZE'))
            )

        except ConnectionError as e:
            logger.error("Failed to connect to PostgreSQL: %s", e)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def get_session(self):

        return self.session
