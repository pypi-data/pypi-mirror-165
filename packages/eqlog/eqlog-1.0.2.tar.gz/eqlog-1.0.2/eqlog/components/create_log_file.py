"""
创建日志文件
"""

import os
import traceback


def create_log_file(file_name):
    """
    创建日志文件
    :param file_name: 传入日志文件名称（含路径）
    :return: None 无返回信息
    """

    '''
    判断日志文件所在路径是否存在，如果不存在则进行创建
    '''
    if not os.path.exists(os.path.dirname(file_name)):
        try:
            os.makedirs(os.path.dirname(file_name))
        except Exception as e:
            info = traceback.format_exc()
            print(str(e), info)  # 路径创建失败，打印异常

    '''
    判断日志文件是否存在，如果不存在则进行创建
    '''
    if not os.path.exists(file_name):
        try:
            f = open(file_name, 'w')
            f.close()
        except Exception as e:
            info = traceback.format_exc()
            print(str(e), info)  # 日志文件创建失败，打印异常
