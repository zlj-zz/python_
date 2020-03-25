# coding:utf-8

from . import api
from flask import request, jsonify, current_app, session
from ihome import redis_store, db, constants
from ihome.utils.response_code import RET
from ihome.models import User
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
import re


@api.route("/sessions", methods=["POST"])
def login():
    """user login
    :param: mobile password
    :return:
    """
    req_dict = request.get_json()
    mobile = req_dict.get("mobile")
    pwd = req_dict.get("password")
    if not all([mobile, pwd]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")
    if not re.match(r'1[34578]\d{9}', mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="手机号码格式错误")
    user_ip = request.remote_addr
    try:
        access_num = redis_store.get("access_num_%s" % user_ip)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if access_num is not None and int(access_num) >= constants.LOGIN_ERROR_MAX_TIMES:
            return jsonify(errno=RET.REQERR, errmsg="次数过多，稍候")
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取用户信息失败")
    # 校验用户名和密码
    if user is None or not user.check_password(passwd=pwd):
        try:
            redis_store.incr("access_num_%s" % user_ip)
            redis_store.expire("access_num_%s" % user_ip, constants.LOGIN_ERROR_FORBID_TIMES)
        except Exception as e:
            current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg="用户名或密码错误")
    # 保存登录数据
    session["name"] = user.name
    session["mobile"] = user.mobile
    session["user_id"] = user.id
    return jsonify(errno=RET.OK, errmsg="ok")


@api.route("/session", methods=["GET"])
def check_login():
    """检查登录状态"""
    name = session.get("name")
    if name is not None:
        return jsonify(errno=RET.OK, errmsg="ok", data={"name": name})
    else:
        return jsonify(errno=RET.SESSIONERR, errmsg="false")


@api.route("/session", methods=["DELETE"])
def logout():
    """登出"""
    csrf_token = session.get("csrf_token")
    session.clear()
    session[""] = csrf_token
    return jsonify(errno=RET.OK, errmsg="ok")


@api.route("/users", methods=["POST"])
def register():
    """register

    :return:
    """
    req_dict = request.get_json()
    mobile = req_dict.get("mobile")
    sms_code = req_dict.get("sms_code")
    pwd = req_dict.get("password")
    pwd2 = req_dict.get("password2")
    # 数据是否完整
    if not all([mobile, sms_code, pwd]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")
    # 判断手机格式
    if not re.match(r"1[34578]\d{9}", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="手机格式错误")
    if pwd != pwd2:
        return jsonify(errno=RET.PARAMERR, errmsg="两次密码不一致")
    # 判断短信验证码是否正确
    try:
        real_sms_code = redis_store.get("sms_code_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="读取短信验证码异常")
    if real_sms_code is None:
        return jsonify(errno=RET.NODATA, errmsg="短信验证码失效")
    try:
        redis_store.delete("sms_code_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)
    # 验证码是否正确
    if real_sms_code != sms_code:
        return jsonify(errno=RET.DATAERR, errmsg="短信验证码错误")
    # 保存用户信息

    user = User(name=mobile, mobile=mobile)
    user.password = pwd
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="手机号存在")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库异常")
    # 保存登录数据
    session["name"] = mobile
    session["mobile"] = mobile
    session["user_id"] = user.id
    # return
    return jsonify(errno=RET.OK, errmsg="ok")
