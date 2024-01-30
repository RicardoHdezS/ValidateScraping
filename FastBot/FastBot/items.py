# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class FastbotItem(Item):

    identifier_scraping = Field()
    news_publication_date = Field()
    news_modified_date = Field()
    db_insert_date = Field()
    db_update_date = Field()
    news_url = Field()
    news_section = Field()
    news_head_title = Field()
    news_author = Field()
    news_content = Field()
    news_cve_medio = Field()
    news_media_id = Field()
    news_taxonomy_name = Field()
    scraping_error = Field()
