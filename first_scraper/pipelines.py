# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
from first_scraper.items import BookItem

logger = logging.getLogger(__name__)
class FirstScraperPipeline:

    def process_item(self, item: BookItem, spider):
        logger.info("process_item started")

        adapter = ItemAdapter(item)
        if adapter != None:
            logger.info("itemAdapter created")

        field_names = adapter.field_names()
        if field_names != None:
            logger.info("fieldnames not empty")
            #for field_name in field_names:
            #    logger.debug(adapter.get(field_name))

        for field_name in field_names:
            if field_name != 'product_description':
                valueStr = str(adapter.get(field_name))
                logger.debug(valueStr)
                logger.debug(type(valueStr))
                if type(valueStr) == str:
                    valueStr = valueStr.strip()
                    valueStr = valueStr.replace(",","")
                    valueStr = valueStr.replace("'","")
                    valueStr = valueStr.replace("(","")
                    valueStr = valueStr.replace(")","")
                    adapter[field_name] = valueStr
                    logger.info("value stripped")

        price_keys = ['price', 'price_without_tax', 'price_with_tax','tax']
        for price_key in price_keys:
            valueStr = str(adapter.get(price_key))
            if type(valueStr) == str:
                valueStr = valueStr.replace("£","")
                logger.info("number cleaned")
                logger.debug(valueStr)
                adapter[price_key] = float(valueStr)

        star_ratings = ['star_rating']
        for star_rating in star_ratings:
            stars = str(adapter.get(star_rating))
            stars = stars.split()
            stars = stars[1]
            if stars == "Zero":
                adapter[star_rating] = int(0)
            if stars == "One":
                adapter[star_rating] = int(1)
            if stars == "Two":
                adapter[star_rating] = int(2)
            if stars == "Three":
                adapter[star_rating] = int(3)
            if stars == "Four":
                adapter[star_rating] = int(4)
            if stars == "Five":
                adapter[star_rating] = int(5)

        availabilitys = ['availability']
        for availability in availabilitys:
            in_stock = str(adapter.get(availability))
            in_stock = in_stock.split()
            in_stock = in_stock[2]
            in_stock = int(in_stock)
            adapter[availability] = in_stock

        return item
