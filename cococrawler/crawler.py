# -*- coding:utf-8 -*-
import requests
from cococrawler.piplines import Pipeline
from data_source import DataSource


class Crawler(object):
    name = 'Crawler'
    pipeline = Pipeline()
    source = DataSource()

    def get_url(self):
        for url in self.source:
            return url

    def request_url(self, url):
        res = requests.get(url)
        return res

    def parse(self, response):
        yield None

    def run(self):
        while True:
            _url = self.get_url()
            _res = self.request_url(_url)
            for item in self.parse(_res):
                self.pipeline.pour_out(item)
