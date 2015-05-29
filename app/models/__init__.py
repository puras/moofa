# -*- coding: utf-8 -*-
__author__ = 'puras'
__email__ = 'he@puras.me'

from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user_model import *