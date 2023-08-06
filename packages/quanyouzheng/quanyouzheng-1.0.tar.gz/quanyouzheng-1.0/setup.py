

from distutils.core import  setup
import setuptools
packages = ['healthautotest']# 唯一的包名，自己取名
setup(name='quanyouzheng',
      version='1.0',
      author='Quan-u',
      packages=packages,
      package_dir={'requests': 'requests'},)
