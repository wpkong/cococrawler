# -*- coding:utf-8 -*-
import sys
import os
import argparse
from jinja2 import FileSystemLoader, Environment
import cococrawler
from cococrawler.config import get_project_config
import importlib

CRAWLER_PATH = 'crawlers'
PATH = os.path.dirname(os.path.abspath(cococrawler.__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, 'templates')),
    trim_blocks=False)


def make_class_name(name):
    if not (name[0].isalpha() or name[0] == '_'):
        raise RuntimeError('illegal class name')
    return name[0].upper() + name[1:] + 'Crawler'


def _create_project(project_name):
    for i in project_name:
        if not i.isalpha() and i.isdigit() and i == '_':
            raise RuntimeError('illegal project name')

    os.makedirs(project_name)
    os.chdir(project_name)
    with open('config.py', 'wb') as f:
        f.write(TEMPLATE_ENVIRONMENT.get_template('config.py').render())

    with open('items.py', 'wb') as f:
        f.write(TEMPLATE_ENVIRONMENT.get_template('items.py').render())

    with open('pipelines.py', 'wb') as f:
        f.write(TEMPLATE_ENVIRONMENT.get_template('pipelines.py').render())

    with open('sources.py', 'wb') as f:
        f.write(TEMPLATE_ENVIRONMENT.get_template('sources.py').render())

    if not os.path.exists(CRAWLER_PATH):
        os.makedirs(CRAWLER_PATH)
        os.system(r'touch %s' % os.path.join(CRAWLER_PATH, '__init__.py'))


def _create_crawler(crawler_name):
    class_name = make_class_name(crawler_name)

    if not os.path.exists(CRAWLER_PATH):
        os.makedirs(CRAWLER_PATH)
        os.system(r'touch %s' % os.path.join(CRAWLER_PATH, '__init__.py'))

    with open(os.path.join(CRAWLER_PATH, crawler_name + '.py'), 'wb') as f:
        f.write(TEMPLATE_ENVIRONMENT.get_template('crawler.py').render(
            {'crawler_name': crawler_name, 'class_name': class_name}))


def _run_crawler(crawler_name):
    crawler_config = get_project_config().CRAWLERS.get(crawler_name).split(':')
    class_name = crawler_config[1]
    module_path = crawler_config[0]
    sys.path.append(os.path.abspath('.'))
    modu = importlib.import_module(module_path)
    crawler = getattr(modu, class_name)()
    crawler.run()


def _print_command_help():
    help = '''
[command help]
[command] [target]

createproject        create a new pure cococrawler project named by target param.

createcrawler        create a new crawler from template.

runcralwer           run a crawler

        '''
    return help


def execute():
    arg = argparse.ArgumentParser(add_help=False)
    group = arg.add_argument_group('command')
    group.add_argument('operation')
    group.add_argument('target')
    arg.add_argument('-h', '--help', action='help', help=_print_command_help())

    args = arg.parse_args()

    if args.operation:
        command_name = args.operation
        if command_name == 'createproject':
            if args.target:
                project_name = args.target
                _create_project(project_name)
            else:
                print _print_command_help()

        elif command_name == 'createcrawler':
            # confirm that path in a project
            CONFIG = get_project_config()
            if args.target:
                crawler_name = args.target
                _create_crawler(crawler_name)
            else:
                print _print_command_help()

        elif command_name == 'runcrawler':
            CONFIG = get_project_config()

            if args.target:
                crawler_name = args.target
                if crawler_name not in CONFIG.CRAWLERS.keys():
                    raise RuntimeError('no such spider in configuration file: config.py')
                _run_crawler(crawler_name)
            else:
                print _print_command_help()

        else:
            print _print_command_help()
