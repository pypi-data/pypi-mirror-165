from distutils.core import setup



setup(
    name='duote',  # 对外模块的名字
    version='0.1.3',  # 版本号
    description='测试版本,基本功能',  # 描述
    author='JinxAndLux',  # 作者
    author_email='yby1234@hotmail.com',
    py_modules=['duote.crawler.article','duote.crawler.question','duote.web.func'],  # 要发布的模块

)