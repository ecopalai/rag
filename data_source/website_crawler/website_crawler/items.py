# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WebsiteCrawlerItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    h1 = scrapy.Field()
    meta_description = scrapy.Field()
    meta_keywords = scrapy.Field()
    markdown_content = scrapy.Field()
    links_count = scrapy.Field()
