# -*- coding: utf-8 -*-
__author__ = 'puras'
__email__ = 'he@puras.me'

import os

class Config(object):
    """配置基类"""

    # Flask app config
    DEBUG = False
    TESTING = False
    SECRET_KEY = '@\x98\xbe:\x08\x8a\xcb%\xf3\xe1\xfb\xc2\xce\xd0\x10\xb6\x87X\xa3\x83\xcb-\r\x88'
    PERMANENT_SESSION_LIFETIME = 3600 * 24 * 7
    SESSION_COOKIE_NAME = '#{project}_session'

    # Root path of project
    PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Site domain
    # SITE_TITLE = '#{project}'
    # SITE_DOMAIN = 'http://localhost:5050'
    SITE_TITLE = '何求'
    SITE_DOMAIN = 'http://heqoo.com'
    VSITE_DOMAIN = 'http://heqoo.com/v/'

    # SQLAlchemy config
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/mooto'

    # Uploadsets config
    UPLOADS_DEFAULT_DEST = "%s/app/assets/uploads" % PROJECT_PATH  # 上传文件存储路径
    UPLOADS_DEFAULT_URL = "%s/assets/uploads/" % SITE_DOMAIN  # 上传文件访问URL

    # Theme path
    THEMES_PATH = "%s/app/assets/themes" % PROJECT_PATH