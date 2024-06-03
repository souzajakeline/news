import json
import os
import subprocess

class JsonWriterPipeline:

    def open_spider(self, spider):
        # Open a file in write mode with UTF-8 encoding to store the scraped articles
        self.file = open('articles_utf8.json', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()
        # Call the script to upload JSON to BigQuery
        subprocess.run(["python", "news_crawler/upload_to_bq.py"])

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

