import os
import logging
import logging.config
import sys

# 获取当前根目录路径
BASE_PATH = os.path.dirname(os.path.dirname(__file__))

# 获取user_data文件夹目录路径
USER_DATA_PATH = os.path.join(BASE_PATH, 'db', 'user_data')
SHOP_CAR_DATA_PATH = os.path.join(BASE_PATH, 'db', 'shop_mall_data')

# 自定义日志级别
CONSOLE_LOG_LEVEL = "INFO"
FILE_LOG_LEVEL = "DEBUG"

# 自定义日志格式
# 打印在文件里的格式：时间戳 + 线程名 + 线程ID + 任务ID + 发出日志调用的源文件名 + 发出日志调用的源代码行号 + 日志级别 + 日志消息正文
# [2023-06-04 15:16:05][MainThread:22896][task_id:root][调用.py:12][INFO][这是注册功能]
STANDARD_FORMAT = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d][%(levelname)s][%(message)s]'
# 打印在控制台的格式：日志级别 + 时间戳 + 发出日志调用的源文件名 + 发出日志调用的源代码行号 + 日志消息正文
# [INFO][2023-06-04 15:37:28,019][调用.py:12]这是注册功能

SIMPLE_FORMAT = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
'''
参数详解:
-1.%(asctime)s: 时间戳，表示记录时间
-2.%(threadName)s: 线程名称
-3.%(thread)d: 线程ID
-4.task_id:%(name)s: 任务ID，即日志记录器的名称
-5.%(filename)s: 发出日志调用的源文件名
-6.%(lineno)d: 发出日志调用的源代码行号
-7.%(levelname)s: 日志级别，如DEBUG、INFO、WARNING、ERROR、CRITICAL等
-8.%(message)s: 日志消息正文
'''

# 日志文件路径
# os.getcwd() : 获取当前工作目录，即当前python脚本工作的目录路径
# 拼接日志文件路径 : 当前工作路径 + “logs”(日志文件路径)
LOG_PATH = os.path.join(BASE_PATH, "log", "Activity_logs")
print(LOG_PATH)
# OS模块 ： 创建多层文件夹
# exist_ok=True 的意思是如果该目录已经存在，则不会抛出异常。
os.makedirs(LOG_PATH, exist_ok=True)
# log日志文件路径 ： 路径文件夹路径 + 日志文件
LOG_FILE_PATH = os.path.join(LOG_PATH, 'Logs.log')
print(LOG_FILE_PATH)

# 日志配置字典
LOGGING_DIC = {
    # 日志版本
    'version': 1,
    # 表示是否要禁用已经存在的日志记录器（loggers）。
    # 如果设为 False，则已经存在的日志记录器将不会被禁用，而是可以继续使用。
    # 如果设为 True，则已经存在的日志记录器将会被禁用，不能再被使用。
    'disable_existing_loggers': False,
    # 格式化程序：用于将日志记录转换为字符串以便于处理和存储。
    # 格式化程序定义了每个日志记录的输出格式，并可以包括日期、时间、日志级别和其他自定义信息。
    'formatters': {
        # 自定义格式一：年-月-日 时:分:秒
        'standard': {
            # 自定义日志格式 ：时间戳 + 线程名 + 线程ID + 任务ID + 发出日志调用的源文件名 + 发出日志调用的源代码行号 + 日志级别 + 日志消息正文
            # 这里要对应全局的 STANDARD_FORMAT 配置
            'format': STANDARD_FORMAT,
            # 时间戳格式：年-月-日 时:分:秒
            'datefmt': '%Y-%m-%d %H:%M:%S'  # 时间戳格式
        },
        # 自定义格式二：
        'simple': {
            # 自定义日志格式：# 日志级别 + 时间戳 + 发出日志调用的源文件名 + 发出日志调用的源代码行号 + 日志消息正文
            # 这里要对应全局的 SIMPLE_FORMAT 配置
            'format': SIMPLE_FORMAT
        },
    },
    # 过滤器
    'filters': {},
    # 日志处理器
    'handlers': {
        # 自定义处理器名称 - 输出到控制台屏幕
        'console': {
            # 设置日志等级 为INFO
            'level': CONSOLE_LOG_LEVEL,
            # 表示该处理器将输出日志到流（stream）：日志打印到控制台
            'class': 'logging.StreamHandler',
            # 日志打印格式：日志级别 + 时间戳 + 发出日志调用的源文件名 + 发出日志调用的源代码行号 + 日志消息正文
            # 这里的配置要对应 formatters 中的 simple 配置
            'formatter': 'simple'
        },
        # 自定义处理器名称 - 输出到文件
        'default': {
            # 自定义日志等级
            'level': FILE_LOG_LEVEL,
            # 标准输出到文件
            'class': 'logging.handlers.RotatingFileHandler',
            # 日志打印格式：年-月-日 时:分:秒
            # 这里的配置要对应 formatters 中的 standard 配置
            'formatter': 'standard',
            # 这里 要注意声明配置文件输出端的文件路径
            'filename': LOG_FILE_PATH,
            # 限制文件大小：1024 * 1024 * 5 = 5242880，意味着这个变量的值是 5MB（兆字节）
            'maxBytes': 1024 * 1024 * 5,
            # 表示保留最近的5个日志文件备份。
            # 当日志文件达到最大大小限制时，将会自动轮转并且保留最新的5个备份文件，以便查看先前的日志记录。
            # 当日志文件达到最大大小限制时，会自动进行轮转，后续的文件名将会以数字进行命名，
            # 例如，第一个备份文件将被重命名为原始日志文件名加上".1"的后缀，
            # 第二个备份文件将被重命名为原始日志文件名加上“.2”的后缀，
            # 以此类推，直到保留的备份数量达到设定的最大值。
            'backupCount': 5,
            # 日志存储文件格式
            'encoding': 'utf-8',
        },
    },
    # 日志记录器，用于记录应用程序的运行状态和错误信息。
    'loggers': {
        # 空字符串作为键 能够兼容所有的日志(当没有找到对应的日志记录器时默认使用此配置)
        # 默认日志配置
        '': {
            # 日志处理器 类型：打印到控制台输出 + 写入本地日志文件
            'handlers': ['default', 'console'],
            # 日志等级 ： DEBUG
            'level': 'DEBUG',
            # 默认情况下，当一个日志消息被发送到一个Logger对象且没有被处理时，该消息会被传递给它的父Logger对象，以便在更高层次上进行处理。
            # 这个传递过程称为“传播(propagation)”，而propagate参数指定了是否要使日志消息向上传播。
            # 将其设置为True表示应该传播消息到上一级的Logger对象；如果设置为False则不传播。
            # 表示异常将会在程序中继续传播
            # 也就是说，如果一个异常在当前的代码块中没有被处理，它将会在上级代码块或调用函数中继续向上传递，直到被某个代码块捕获或者程序退出。
            # 这是 Python 中异常处理机制的默认行为。
            # 如果将 'propagate' 设置为 False，则异常不会被传播，即使在上级代码块中没有处理异常的语句，程序也会忽略异常并继续执行。
            'propagate': True,
        },
    },
}
