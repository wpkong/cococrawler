# -*- coding:utf-8 -*-

#   {crawler_name: crawler_module: class_name}

CRAWLERS = {
    'test':'crawlers.test:class'
}

#   [requirements]
#   redis : host, port, db[default = 0], password[default None]
#   mongodb: host, port, db, collection

# [type options]
# redis, mongodb
DATABASES = {
    'database_name': {
        'type': 'redis',
        'host': 'localhost',
        'port': 0,
    },
}

# [type options]
# redis, file, mongodb

# [requirements]
# redis: database
# file: filename, fileformat
# mongodb: database

PIPELINES = {
    'pipeline_name': {
        'type': 'redis',
        'database':'database_name',
    },
}

# [type options]
# redis, queue

# [requirements]
# redis: database,key
# queue: None

SOURCES = {
    'source_name': {
        'type': 'redis',
        'database': 'database_name',
        'key': 'key_name'
    }
}