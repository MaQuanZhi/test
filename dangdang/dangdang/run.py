from scrapy import cmdline

cmdline.execute('scrapy crawl spider1 -s LOG_ENABLED=False'.split())
