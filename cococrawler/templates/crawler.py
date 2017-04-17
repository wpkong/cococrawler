# -*- coding:utf-8 -*-
from cococrawler.crawler import Crawler
from cococrawler.piplines import Pipeline
from cococrawler.data_source import DataSource


class {{ class_name }}(Crawler):
    name = '{{ crawler_name }}'
    pipeline = Pipeline()
    source = DataSource()

    def parse(self, response):
        # write your code here
        pass