from FastBot.FastBot.db.alchemy_connector import PostgreSQLDBConnection
from datetime import datetime
import os
from dotenv import load_dotenv
from FastBot.FastBot.utils.logger import logger
from FastBot.FastBot.data.models.scrapers import (
    ScrapersData, TaxonomyName, TypeSpiders, FrequencySpider
)
from FastBot.FastBot.data.models.errors import ScrapingErrors, DescriptionErrors
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import json

load_dotenv()

class ScrapersConnector:

    def get_connection(self):

        logger.info("Starting connection with PostgreSQL")

        db_connection = PostgreSQLDBConnection(
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=int(os.getenv("POSTGRES_PORT")),
            database=os.getenv("POSTGRES_DB")
        )

        self.session = db_connection.get_session()

        return self.session

session = ScrapersConnector().get_connection()

try:
    query = (
        session.query(
            ScrapersData.id.label('scraper_id'),
            ScrapersData.name.label('scraper_name'),
            ScrapersData.cve_medio.label('scraper_medium_id'),
            TaxonomyName.name.label('medium_name'),
            ScrapersData.status.label('scraper_status'),
            ScrapersData.frequency.label('scraper_frequency'),
            FrequencySpider.crontab.label('frequency_crontab'),
            FrequencySpider.description.label('frequency_description'),
            ScrapersData.start_urls.label('scraper_start_urls'),
            ScrapersData.allowed_domains.label('scraper_allowed_domains'),
            ScrapersData.selector_sections.label('scraper_selector_sections'),
            ScrapersData.selector_notes.label('scraper_selector_notes'),
            ScrapersData.selector_publish_date.label('scraper_selector_publish_date'),
            ScrapersData.selector_modified_date.label('scraper_selector_modified_date'),
            ScrapersData.selector_title.label('scraper_selector_title'),
            ScrapersData.selector_author.label('scraper_selector_author'),
            ScrapersData.selector_content.label('scraper_selector_content'),
            ScrapersData.attrs_titles.label('scraper_attrs_titles'),
            ScrapersData.selector_remove_elements.label('scraper_selector_remove_elements'),
            ScrapersData.regex_allow_domains.label('scraper_regex_allow_domains'),
            ScrapersData.regex_deny_sections.label('scraper_regex_deny_sections'),
            ScrapersData.limit_to_scrape.label('scraper_limit_to_scrape'),
            ScrapersData.user_creator_spider.label('scraper_user_creator_spider'),
            ScrapersData.date_creation_spider.label('scraper_date_creation_spider'),
            ScrapersData.user_last_update_spider.label('scraper_user_last_update_spider'),
            ScrapersData.date_last_update_spider.label('scraper_date_last_update_spider'),
            ScrapersData.type_template.label('scraper_type_template'),
            TypeSpiders.name.label('type_spider_name'),
            ScrapersData.is_utc.label('scraper_is_utc'),
            ScrapersData.is_other_format.label('scraper_is_other_format'),
            ScrapersData.str_format.label('scraper_str_format'),
            ScrapersData.is_json.label('scraper_is_json'),
            DescriptionErrors.taxonomy.label('description_errors_taxonomy'),
            DescriptionErrors.description.label('description_errors_description')
        )
        .join(TaxonomyName, TaxonomyName.id == ScrapersData.cve_medio)
        .join(FrequencySpider, ScrapersData.frequency == FrequencySpider.id)
        .join(TypeSpiders, ScrapersData.type_template == TypeSpiders.id)
        .join(DescriptionErrors, ScrapersData.error_to_solve == DescriptionErrors.id)
        .where(ScrapersData.to_validate_user == int(os.getenv("USER_VALIDATOR")))
        .group_by(
            ScrapersData.id, ScrapersData.name, ScrapersData.cve_medio,
            TaxonomyName.name, ScrapersData.status, ScrapersData.frequency,
            ScrapersData.start_urls, ScrapersData.allowed_domains,
            ScrapersData.selector_sections, ScrapersData.selector_notes,
            ScrapersData.selector_publish_date, ScrapersData.selector_modified_date,
            ScrapersData.selector_title, ScrapersData.selector_author,
            ScrapersData.selector_content, ScrapersData.attrs_titles,
            ScrapersData.selector_remove_elements, ScrapersData.regex_allow_domains,
            ScrapersData.regex_deny_sections, ScrapersData.limit_to_scrape,
            ScrapersData.user_creator_spider, ScrapersData.date_creation_spider,
            ScrapersData.user_last_update_spider, ScrapersData.date_last_update_spider,
            ScrapersData.type_template, ScrapersData.is_utc, ScrapersData.is_other_format,
            ScrapersData.str_format, ScrapersData.is_json,
            TaxonomyName.name, ScrapersData.cve_medio,
            FrequencySpider.crontab, FrequencySpider.description,
            TypeSpiders.name, DescriptionErrors.taxonomy, DescriptionErrors.description
        )
        .order_by(ScrapersData.id)
    )

    result = query.all()
    session.close()

    scrapy_commands = []
    path_spiders = f"{os.getenv("SCRAPERS_SPIDERS_PATH")}/gen_scrapy.txt"

    for element in result:

        data = {
            "scraper_id": element.scraper_id,
            "scraper_name": element.scraper_name,
            "scraper_medium_id": element.scraper_medium_id,
            "medium_name": element.medium_name,
            "scraper_status": element.scraper_status,
            "scraper_frequency": element.scraper_frequency,
            "scraper_frequency_description": element.frequency_description,
            "scraper_start_urls": element.scraper_start_urls,
            "scraper_allowed_domains": element.scraper_allowed_domains,
            "scraper_selector_sections": element.scraper_selector_sections,
            "scraper_selector_notes": element.scraper_selector_notes,
            "scraper_selector_publish_date": element.scraper_selector_publish_date,
            "scraper_selector_modified_date": element.scraper_selector_modified_date,
            "scraper_selector_title": element.scraper_selector_title,
            "scraper_selector_author": element.scraper_selector_author,
            "scraper_selector_content": element.scraper_selector_content,
            "scraper_attrs_titles": element.scraper_attrs_titles,
            "scraper_selector_remove_elements": element.scraper_selector_remove_elements,
            "scraper_regex_allow_domains": element.scraper_regex_allow_domains,
            "scraper_regex_deny_sections": element.scraper_regex_deny_sections,
            "scraper_limit_to_scrape": element.scraper_limit_to_scrape,
            "scraper_user_creator_spider": element.scraper_user_creator_spider,
            "scraper_date_creation_spider": element.scraper_date_creation_spider.strftime("%Y-%m-%d %H:%M:%S"),
            "scraper_user_last_update_spider": element.scraper_user_last_update_spider,
            "scraper_date_last_update_spider": element.scraper_date_last_update_spider.strftime("%Y-%m-%d %H:%M:%S"),
            "scraper_type_template": element.scraper_type_template,
            "scraper_is_utc": element.scraper_is_utc,
            "scraper_is_other_format": element.scraper_is_other_format,
            "scraper_str_format": element.scraper_str_format,
            "scraper_is_json": element.scraper_is_json,
            "scraper_description_errors_taxonomy": element.description_errors_taxonomy,
            "scraper_description_errors_description": element.description_errors_description
        }

        json_data = json.dumps(data, ensure_ascii=False)

        command = f"scrapy genspider -t ds_scrapy_file {element.scraper_name} {element.scraper_start_urls} '{json_data}'"
        scrapy_commands.append(command)

    scrapy_commands = list(set(scrapy_commands))
    print(len(scrapy_commands))

    with open(path_spiders, 'w') as f:
        for scraper in scrapy_commands:
            f.write(f"{scraper}\n")

except Exception as e:
    logger.error(f"Error al obtener los datos de la plantilla: {e}")