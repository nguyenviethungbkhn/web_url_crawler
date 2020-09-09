from itemadapter import ItemAdapter
import json, codecs

class WebUrlPipeline(object):
    def __init__(self):
        self.items = []
        self.file = open('web_url_crawler/data/web_url.json', 'w') # open('items.json', 'w')

    def close_spider(self, spider):
        json.dump(self.items, self.file)
        self.file.close()

    def process_item(self, item, spider):            
        self.items.append(dict(item))
        return item

