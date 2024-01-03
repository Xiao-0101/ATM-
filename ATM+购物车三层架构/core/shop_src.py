from core import src
from interface import shop_interface
from db import db_handler


# 添加购物车商品信息
def add_shop_goods():
    # 初始化购物车
    while True:
        # 枚举： enumerate（可迭代对象）--> （可迭代对象的索引，索引对应的值）
        user_dict = db_handler.select(src.login_user)
        shopping_car = user_dict['shop_car']
        print(f'后台购物车信息：{shopping_car}')
        # 获取当前商品商城的数据
        shop_list = db_handler.select_shop()
        # 枚举： enumerate（可迭代对象）--> （可迭代对象的索引，索引对应的值）
        for index, shop in enumerate(shop_list):
            shop_name, shop_price, shop_count = shop
            print(f'商品编号为：{index}',
                  f'商品名称：{shop_name}',
                  f'商品单价：{shop_price}',
                  f'库存数量：{shop_count}')
        choice = input('请输入需要添加的商品编号(退出按q)：').strip()
        if choice == 'q':
            break
        if not choice.isdigit():
            print('商品编号格式错误')
            continue
        choice = int(choice)
        if choice not in range(len(shop_list)):
            print('请输入正确的商品编号')
            continue
        # 调用添加购物车中的商品信息接口
        flag, msg = shop_interface.add_shop_car_interface(choice, user_dict, shop_list)
        if flag:
            print(msg)
            continue
        else:
            print(msg)
            continue


# 删减购物车商品信息
def del_shop_goods():
    while True:
        # 获取当前用户的数据
        user_dict = db_handler.select(src.login_user)
        shopping_car = user_dict['shop_car']
        print(f'后台购物车信息：{shopping_car}')
        # 获取当前商品商城的数据
        shop_list = db_handler.select_shop()
        # 枚举： enumerate（可迭代对象）--> （可迭代对象的索引，索引对应的值）
        for index, shop in enumerate(shop_list):
            shop_name, shop_price, shop_count = shop
            print(f'商品编号为：{index}',
                  f'商品名称：{shop_name}',
                  f'商品单价：{shop_price}',
                  f'库存数量：{shop_count}')
        choice = input('请输入需要删减的商品编号(退出按q)：').strip()
        if choice == 'q':
            break
        if not choice.isdigit():
            print('商品编号格式错误')
            continue
        choice = int(choice)
        if choice not in range(len(shop_list)):
            print('请输入正确的商品编号')
            continue
        # 调用删减购物车中的商品信息接口
        flag, msg = shop_interface.del_shop_car_interface(choice, user_dict, shopping_car, shop_list)
        if flag:
            print(msg)
            continue
        else:
            print(msg)
            continue


def charge():
    user_dict = db_handler.select(src.login_user)
    # 判断当前的购物车是否为空，为空则不能支付
    if not user_dict['shop_car']:
        return False, '当前购物车为空，没有商品可以支付，请选择添加商品或者退出'
    # 调用支付接口
    flag, msg = shop_interface.shopping_interface(src.login_user, user_dict)
    # 支付成功，减少购物商城里的库存数量
    if flag:
        print(msg)
        # 调用减少商品库存数量接口
        flag, msg = shop_interface.del_count_shopping_interface(src.login_user)
        if flag:
            print(msg)
        else:
            print(msg)
        # user_dict['shop_car'].clear()
        # shop_list = db_handler.select_shop()
        # for shop_name, price_number in shopping_car.items():
        #     for index, shop in enumerate(shop_list):
        #         shop_list_name, shop_list_price, shop_count = shop
        #         if shop_name == shop_list_name:
        #             shop_count -= price_number[1]
        #             shop_list[int(index)][-1] = shop_count
        # db_handler.save(user_dict)
        # db_handler.save_shop(shop_list)
    else:
        print(msg)


shop_func = {
    '1': add_shop_goods,
    '2': del_shop_goods,
    '3': charge,
    'q': ''
}


def shop_run():
    while True:
        print('''
        1、添加商品
        2、删减商品
        3、结账
        退出购物车功能请按q
        ''')
        choice = input('请输入购物车功能编号：').strip()
        if choice not in shop_func:
            print('请输入正确的功能编号!')
            continue
        if choice == 'q':
            print('再见，欢迎下次使用！')
            break
        shop_func.get(choice)()
