"""
日志工具类
"""

from logging import getLogger, FileHandler, Formatter, ERROR, DEBUG, INFO, WARN
from eqlog.components.file_option import FileOption
from eqlog.components.create_log_file import create_log_file
from functools import wraps
from time import strftime, localtime
from datetime import datetime
from inspect import stack as ins_stack


def log_connect(params):
    """
    用于日志的参数拼接
    :param params: 要拼接的日志列表
    :return: 拼接后的日志字符串
    """
    info = ''
    for item in params:
        info = info + ' ' + str(item)
    return info.strip()


class Logger:
    """
    日志控制器，对 logging 进行定制化增强
    """

    '''
    日志级别字典，直接使用 logging 的定义
    '''
    level_dictionary = {
        'INFO': INFO,
        'ERROR': ERROR,
        'DEBUG': DEBUG,
        'WARNING': WARN
    }

    def __init__(self, module_name='common', level='INFO', log_file_dir='', conf_file='', conf_deep=3,
                 conf_console=None):
        """
        日志工具初始化
        :param module_name: 日志模块名称，默认为 common
        :param level: 日志级别，默认为 INFO
        :param log_file_dir: 日志文件根目录
        :param conf_file: 配置文件
        :param conf_deep: 配置文件搜索深度，默认为3个层级
        :param conf_console: 控制台日志打印标志
        """
        '''
        初始化文件操作对象，校验配置文件是否存在(此时不再传入配置文件路径)，读取配置文件
        '''
        self.op = FileOption(conf_file, conf_deep)
        self.op.config_path_read()
        self.op.read_xml()
        '''
        根据配置文件，加载日志输出目录、控制台打印标志到本对象中
        '''
        self._root = self.op.logfile_path if log_file_dir == '' else self.op.logfile_path
        self._console = self.op.console if conf_console is None else self.op.console
        '''本地时间，用于生成日志文件名称'''
        self._date_time = strftime("%Y-%m-%d", localtime())
        '''日志模块名称，用于生成日志文件名称'''
        self._log_module_name = module_name
        file_name = self.set_log_file_name()
        create_log_file(file_name)
        '''
        初始化 logging 工具
        '''
        self._logger = getLogger()
        self._logger.setLevel(self.level_dictionary[level])  # 日志级别
        self._formatter = Formatter(
            "%(asctime)s [%(levelname)s] %(message)s")  # 日志格式
        self._file_handler = FileHandler(file_name, encoding='utf-8', mode='a')  # 日志文件编码
        self._file_handler.setFormatter(self._formatter)  # 日志文件格式

    def log(self, func):
        """
        函数装饰器：被装饰函数隐式输出日志
        :param func: 被装饰函数
        :return: 装饰后的新函数
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                self.common_log('info', '[decorator: ' + func.__name__ + '] [params args]:' + (
                    'None' if (lambda x: not x)(args) else str(args)) + ' [params kwargs]:' + (
                                    'None' if (lambda x: not x)(kwargs) else str(kwargs)))
                return func(*args, **kwargs)
            except Exception as e:
                self.common_log('error', '[decorator: ' + func.__name__ + '] [执行异常]:' + str(e))

        return wrapper

    def common_log(self, level='info', message=''):
        """
        通用 日志处理入口
        :param level: 输出日志级别
        :param message: 日志字符串
        :return: None
        """
        '''
        每次打印时，检查日志打印时间（本地日期与日系统日期），跨日时更新
        '''
        if strftime("%Y-%m-%d", localtime()) != self._date_time:
            '''
            _date_time 日志系统登记的时间
            '''
            self._date_time = strftime("%Y-%m-%d", localtime())
            '''
            生成新日期的 file name，重新设置 logging
            '''
            file_name = self.set_log_file_name()
            self._file_handler = FileHandler(file_name, encoding='utf-8', mode='a')
            self._file_handler.setFormatter(self._formatter)
        '''
        手动设置一下 logging 输出的日志文件，为啥？ 忘了...
        '''
        self._logger.addHandler(self._file_handler)
        '''
        格式化日志，加入函数出错位置的打印（文件、行号、函数名）
        '''
        message = f"[{ins_stack()[2].filename}, line {ins_stack()[2].lineno}] [function {ins_stack()[2].function}] {message}"
        '''
        如果开启了控制台输出，则使用 print 打印到控制台
        '''
        if self._console:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3], '[' + level.upper() + '] [eqlog]',
                  message)
        '''
        根据不同的日志级别，调用不同的 logging 函数
        '''
        if level == 'info':
            self._logger.info(message)
        elif level == 'warning':
            self._logger.warning(message)
        elif level == 'debug':
            self._logger.debug(message)
        else:
            self._logger.error(message)
        self._logger.removeHandler(self._file_handler)

    def set_log_file_name(self):
        """
        日志文件名设置
        :return: 日志文件完整路径
        """
        if self._log_module_name == 'common':
            file_name = self._root + 'common_' + self._date_time + '.log'
        else:
            file_name = self._root + self._log_module_name + '_' + self._date_time + '.log'
        return file_name

    def info(self, *args):
        """
        info 级别日志
        :param args: 日志列表
        :return:
        """
        self.common_log('info', log_connect(args))

    def error(self, *args):
        """
        error 级别日志
        :param args: 日志列表
        :return: None
        """
        self.common_log('error', log_connect(args))

    def warning(self, *args):
        """
        waring 级别日志
        :param args: 日志列表
        :return: None
        """
        self.common_log('warning', log_connect(args))

    def debug(self, *args):
        """
        debug 级别日志
        :param args: 日志列表
        :return: None
        """
        self.common_log('debug', log_connect(args))


"""
可用于默认的日志输出
"""
eqlog = Logger()
