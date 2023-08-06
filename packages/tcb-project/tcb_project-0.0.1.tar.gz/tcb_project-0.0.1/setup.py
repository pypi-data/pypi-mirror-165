from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()

setup(name='tcb_project',  # 包名
      version='0.0.1',  # 版本号
      description='Collecting C.elegans WGS Data with obvious phenotype',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Guo_Zhengyang',
      author_email='guozhengyang980525@yahoo.co.jp',
      install_requires=['pandas'],
      license='MIT License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=['Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', ]
      )