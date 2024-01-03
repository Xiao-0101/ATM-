"""
第一层：用户视图层
用户能实现的功能
"""

from interface import user_interface
from interface import bank_interface
from interface import shop_interface
from lib import common

login_user = None  # 登陆成功代表login_user = username


# 用户注册
def register():
    while True:
        username = input('请输入用户名:').strip()
        password = input('请输入密码：').strip()
        re_password = input('请确认密码：').strip()
        if password == re_password:
            flag, msg = user_interface.register_interface(username, password)
            if flag:
                print(msg)
                break
            else:
                print(msg)
        print('两次密码不相同，请重新输入')
        break


# 用户登录
def login():
    while True:
        username = input('请输入用户名:').strip()
        password = input('请输入密码：').strip()
        flag, msg = user_interface.login_interface(username, password)
        if flag:
            print(msg)
            # 给用户记录，已登录
            global login_user
            login_user = username
            break
        else:
            print(msg)
        break


# 激活银行卡
@common.login_auth
def active_bank_card():
    while True:
        bank_pwd = input('请设置你的银行卡密码：').strip()
        re_bank_pwd = input('请确认密码：').strip()
        if bank_pwd == re_bank_pwd:
            flag, msg = bank_interface.active_bank_card_interface(login_user, bank_pwd)
            if flag:
                print(msg)
                break
            else:
                print(msg)


# 检查余额
@common.login_auth
@common.active_bank_card_auth
def check_balance():
    balance = user_interface.check_bal_interface(login_user)  # username
    print(f'用户{login_user} 账户余额为： {balance}')


# 取款
@common.login_auth
@common.active_bank_card_auth
def withdraw():
    while True:
        input_money = input('请输入提现金额：').strip()
        input_bank_pwd = input('请输入支付密码：').strip()
        if not (input_money.isdigit() and input_bank_pwd):
            print('金额或密码输入格式非法，请重新输入')
            continue
        flag, msg = bank_interface.withdraw_interface(login_user, input_money, input_bank_pwd)
        if flag:
            print(msg)
            break
        else:
            print(msg)


# 存钱
@common.login_auth
@common.active_bank_card_auth
def repay():
    while True:
        input_money = input('请输入存款金额：').strip()
        if not input_money.isdigit():
            print('请输入正确的金额：')
            continue
        input_money = int(input_money)
        if input_money > 0:
            flag, msg = bank_interface.repay_interface(login_user, input_money)
            if flag:
                print(msg)
                break
        else:
            print('输入的金额不能小于0 ')


# 转账
@common.login_auth
@common.active_bank_card_auth
def transfer():
    while True:
        to_bank_id = input('请输入转账目标银行卡号：').strip()
        to_user = input('请输入转账目标用户：').strip()
        money = input('请输入转账金额：').strip()
        bank_pwd = input('请输入支付密码：').strip()
        if not (money.isdigit() and bank_pwd.isdigit()):
            print('输入金额格式非法！请重新输入')
            continue
        money = int(money)
        if money > 0:
            flag, msg = bank_interface.transfer_interface(login_user, to_user, money, bank_pwd,
                                                          to_bank_id)
            if flag:
                print(msg)
                break
            else:
                print(msg)
        else:
            print('请输入正确的金额：')


# 检查流水
@common.login_auth
@common.active_bank_card_auth
def check_flow():
    flow_list = bank_interface.check_flow_interface(login_user)
    if flow_list:
        for flow in flow_list['flow']:
            print(flow)
    else:
        print('当前用户没有流水')


# 购物功能
@common.login_auth
@common.active_bank_card_auth
def shopping():
    from core import shop_src
    shop_src.shop_run()


# 查看购物车
@common.login_auth
@common.active_bank_card_auth
def check_shop_car():
    shop_car = shop_interface.check_shop_car_interface(login_user)
    print(shop_car)


# 管理员功能
def admin():
    flag, msg = common.is_admin()
    if not flag:
        print(msg)
        return flag, msg
    from core import admin_src
    admin_src.admin_run()


func_dic = {
    '1': register,
    '2': login,
    '3': active_bank_card,
    '4': check_balance,
    '5': withdraw,
    '6': repay,
    '7': transfer,
    '8': check_flow,
    '9': shopping,
    '10': check_shop_car,
    '11': admin,
    'q': ''
}


def run():
    while True:
        print('''
        1、注册功能
        2、登录功能
        3、激活银行卡
        4、查看余额
        5、提现功能
        6、存款功能
        7、转账功能
        8、查看流水
        9、购物功能
        10、查看购物车
        11、管理员功能
        退出系统请按q
        ''')
        choice = input('请输入功能编号：').strip()
        if choice not in func_dic:
            print('请输入正确的编号')
            continue
        if choice == 'q':
            print('感谢使用本系统，欢迎下次使用！')
            break
        func_dic.get(choice)()  # func_dic.get('1')() --> register()
