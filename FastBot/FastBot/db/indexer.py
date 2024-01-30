from dotenv import load_dotenv
from ..utils.logger import logger
import os
from .alchemy_connector import PostgreSQLDBConnection
from ..data.models.scrapers import (ScrapersData, TaxonomyName,
                                    TypeSpiders, FrequencySpider)
from ..data.models.errors import ScrapingErrors
from datetime import timedelta
from sqlalchemy import update, insert

load_dotenv()

class ScrapersConnector:

    def get_connection(self):

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

class ScrapersTemplate:


    def get_template_data(self, cve_medio, status):

            try:

                query = (
                    session.query(
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
                        ScrapersData.str_format, ScrapersData.is_json
                    )
                    .join(TaxonomyName, ScrapersData.cve_medio == TaxonomyName.id)
                    .filter(ScrapersData.cve_medio == cve_medio)
                    .filter(ScrapersData.status == status)
                )

                result = query.all()
                session.close()
                return result[0]

            except Exception as e:
                logger.error(f"Error al obtener los datos de la plantilla: {e}")

class GetScrapingErrors:

    session = ScrapersConnector().get_connection()
    def get_error_data(self, date_error, type_error, scraper_file):
            try:

                since = date_error.replace(hour=0, minute=0, second=0, microsecond=0)
                until = since + timedelta(days=1) - timedelta(microseconds=1)

                query = (
                    session.query(
                        ScrapingErrors.date_error, ScrapingErrors.status,
                        ScrapingErrors.type_error, ScrapingErrors.scraper_file,
                        ScrapingErrors.url_list
                    )
                    .filter(ScrapingErrors.type_error == type_error)
                    .filter(ScrapingErrors.scraper_file == scraper_file)
                    .filter(ScrapingErrors.status == 1)
                    .filter(ScrapingErrors.date_error >= since)
                    .filter(ScrapingErrors.date_error <= until)
                )

                result = query.all()

                session.close()
                return result[0]

            except Exception as e:
                logger.error(f"Error al obtener los datos de la plantilla: {e}")

    def insert_error(self, item):
        try:
            values = {
                'date_error': item['error']['scraping']['date'],
                'status': 1,
                'type_error': item['error']['scraping']['type'],
                'scraper_file': item['error']['scraping']['spider'],
                'url_list': [item['error']['scraping']['url']]
            }

            insert_error = insert(ScrapingErrors).values(values)

            session.execute(insert_error)
            session.commit()

            session.close()
            return True

        except Exception as e:
            logger.error(f"Error al insertar el error: {e}")
            return False

    def update_error(self, values, fields):
        try:
            since = fields['date_error'].replace(hour=0, minute=0, second=0, microsecond=0)
            until = since + timedelta(days=1) - timedelta(microseconds=1)

            update_error = (
                update(ScrapingErrors)
                .values(values)
                .where(
                    (ScrapingErrors.date_error >= since) &
                    (ScrapingErrors.date_error <= until) &
                    (ScrapingErrors.type_error == fields['type_error']) &
                    (ScrapingErrors.scraper_file == fields['scraper_file'])
                )
            )

            session.execute(update_error)
            session.commit()

            session.close()
            return True

        except Exception as e:
            logger.error(f"Error al insertar el error: {e}")
            return False

class CrontabManager:

    session = ScrapersConnector().get_connection()

    def get_crontab_add_spider(self):
        try:
            query = (
                session.query(
                    ScrapersData.id.label('scraper_id'), ScrapersData.name.label('scraper_name'), ScrapersData.cve_medio,
                    ScrapersData.status, ScrapersData.frequency, ScrapersData.type_template,
                    TypeSpiders.name, TypeSpiders.description, TypeSpiders.command,
                    FrequencySpider.id, FrequencySpider.crontab, FrequencySpider.description
                )
                .join(TypeSpiders, ScrapersData.type_template == TypeSpiders.id)
                .join(FrequencySpider, ScrapersData.frequency == FrequencySpider.id)
                .filter(ScrapersData.status == 1)
                .order_by(ScrapersData.id)
            )

            result = query.all()
            session.close()

            return result

        except Exception as e:
            logger.error("Error in get_crontab_manager: %s", e)

