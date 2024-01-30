# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import requests

from .utils.logger import logger
# useful for handling different item types with a single interface
from dotenv import load_dotenv
import os
from .db.indexer import GetScrapingErrors
from collections import OrderedDict
load_dotenv()


class WebNotesPipeline:
    def process_item(self, item, spider):

        if spider.stop_flag:
            item['scraping_error'] = spider.scraping_element_error
            return item['scraping_error']

        logger.info("Enviando datos a API")
        send_data = self.sending_data(dict(item))
        try:
            if send_data.status_code == 200:
                logger.info("Datos enviados correctamente")
                return 200
        except:
            logger.error("Error al enviar datos a API")
            return 666
        # return item

    def sending_data(self, data):
        API_URI = os.getenv("API_HOST")
        API_PORT = os.getenv("API_PORT")
        API_ENDPOINT = os.getenv("API_ENDPOINT")
        try:
            logger.info("Enviando datos a API")
            send_request = requests.post(f"http://{API_URI}:{API_PORT}/{API_ENDPOINT}", json=data)

            return send_request

        except Exception as e:
            return 666


class WebNotesErrorPipeline:
    def process_item(self, item, spider):
        if spider.stop_flag == False:
            return item

        errors = GetScrapingErrors()
        date_error = item['error']['scraping']['date']
        type_error = item['error']['scraping']['type']
        scraper_file = item['error']['scraping']['spider']
        url_to_attach = item['error']['scraping']['url']

        data = errors.get_error_data(date_error, type_error, scraper_file)

        if data:

            self.update_error = ''

            if type_error == 1 or type_error > 10:

                values = {
                    'date_update_error': date_error
                }

                fields = {
                    'date_error': date_error,
                    'type_error': type_error,
                    'scraper_file': scraper_file
                }

                self.update_error = errors.update_error(values, fields)

            else:
                if url_to_attach in data.url_list:
                    logger.info("URL ya existe en la lista")
                else:
                    data.url_list.append(url_to_attach)

                    values = {
                        'date_update_error': date_error,
                        'url_list': list(OrderedDict.fromkeys(set(data.url_list)))
                    }

                    fields = {
                        'date_error': date_error,
                        'type_error': type_error,
                        'scraper_file': scraper_file
                    }

                    self.update_error = errors.update_error(values, fields)

            if self.update_error:

                logger.info("Error actualizado correctamente")
            else:
                logger.error("Error al actualizar el error")


        else:
            new_error = errors.insert_error(item)
            if new_error:
                logger.info("Error insertado correctamente")
            else:
                logger.error("Error al insertar el error")
