from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()


# tutor: https://developer.aliyun.com/article/778803

# license : https://choosealicense.com/community/

# dowloading statistics https://pepy.tech/

setup(name='jojo-net',  # 包的分发名称
      version='0.3.0',  # PyPI上只允许一个版本存在，如果后续代码有了任何更改，再次上传需要增加版本号
      description='network utilities',  # 项目的简短描述
      long_description=long_description,  # 详细描述，会显示在PyPI的项目描述页面。必须是rst(reStructuredText) 格式的
      author='JoStudio',
      author_email='jostudio@189.cn',
      url='https://www.jostudio.com.cn/python',
      install_requires=['requests'],  # 项目依赖哪些库，这些库会在pip install的时候自动安装
      license='Apache License 2.0',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: English', # Chinese(Simplified)
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
)
