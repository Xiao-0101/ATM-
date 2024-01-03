from lib import common
from db import db_handler

shop_logger = common.get_logger(log_type='shop')


# 商品准备结算接口，判断是否满足支付要求，满足要求后调用银行支付接口
def shopping_interface(login_user,user_dict):
    # 计算消费总额
    cost = 0
    for price_number in user_dict['shop_car'].values():
        price, number = price_number
        cost += (price * number)
    # 导入银行接口
    from interface import bank_interface
    flag = bank_interface.pay_interface(login_user, cost)
    if flag:
        msg = f'用户{login_user}支付{cost}成功，准备发货'
        shop_logger.info(msg)
        return True, msg
    return False, '支付失败'


# 购物车添加接口
def add_shop_car_interface(choice, user_dict,shop_list):
    shop_name, shop_price, shop_count = shop_list[choice]
    # 加入购物车 --> 必须先将用户的购物车获取到，所以需要初始化
    # 判断用户选择的商品是否重复
    if shop_name in user_dict['shop_car']:
        # 添加商品数量
        user_dict['shop_car'][shop_name][1] += 1
    else:
        user_dict['shop_car'][shop_name] = [shop_price, 1]
    print(f'当前购物车：{user_dict["shop_car"]}')
    # 保存用户数据
    db_handler.save(user_dict)
    return True, '添加购物车成功'


def del_shop_car_interface(choice, user_dict, shopping_car, shop_list):
    shop_name, shop_price, shop_count = shop_list[choice]
    # 加入购物车 --> 必须先将用户的购物车获取到，所以需要初始化
    # 判断用户选择的商品是否重复
    if shop_name in shopping_car:
        # 添加商品数量
        shopping_car[shop_name][1] -= 1
    else:
        return False, f'{shop_name}并不在购物车中，无法删减'
    if user_dict['shop_car'][shop_name][1] == 0:
        del user_dict['shop_car'][shop_name]
    db_handler.save(user_dict)
    return True, '购物车删减商品成功'


# 删减库存数量接口
def del_count_shopping_interface(username):
    user_dict = db_handler.select(username)
    shop_list = db_handler.select_shop()
    for shop_name, price_number in user_dict['shop_car'].items():
        for index, shop in enumerate(shop_list):
            shop_list_name, shop_list_price, shop_count = shop
            if shop_name == shop_list_name:
                shop_count -= price_number[1]
                shop_list[int(index)][-1] = shop_count
    user_dict['shop_car'].clear()
    db_handler.save(user_dict)
    db_handler.save_shop(shop_list)
    return True, '库存减少，请管理员尽快补货'


def check_shop_car_interface(username):
    user_dic = db_handler.select(username)
    return user_dic.get('shop_car')
