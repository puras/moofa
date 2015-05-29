# -*- coding: utf-8 -*-
__author__ = 'puras'
__email__ = 'he@puras.me'

import sys
import os

import hashlib
from flask import Flask, request, url_for, render_template, g
from werkzeug.contrib.fixers import ProxyFix
from config import load_config
import logging
import time

reload(sys)
sys.setdefaultencoding('utf8')

def create_app():
    """创建Flask App"""
    app = Flask(__name__, static_folder='assets')

    config = load_config()
    app.config.from_object(config)

    # Logger
    app.logger.setLevel(logging.DEBUG)
    app.logger.disabled = False
    handler = logging.FileHandler('moovo.log')
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s: \t%(message)s")
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    # Proxy Fix
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # CSRF protect

    # 注册组件
    register_db(app)
    register_routes(app)
    register_jinja(app)
    register_error_handle(app)
    regiter_uploadsets(app)
    register_hooks(app)

    return app

def register_db(app):
    """注册Model"""
    from .models import db
    db.init_app(app)

def register_routes(app):
    """注册路由"""
    from .controllers import home_controller

    app.register_blueprint(home_controller.bp, url_prefix='')

def register_jinja(app):
    """注册模板全局变量和全局函数"""
    from jinja2 import Markup
    from .utils import filters

    if not hasattr(app, '_static_hash'):
        app._static_hash = {}

    app.jinja_env.filters['timesince'] = filters.timesince

    # inject vars into template context
    @app.context_processor
    def inject_vars():
        return dict()

    def url_for_other_page(page):
        """Generate url for pagination"""
        view_args = request.view_args.copy()
        args = request.args.copy().to_dict()
        combined_args = dict(view_args.items() + args.items())
        combined_args['page'] = page
        return url_for(request.endpoint, **combined_args)

    def static(filename):
        """静态资源URL
        计算资源内容Hash作为Query String，并缓存起来"""
        url = url_for('static', filename=filename)
        if app.testing:
            return url

        if filename in app._static_hash:
            return app._static_hash[filename]

        path = os.path.join(app.static_folder, filename)
        if not os.path.exists(path):
            return url

        with open(path, 'r') as f:
            content = f.read()
            hash = hashlib.md5(content).hexdigest()

        url = '%s?v=%s' % (url, hash[:10])
        app._static_hash[filename] = url
        return url

    def script(path):
        """Script标签"""
        return Markup('<script type="text/javascript" src="%s"></script>' % static(path))

    def link(path):
        return Markup('<link rel="stylesheet" href="%s">' % static(path))

    def theme_screens(template_name):
        path = os.path.join(app.config['THEMES_PATH'], template_name)
        screen_ext = ['.jpeg', '.jpg', '.png']
        file_list = os.listdir(path)
        screens = []
        for f in file_list:
            fn, ext = os.path.splitext(f)
            if ext in screen_ext and fn.find('screen_') == 0:
                screens.append(f)

        return screens

    app.jinja_env.globals['url_for_other_page'] = url_for_other_page
    app.jinja_env.globals['static'] = static
    app.jinja_env.globals['script'] = script
    app.jinja_env.globals['link'] = link
    app.jinja_env.globals['theme_screens'] = theme_screens


def register_error_handle(app):
    """注册HTTP错误页面"""

    @app.errorhandler(403)
    def page_403(error):
        return render_template('error/403.html'), 403

    @app.errorhandler(404)
    def page_404(error):
        return render_template('error/404.html'), 404

    @app.errorhandler(500)
    def page_500(error):
        return render_template('error/500.html'), 500

def regiter_uploadsets(app):
    """注册UploadSets"""
    pass


def register_hooks(app):
    """注册Hooks"""
    from .helpers.account_helper import current_user

    @app.before_request
    def before_request():
        g.user = current_user()
        if g.user:
            g._before_request_time = time.time()

    @app.after_request
    def after_request(response):
        if hasattr(g, '_before_request_time'):
            delta = time.time() - g._before_request_time
            response.headers['X-Render-Time'] = delta * 1000
            print "Load time %.4f" % (delta * 1000)
        return response