# -*- coding:utf-8 -*-
import redis
import items
import json
from cococrawler.config import get_project_config
from pymongo import MongoClient


class Pipeline(object):
    def pour_out(self, data):
        if not isinstance(data, items.Item):
            raise RuntimeError('Bad data type!')


class RedisPipeline(Pipeline):

    def __init__(self, pipename):
        config = get_project_config()
        setting = config.PIPELINES.get(pipename)
        if setting is None or setting.get('type') != 'redis':
            raise RuntimeError('Bad setting on Pipeline')
        db_name = setting.get('database')
        db_setting = config.DATABASES.get(db_name)
        if db_setting is None or db_setting.get('type') != 'redis':
            raise RuntimeError('Bad setting on Pipeline')

        host = db_setting.get('host')
        port = db_setting.get('port')
        db = db_setting.get('db')
        password = db_setting.get('password')
        self.client = redis.Redis(host=host, port=port, db=db, password=password)

    def pour_out(self, data):
        Pipeline.pour_out(self, data)
        for k, v in data.items():
            self.client.sadd(k, v)


class MongodbPipeline(Pipeline):
    def __init__(self,pipename):
        config = get_project_config()
        setting = config.PIPELINES.get(pipename)
        if setting is None or setting.get('type') != 'mongodb':
            raise RuntimeError('Bad settings on Pipeline')
        db_name = setting.get('database')
        db_setting = config.DATABASES.get(db_name)
        if db_setting is None or db_setting.get('type') != 'mongodb':
            raise RuntimeError('Bad setting on Pipeline')

        host = db_setting.get('host')
        port = db_setting.get('port')
        db = db_setting.get('db')
        collection = db_setting.get('collection')
        client = MongoClient(host=host,port=port)
        self.db = client[db]
        self.collection = self.db[collection]

    def pour_out(self, data):
        Pipeline.pour_out(self,data)
        self.collection.insert(data)


class FilePipeline(Pipeline):
    def __init__(self, pipename):
        config = get_project_config()
        setting = config.PIPELINES.get(pipename)
        if setting is None or setting.get('type') != 'mongodb':
            raise RuntimeError('Bad settings on Pipeline')

        self.filename = setting.get('filename')
        self.fileFormat = setting.get('fileFormat')
        self.file = open('.'.join([self.filename,self.fileFormat]), 'wb')

    def __del__(self):
        self.file.close()

    def pour_out(self, data):
        Pipeline.pour_out(self, data)
        self.file.write(json.dumps(data,ensure_ascii=False) + '\n')
        self.file.flush()
