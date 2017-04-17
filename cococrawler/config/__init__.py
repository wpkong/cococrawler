# -*- coding:utf-8 -*-
import sys
import importlib
import os


def get_project_config():
    sys.path.append(os.path.abspath('.'))
    config = importlib.import_module('config')
    return config