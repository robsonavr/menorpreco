# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MenorprecoPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        #field name: distance
        field_name = 'distance'
        value = adapter.get(field_name)
        value = value.strip('\xa0')
        adapter[field_name] = value

        #field name: period
        field_name = 'period'
        value = adapter.get(field_name)
        value = value.strip('há ')
        adapter[field_name] = value

        #field name: price
        field_name = 'price'
        value = adapter.get(field_name)
        value = value.strip('\xa0').replace(',','.')
        adapter[field_name] = float(value)
        
        return item
