# -*- coding: utf-8 -*-
__author__ = 'puras'
__email__ = 'he@puras.me'

from flask import render_template, Blueprint

bp = Blueprint('home', __name__)

@bp.route('/', methods=['GET'])
def index():
    """首页"""
    return render_template('home/index.html')