from db import db_handler
from lib import common

# 根据不同的接口类型传入不同的日志对象
user_logger = common.get_logger(log_type='user')


def register_interface(username, password, balance=15000):
    user_dic = db_handler.select(username)
    if user_dic:
        return False, '用户名已存在'
    if username == 'xiao' and password == '123':
        role = True
    else:
        role = False
    # 【3】获取注册需要验证的字符串
    code = common.get_code(6)
    code_input = input(f"请输入{code}验证注册： ").strip()
    if code_input.upper() != code.upper():
        return False, f'当前验证码输入错误!'
    # 加盐
    salt = common.get_code(4)
    # 对密码进行加密
    password = common.get_pwd_md5(data=password, salt=salt)
    bank_pwd = common.get_pwd_md5(data=None, salt=None)
    # 随机生成银行卡号
    bank_id = common.get_bank_id()
    user_dic = {
        'username': username,
        'password': password,
        'salt': salt,
        'bank_id': bank_id,
        'bank_pwd': bank_pwd,
        'balance': balance,
        'flow': [],
        'shop_car': {},
        'locked': False,
        'is_admin': role
    }
    # 保存数据
    db_handler.save(user_dic)
    # 记录日志
    msg = f'{username}注册成功！'
    user_logger.info(msg)
    return True, msg


def login_interface(username, password):
    user_dic = db_handler.select(username)
    # 若有冻结用户，则需要判断是否被锁定
    if user_dic:
        if user_dic.get('locked'):
            return False, '当前用户已被锁定'
        # 获取到旧密码
        old_password = user_dic.get('password')
        # 获取到旧密码加密时用到的盐
        salt = user_dic.get('salt')
        password = common.get_pwd_md5(data=password, salt=salt)
        if password == old_password:
            msg = f'用户{username}登陆成功'
            # info表示成功
            user_logger.info(msg)
            return True, msg
        else:
            msg = f'用户{username}密码错误'
            # warn表示失败
            user_logger.warn(msg)
            return False, msg
    return False, '用户不存在，请重新输入！'


def check_bal_interface(username):
    user_dic = db_handler.select(username)
    return user_dic['balance']
