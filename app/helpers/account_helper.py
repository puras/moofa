# -*- coding: utf-8 -*-
__author__ = 'puras'
__email__ = 'he@puras.me'

from flask import session
from ..models import User


def current_user():
    """获取当前User，同时进行Session有效性的检测"""
    if not 'user_id' in session:
        return None
    user = User.query.filter(User.id == session['user_id']).first()
    if not user:
        # signout_user()
        return None
    return user