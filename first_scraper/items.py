# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from scrapy.item import Item, Field

class BookItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field()
    price = Field()
    product_description = Field()
    category = Field()
    upc = Field()
    product_type = Field()
    price_without_tax = Field()
    price_with_tax = Field()
    tax = Field()
    availability = Field()
    star_rating = Field()
