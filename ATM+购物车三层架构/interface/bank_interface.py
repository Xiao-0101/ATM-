from db import db_handler
from lib import common

bank_logger = common.get_logger(log_type='bank')


def active_bank_card_interface(username, bank_pwd):
    user_dic = db_handler.select(username)
    salt = user_dic['salt']
    # 对密码进行加密
    bank_pwd = common.get_pwd_md5(data=bank_pwd, salt=salt)
    user_dic['bank_pwd'] = bank_pwd
    db_handler.save(user_dic)
    msg = f'{username}银行卡激活成功'
    bank_logger.info(msg)
    return True, msg


def withdraw_interface(username, money, bank_pwd):
    user_dic = db_handler.select(username)
    old_bank_pwd = user_dic.get('bank_pwd')
    # 获取到旧密码加密时用到的盐
    salt = user_dic.get('salt')
    bank_pwd = common.get_pwd_md5(data=bank_pwd, salt=salt)
    if old_bank_pwd != bank_pwd:
        return False, '支付密码错误'
    balance = int(user_dic.get('balance'))
    money2 = int(money) * 1.05
    if balance >= money2:
        balance -= money2
        user_dic['balance'] = balance
        flow = f'用户{username} 提现金额【{money}】成功，手续费为【{money2 - float(money)}】'
        user_dic['flow'].append(flow)
        db_handler.save(user_dic)
        bank_logger.info(flow)
        return True, flow
    return False, '提现金额不足，请重新输入'


def repay_interface(username, money):
    user_dic = db_handler.select(username)
    # user_dic['balance']本来就是int
    user_dic['balance'] += money
    flow = f'用户【{username}】 存款【{money}】成功，当前额度为{user_dic["balance"]}'
    user_dic['flow'].append(flow)
    db_handler.save(user_dic)
    bank_logger.info(flow)
    return True, flow


def transfer_interface(login_user, to_user, money, bank_pwd, to_bank_id):
    login_user_dic = db_handler.select(login_user)
    # 比对加密的密码
    old_bank_pwd = login_user_dic.get('bank_pwd')
    # 获取到旧密码加密时用到的盐
    salt = login_user_dic.get('salt')
    bank_pwd = common.get_pwd_md5(data=bank_pwd, salt=salt)
    if old_bank_pwd != bank_pwd:
        return False, '支付密码错误'
    # 读取对方账户
    to_user_dic = db_handler.select(to_user)
    if not to_user_dic:
        return False, '目标用户不存在'
    if to_bank_id != to_user_dic.get('bank_id'):
        return False, '目标用户并未有此银行卡'
    if login_user_dic['balance'] >= money:
        login_user_dic['balance'] -= money
        to_user_dic['balance'] += money
        login_user_flow = f'用户{login_user} 给用户 {to_user}转账{money}成功'
        login_user_dic['flow'].append(login_user_flow)
        bank_logger.info(login_user_flow)
        to_user_flow = f'用户{to_user} 接收用户 {login_user}转账{money}成功'
        to_user_dic['flow'].append(to_user_flow)
        bank_logger.info(to_user_flow)
        db_handler.save(login_user_dic)
        db_handler.save(to_user_dic)
        return True, login_user_flow
    return False, '当前用户转账金额不足'


def check_flow_interface(login_user):
    user_dic = db_handler.select(login_user)
    return user_dic


def pay_interface(login_user, cost):
    user_dict = db_handler.select(login_user)
    if user_dict.get('balance') >= cost:
        user_dict['balance'] -= cost
        # 记录消费流水
        flow = f'用户消费金额：{cost}'
        user_dict['flow'].append(flow)
        # 保存数据
        db_handler.save(user_dict)
        bank_logger.info(flow)
        # return的值交给购物接口来做处理
        return True
    return False
