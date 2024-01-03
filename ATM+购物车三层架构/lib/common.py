import hashlib
import os
import random
import logging.config
from conf import settings
from db import db_handler


# 随机生成验证码或盐
def get_code(n):
    code = ''
    for i in range(n):
        code_temp_list = [random.randint(0, 9),
                          chr(random.randint(65, 90)),
                          chr(random.randint(97, 122))]
        code += str(random.choice(code_temp_list))
    return code


# 随机生成银行卡号
def get_bank_id():
    bank_id = ''
    for i in range(6):
        bank_id += str(random.randint(0, 9))
    return bank_id


# 密码加密
def get_pwd_md5(data=None, salt=None):
    md5_obj = hashlib.md5()
    data = str(data) + str(salt)
    md5_obj.update(data.encode('utf8'))
    return md5_obj.hexdigest()


# 登录检测
def login_auth(func):
    from core import src

    def inner(*args, **kwargs):
        # 判断全局变量login_user是否为空
        if src.login_user:
            res = func(*args, **kwargs)
            return res
        else:
            print('未登录，无法使用功能')
            src.run()

    return inner


# 银行卡激活检测
def active_bank_card_auth(func):
    from core import src

    def inner(*args, **kwargs):
        user_dic = db_handler.select(src.login_user)
        if user_dic.get('bank_pwd') == get_pwd_md5(data=None, salt=None):
            print(f'当前银行卡未激活!')
            src.run()
        else:
            return func(*args, **kwargs)

    return inner


# 检测是否为管理员
def is_admin():
    from core import src
    user_dic = db_handler.select(src.login_user)
    if user_dic['is_admin'] is False:
        return False, f'{src.login_user}用户未获得管理员权限,请重新输入'
    return True, ''


# 添加日志功能(日志功能在接口层使用)
def get_logger(log_type):  # log_type --> user,bank
    '''
    :param  log_type:user日志，bank日志，购物商城日志
    :return:
    '''
    # 加载日志配置对象
    logging.config.dictConfig(settings.LOGGING_DIC)
    # 获取日志对象
    logger = logging.getLogger(log_type)
    return logger
