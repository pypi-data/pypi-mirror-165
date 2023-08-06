"""
eqlog 组件

create_log_file --- 创建日志文件
file_option --- 日志读写相关的文件操作
"""

"""
eqlog.xml 配置文件示例

<?xml version="1.0" ?>
<eqlog>
    <!--  配置文件名称  -->
    <file_name name="name">eqlog.xml</file_name>
    <!--  控制台是否输出  -->
    <console name="console_flag">true</console>
    <!--  配置文件目录  -->
    <file_path name="path">
        <!--  linux下的日志文件目录  -->
        <linux_path name="linux">/home/data/logs/</linux_path>
        <!--  windows下的日志文件目录  -->
        <win_path name="win">D:/MyProjects/eqlog/tests/logs/</win_path>
    </file_path>
</eqlog>
"""
