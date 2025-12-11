# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

class FirstScraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()

        for field_name in field_names:
            if field_name != 'product_description':
               value = adapter.get(field_name)
               if type(value) == str:
                    adapter[field_name] = value.strip()

        price_keys = ['price', 'price_without_tax', 'price_with_tax','tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            if type(value) == str:
                value = value.replace("£","")
                adapter[price_key] = float(value)
        return item

