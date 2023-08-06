"""
日志读写相关的文件操作
"""

from datetime import datetime
from os import path as os_path, getcwd as os_get_cwd
from platform import system as plat_system
from inspect import stack as ins_stack
from xml.etree.cElementTree import parse as xml_tree

"""
cElementTree C 语言实现，速度更快，占用内存更少
ElementTree Python 语言实现
"""


class FileOption:
    """
    日志读写相关的文件操作
    """

    def __init__(self, conf_path, conf_deep):
        """
        类初始化
        :param conf_path: str 配置文件路径 xxx.xml
        :param conf_deep: int 配置文件搜索深度
        """
        '''
        设置配置文件路径
        1、配置文件为空，读取运行程序所在路径下的 eqlog.xml 文件，作为配置文件
        2、配置文件不为空，且最后4个字符为 .xml，则使用传入值作为配置文件
        3、配置文件只传入了路径，则读取传入路径下的 eqlog.xml 文件作为配置文件
        conf_path 设置配置文件所在目录
        '''
        if conf_path == '' or conf_path is None:
            self.conf_path = os_get_cwd() + '/eqlog.xml'
        elif conf_path[-4:] == '.xml':
            self.conf_path = conf_path
        elif conf_path[-1:] == '/' or conf_path[-1:] == '\\':
            self.conf_path = conf_path + 'eqlog.xml'
        else:
            self.conf_path = conf_path + '/eqlog.xml'
        '''
        上述路径下未找到配置文件，则会进行配置文件搜索
        conf_deep 设置配置文件搜索深度
        '''
        self.conf_deep = conf_deep
        '''
        日志文件需要写入到某个目录下
        logfile_path 设置日志文件存储目录
        '''
        self.logfile_path = ''
        '''
        Windows 和 Linux 系统，文件目录需要进行区别设置
        env 存储当前系统的类型
        '''
        self.env = 'win_path' if plat_system().lower() == 'windows' else 'linux_path'
        '''
        console 控制日志是否打印在控制台，默认为 False.
        '''
        self.console = False

    def config_path_read(self, deep=1):
        """
        配置文件存在性校验
        :param deep: 找不到配置文件时，自动搜索的目录深度
        :return: None 无返回值
        """
        '''
        递归调用与判断
        如果未找到配置文件，则在同级目录下寻找 eqconfig 下 eqlog.xml
        如果当前目录下 eqlog.xml eqconfig/eqlog.xml 均不存在，按照深度，向上查找
        '''
        if not os_path.exists(self.conf_path):
            eqlog_dir = os_path.dirname(self.conf_path) + '/eqconfig/eqlog.xml'
            if not os_path.exists(eqlog_dir) and deep <= self.conf_deep:
                '''文件不存在，继续深入查找'''
                self.conf_path = os_path.abspath(os_path.join(os_path.dirname(self.conf_path), "..")) + '/eqlog.xml'
                self.config_path_read(deep + 1)
            else:
                '''文件已存在，使用当前文件'''
                self.conf_path = eqlog_dir

    def read_xml(self, conf_path=''):
        """
        读取 xml 文件配置项
        :param conf_path: xml配置文件路径
        :return: None
        """
        '''
        如果未手动传入配置文件，则使用对象初始化时设置的配置文件
        '''
        conf_path = self.conf_path if conf_path == '' else conf_path
        '''
        读取日志文件所在目录，写入对象 logfile_path 属性中
        '''
        try:
            xml_root = xml_tree(conf_path).getroot()
            self.logfile_path = xml_root.find('file_path').find(self.env).text
        except Exception as e:
            self.logfile_path = os_get_cwd().replace('\\', '/') + '/logs/'
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3], '[WARNING]', '[eqlog]',
                  f"[{__file__}, {ins_stack()[0].function}(), line {ins_stack()[0].lineno}]",
                  '[读取日志文件目录失败，在当前目录输出]', str(e))
        '''
        读取控制台输出标志，写入对象 console 属性中
        '''
        try:
            xml_root = xml_tree(conf_path).getroot()
            self.console = True if xml_root.find('console').text == 'true' else False
        except Exception as e:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3], '[WARNING]', '[eqlog]',
                  f"[{__file__}, {ins_stack()[0].function}(), line {ins_stack()[0].lineno}]",
                  '[读取控制台输出配置失败，默认为False，不在控制台打印]', str(e))
