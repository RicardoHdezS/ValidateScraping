import os

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ARRAY
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class ScrapingErrors(Base):
    __tablename__ = "scraping_errors"
    __table_args__ = {'schema' : os.getenv('POSTGRES_SCHEMA')}

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    date_error = Column(DateTime, nullable=False)
    date_update_error = Column(DateTime, nullable=True)
    status = Column(Integer, nullable=False)
    type_error = Column(Integer, nullable=False)
    scraper_file = Column(Integer, nullable=False)
    url_list = Column(ARRAY(String), nullable=False)
    user_assigned = Column(Integer, nullable=True)

class DescriptionErrors(Base):
    __tablename__ = "description_error"
    __table_args__ = {'schema': os.getenv('POSTGRES_SCHEMA')}

    id = Column(Integer, primary_key=True)
    taxonomy = Column(Text)
    description = Column(Text)