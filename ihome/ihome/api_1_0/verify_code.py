# coding:utf-8

from . import api
from ihome.utils.captcha.captcha import captcha
from ihome import redis_store, constants, db
from ihome.utils.response_code import RET
from ihome.libs.yuntongxun.sms import CCP
from flask import current_app, jsonify, make_response, request
from ihome.models import User
import random
from ihome.task.task_sms import send_sms


@api.route("/get_image_code/<image_code_id>")
def get_image_code(image_code_id):
    """
    获取图片验证码
    :return:  right:验证码图片 error:json message
    """
    # 生成图片
    name, text, image_data = captcha.generate_captcha()
    # save code to redis
    try:
        redis_store.setex("image_code_%s" % image_code_id,
                          constants.IMAGE_CODE_REDIS_EXPIRES, text)
    except Exception as e:
        # 捕获异常
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="save image code failed")
    # return picture
    resp = make_response(image_data)
    resp.headers["Content-Type"] = "image/jpg"
    return resp


@api.route("/sms_codes/<re(r'1[34578]\d{9}'):mobile>")
def get_sms_code(mobile):
    """获取短信"""
    image_code = request.args.get("image_code")
    image_code_id = request.args.get("image_code_id")
    if not all([image_code, image_code_id]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")
    # 取出code校验
    try:
        real_image_code = redis_store.get("image_code_%s" % image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="redis error")
    if real_image_code is None:
        return jsonify(errno=RET.NODATA, errmsg="code older")
    # remove verification code
    try:
        redis_store.delete("image_code_%s" % image_code_id)
    except Exception as e:
        current_app.logger.error(e)
    if real_image_code.lower() != image_code.lower():
        return jsonify(errno=RET.DATAERR, errmsg="code error")
    # 判断是否发送过
    try:
        send_flag = redis_store.get("send_sms_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if send_flag is not None:
            return jsonify(errno=RET.REQERR, errmsg="time not achieve")
    # 判断手机号是否存在
    try:
        user = User.query.filter_by(mobile=mobile).firs()
    except Exception as e:
        current_app.logger.error(e)
    else:
        if user is not None:
            return jsonify(errno=RET.DATAEXIST, errmsg="mobile exist")
    # 生成短信验证码
    sms_code = "%06d" % random.randint(0, 999999)
    try:
        redis_store.setex("sms_code_%s" % mobile,
                          constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        #
        redis_store.setex("send_sms_%s" % mobile,
                          constants.SEND_SMS_CODE_INTERVAL, 1)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="save sms code error")
    # 发送短信西
    try:
        # ccp = CCP()
        # result = ccp.send_template_sms(mobile, [sms_code, int(constants.SMS_CODE_REDIS_EXPIRES / 60)], 1)
        send_sms.delay(
            mobile,
            [sms_code, int(constants.SMS_CODE_REDIS_EXPIRES / 60)], 1)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="send error")

    return jsonify(errno=RET.OK, errmsg="ok")
