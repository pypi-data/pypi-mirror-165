# eqlog
日志处理工具，对 logging 进行了扩展和定制使用。



## 使用说明

### 1.安装
```shell script
pip install eqlog
```

### 2.升级
```shell script
pip install --upgrade eqlog
```

### 3.作为函数装饰器
> 打印函数入参和执行异常信息

```python
from eqlog import eqlog

@eqlog.log
def func(param):
    print(param)
    print('打印函数入参和执行异常信息')
```

### 4.主动调用
```python
from eqlog import eqlog

def func(param):  
    eqlog.info(param)  
    eqlog.debug(param)  
    eqlog.warning(param)  
    eqlog.error(param)  
```

### 5.配置文件
> 配置文件命名为 eqlog.xml，可放在项目启动文件同级目录、上级目录、上上级目录
```xml
<?xml version="1.0" ?>
<eqlog>
    <!--  配置文件名称  -->
    <file_name name="name">eqlog.xml</file_name>
   <!--  控制台是否输出 true 或 false  -->
    <console name="console_flag">true</console>
    <!--  配置文件目录  -->
    <file_path name="path">
        <!--  linux下的日志文件目录  -->
        <linux_path name="linux">/home/data/logs/</linux_path>
        <!--  windows下的日志文件目录  -->
        <win_path name="win">D:/MyProjects/eqlog/tests/logs/</win_path>
    </file_path>
</eqlog>
```

### 6.主动声明日志工具
```python
from eqlog import Logger

eq_logger = Logger('module_name', log_file_dir='./log/',conf_file='./log.xml')

@eq_logger.log
def func(param):  
    eq_logger.info(param)  
    eq_logger.debug(param)  
    eq_logger.warning(param)  
    eq_logger.error(param)  
```

### 7. 日志输出
#### 文件日志
```
2022-07-07 15:08:35,632 [INFO] [D:/MyProjects/eqlog/tests/test_log_one.py, line 23] [function <module>] [Function test_log_func()] [Params]:('the function is test_log_func, file is test_log_one.py',), 
2022-07-07 15:08:35,635 [ERROR] [D:/MyProjects/eqlog/tests/test_log_one.py, line 23] [function <module>] [Function test_log_func()] [执行异常]:name 'e' is not defined
```
#### 控制台日志
多了 "\[eqlog]" 标识
```
2022-07-07 20:28:37,632 [INFO] [eqlog] [D:/MyProjects/eqlog/tests/two/test_log_two.py, line 17] [function test_log_func] the function is test_log_func, file is test_log_two.py
2022-07-07 20:28:37,633 [ERROR] [eqlog] [D:/MyProjects/eqlog/tests/two/test_log_two.py, line 23] [function <module>] [decorator: test_log_func] [执行异常]:name 'e' is not defined
```

## 版本说明

### 1、当前版本：V1
```shell script
pip install eqlog==1.0.2
```
- 修复单词拼写 bug 
- 解决配置文件读取 bug
- 解决 0.0.7 版本，日志记录中，代码文件及行数展示错误的问题
- 移除若干无用、冗余逻辑
- 添加代码注释

### 2、未来版本
```
分布式日志、嵌入第三方模块
```

### 3、历史版本
```
eqlog: 0.0.1 ~ 0.0.7
```


### 免责声明

* 本项目所有内容仅供参考和学习交流使用。
* 项目所存在的风险将由使用者自行承担，因使用本项目而产生的一切后果也由使用者自己承担。
* 凡以任何方式直接、间接使用本项目的人员，视为自愿接受本项目声明的约束。