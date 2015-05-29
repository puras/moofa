# -*- coding: utf-8 -*-
__author__ = 'puras'
__email__ = 'he@puras.me'

from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(db.Model):
    __tablename__ = 'mk_users'

    id = db.Column(db.Integer, primary_key=True)