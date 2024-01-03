from db import db_handler
from lib import common

admin_logger = common.get_logger(log_type='admin')


def change_balance_interface(username, money):
    user_dic = db_handler.select(username)
    if user_dic:
        user_dic['balance'] = int(money)
        db_handler.save(user_dic)
        msg = f'管理员修改用户{username}额度修改成功'
        admin_logger.info(msg)
        return True, msg
    return False, '修改额度用户不存在'


def lock_user_interface(username):
    user_dic = db_handler.select(username)
    print(user_dic)
    if user_dic:
        if user_dic['locked'] is True:
            choice = input('该账户已冻结，请问是否解冻(输入y解冻)： ').strip()
            if choice == 'y':
                user_dic['locked'] = False
                db_handler.save(user_dic)
                msg = f'{username}已解冻'
                admin_logger.info(msg)
                return True, msg
        if user_dic['locked'] is False:
            choice = input('该账户未冻结，请问是否冻结(输入y冻结)： ').strip()
            if choice == 'y':
                user_dic['locked'] = True
                db_handler.save(user_dic)
                msg = f'用户{username}冻结成功'
                admin_logger.info(msg)
                return True, msg
        return False, '操作未成功，请重新输入'
    return False, '用户不存在'


def change_admin_interface(username):
    user_dic = db_handler.select(username)
    if user_dic:
        if user_dic['is_admin'] is True:
            choice = input('该账户为管理员账户，请问是否修改为普通用户(输入y修改)： ').strip()
            if choice == 'y':
                user_dic['is_admin'] = False
                db_handler.save(user_dic)
                msg = f'{username}已降为普通用户'
                admin_logger.info(msg)
                return True, msg
        if user_dic['is_admin'] is False:
            choice = input('该账户为普通用户，请问是否修改为管理员(输入y修改)： ').strip()
            if choice == 'y':
                user_dic['is_admin'] = True
                db_handler.save(user_dic)
                msg = f'用户{username}已升为管理员'
                admin_logger.info(msg)
                return True, msg
        return False, '操作未成功，请重新输入'
    return False, '用户不存在'


def change_goods_interface(choice, change_shop_name, change_shop_price,change_shop_count):
    shop_list = db_handler.select_shop()
    if shop_list:
        if not choice.isdigit():
            return False, '商品编号格式错误'
        choice = int(choice)
        if choice not in range(len(shop_list)):
            return False, '请输入正确的商品编号'
        # 弹出索引位置的值
        shop_list.pop(choice)
        # 将修改的值插入该索引位置
        shop_list.insert(choice, [change_shop_name, change_shop_price, change_shop_count])
        db_handler.save_shop(shop_list)
        msg = f'商店商品已更新'
        admin_logger.info(msg)
        return True, msg
    return False, '商城无商品，请先添加商品'


def add_goods_interface(new_shop_name, new_shop_price, new_shop_count):
    shop_list = db_handler.select_shop()
    for shop in shop_list:
        if new_shop_name in shop[0]:
            return False, f'{new_shop_name}商品已存在，请勿重复添加！'
    shop_list.append([new_shop_name, new_shop_price, new_shop_count])
    db_handler.save_shop(shop_list)
    msg = '商品添加成功！'
    admin_logger.info(msg)
    return True, msg


def del_goods_interface(choice):
    shop_list = db_handler.select_shop()
    if shop_list:
        if not choice.isdigit():
            return False, '商品编号格式错误'
        choice = int(choice)
        if choice not in range(len(shop_list)):
            return False, '请输入正确的商品编号'
        # 弹出索引位置的值 == 删除
        shop_list.pop(choice)
        db_handler.save_shop(shop_list)
        msg = f'商品删除成功'
        admin_logger.info(msg)
        return True, msg
    return False, '商城无商品，请先添加商品'
