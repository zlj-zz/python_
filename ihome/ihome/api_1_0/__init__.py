# coding:utf-8

from flask import Blueprint

# create blueprint object
api = Blueprint('api_1_0', __name__)

from . import demo, verify_code, passport, profile, houses, orders, pay
