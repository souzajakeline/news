BOT_NAME = 'news_crawler'

SPIDER_MODULES = ['news_crawler.spiders']
NEWSPIDER_MODULE = 'news_crawler.spiders'

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'news_crawler.pipelines.JsonWriterPipeline': 1,
}
