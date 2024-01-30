import os

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TaxonomyName(Base):
    __tablename__ = "taxonomy_name"
    __table_args__ = {'schema': os.getenv('POSTGRES_SCHEMA')}

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)

class StatusSpider(Base):
    __tablename__ = "status_spider"
    __table_args__ = {'schema': os.getenv('POSTGRES_SCHEMA')}

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class FrequencySpider(Base):
    __tablename__ = "frequency_spider"
    __table_args__ = {'schema': os.getenv('POSTGRES_SCHEMA')}

    id = Column(Integer, primary_key=True)
    crontab = Column(Text, nullable=False)
    description = Column(Text)

class UserScraperValidator(Base):
    __tablename__ = "users_scraper_validator"
    __table_args__ = {'schema': os.getenv('POSTGRES_SCHEMA')}

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    last_name = Column(String)
    date_register = Column(DateTime, nullable=False)
    status = Column(String)

class TypeSpiders(Base):
    __tablename__ = "type_spiders"
    __table_args__ = {'schema': os.getenv('POSTGRES_SCHEMA')}

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    command = Column(String)

class ClassificationSpiders(Base):
    __tablename__ = "classification_spiders"
    __table_args__ = {'schema': os.getenv('POSTGRES_SCHEMA')}

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)

class CountrySpiders(Base):
    __tablename__ = "country_spiders"
    __table_args__ = {'schema': os.getenv('POSTGRES_SCHEMA')}

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)

class StateSpiders(Base):
    __tablename__ = "state_spiders"
    __table_args__ = {'schema': os.getenv('POSTGRES_SCHEMA')}

    id = Column(Integer, primary_key=True)
    country_id = Column(Integer)
    state_id = Column(Integer, nullable=False)
    state_name = Column(String, nullable=False)

class WitnessCarpetLocation(Base):
    __tablename__ = "witness_carpet_location"
    __table_args__ = {'schema': os.getenv('POSTGRES_SCHEMA')}

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    location = Column(Text)

class ScrapersData(Base):
    __tablename__ = "scrapers_data"
    __table_args__ = {'schema': os.getenv('POSTGRES_SCHEMA')}

    id = Column(Integer, primary_key=True)
    name = Column(String)
    cve_medio = Column(Integer)
    status = Column(Integer)
    frequency = Column(Integer)
    start_urls = Column(Text)
    allowed_domains = Column(Text)
    selector_sections = Column(Text)
    selector_notes = Column(Text)
    selector_publish_date = Column(Text)
    selector_modified_date = Column(Text)
    selector_title = Column(Text)
    selector_author = Column(Text)
    selector_content = Column(Text)
    attrs_titles = Column(Text)
    selector_remove_elements = Column(Text)
    regex_allow_domains = Column(Text)
    regex_deny_sections = Column(Text)
    limit_to_scrape = Column(Integer)
    user_creator_spider = Column(Integer)
    date_creation_spider = Column(DateTime)
    user_last_update_spider = Column(Integer)
    date_last_update_spider = Column(DateTime)
    type_template = Column(Integer)
    classification = Column(Integer)
    country = Column(Integer)
    witness_carpet_location = Column(Integer)
    is_utc = Column(Boolean)
    is_other_format = Column(Boolean)
    str_format = Column(Text)
    is_json = Column(Boolean)
    to_validate_user = Column(Integer)
    error_to_solve = Column(Integer)
