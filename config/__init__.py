# -*- coding: utf-8 -*-
__author__ = 'puras'
__email__ = 'he@puras.me'

import os

def load_config():
    """加载配置类"""
    mode = os.environ.get('MODE')
    try:
        if mode == 'PROD':
            from .production import ProductionConfig
            return ProductionConfig
        elif mode == 'TEST':
            from .test import TestConfig
            return TestConfig
        else:
            from .developement import DevelopementConfig
            return DevelopementConfig
    except ImportError, e:
        from .default import Config
        return Config