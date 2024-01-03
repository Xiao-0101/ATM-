from core import src
from interface import admin_interface



# 添加用户
def add_user():
    src.register()


# 修改用户额度
def change_balance():
    while True:
        change_user = input('请输入想要修改额度的用户名：').strip()
        money = input('请输入想要修改的用户额度：').strip()
        if not money.isdigit():
            continue
        flag, msg = admin_interface.change_balance_interface(change_user, money)
        if flag:
            print(msg)
            break
        else:
            print(msg)


# 修改用户账户状态
def lock_user():
    while True:
        change_user = input('请输入需要操作的账户用户名：').strip()
        flag, msg = admin_interface.lock_user_interface(change_user)
        if flag:
            print(msg)
            break
        else:
            print(msg)


# 修改用户权限
def change_admin():
    while True:
        change_user = input('请输入需要操作的账户用户名：').strip()
        if change_user == src.login_user:
            print('不能修改自己账户权限')
            break
        flag, msg = admin_interface.change_admin_interface(change_user)
        if flag:
            print(msg)
            break
        else:
            print(msg)


# 修改后台购物车商品信息
def change_goods():
    while True:
        from db import db_handler
        for index, shop in enumerate(db_handler.select_shop()):
            shop_name, shop_price, shop_count = shop
            print(f'商品编号为：{index}',
                  f'商品名称：{shop_name}',
                  f'商品单价：{shop_price}',
                  f'库存数量：{shop_count}')
        choice = input('请输入需要修改的商品编号：').strip()
        change_shop_name = input('请输入修改后的商品名称：').strip()
        change_shop_price = input('请输入修改后的商品价格：').strip()
        change_shop_count = input('请输入修改后的库存数量：').strip()
        change_shop_price = int(change_shop_price)
        change_shop_count = int(change_shop_count)
        flag, msg = admin_interface.change_goods_interface(choice, change_shop_name, change_shop_price,change_shop_count)
        if flag:
            print(msg)
            break
        else:
            print(msg)


# 添加后台商品信息
def add_goods():
    while True:
        new_shop_name = input('请输入添加的商品名字：').strip()
        new_shop_price = input('请输入添加的商品价格：').strip()
        new_shop_count = input('请输入添加的商品库存数量：').strip()
        new_shop_price = int(new_shop_price)
        new_shop_count = int(new_shop_count)
        flag, msg = admin_interface.add_goods_interface(new_shop_name, new_shop_price, new_shop_count)
        if flag:
            print(msg)
            break
        else:
            print(msg)
            choice = input('是否继续添加（q退出，任意键继续)：').strip()
            if choice == 'q':
                break
            else:
                continue


# 删除后台商品信息
def del_goods():
    while True:
        from db import db_handler
        for index, shop in enumerate(db_handler.select_shop()):
            shop_name, shop_price, shop_count= shop
            print(f'商品编号为：{index}',
                  f'商品名称：{shop_name}',
                  f'商品单价：{shop_price},'
                  f'库存数量：{shop_count}')
        choice = input('请输入需要删除的商品编号：').strip()
        flag, msg = admin_interface.del_goods_interface(choice)
        if flag:
            print(msg)
            break
        else:
            print(msg)


admin_func = {
    '1': add_user,
    '2': change_balance,
    '3': lock_user,
    '4': change_admin,
    '5': add_goods,
    '6': change_goods,
    '7': del_goods,
    'q': ''
}


def admin_run():
    while True:
        print('''
        1、添加账户
        2、修改用户额度
        3、冻结/解冻账户
        4、修改用户权限(管理员/普通用户)
        5、增加商品信息
        6、修改商品信息
        7、删除商品信息
        退出管理员功能请按q
        ''')
        choice = input('请输入管理员功能编号：').strip()
        if choice not in admin_func:
            print('请输入正确的功能编号!')
            continue
        if choice == 'q':
            print('再见,尊贵的管理员先生，欢迎下次使用！')
            break
        admin_func.get(choice)()
