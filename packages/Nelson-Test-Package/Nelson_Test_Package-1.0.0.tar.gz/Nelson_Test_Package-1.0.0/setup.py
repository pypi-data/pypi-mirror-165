from distutils.core import setup

setup(
    name='Nelson_Test_Package',  # 对外模块的名字
    version='1.0.0',  # 版本号
    description='测试本地发布模块',  # 描述
    author='nelson',  # 作者
    author_email='710378572@qq.com',
    py_modules=['test_function'],  # 要发布的模块
)