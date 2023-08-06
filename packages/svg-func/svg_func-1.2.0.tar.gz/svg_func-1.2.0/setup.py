from setuptools import setup
import setuptools

setup(name='svg_func',
      version='1.2.0',
      description='functions in svg for logo, debug for near rectangle',
      author='xmn',
      author_email='2579015983@qq.com',
      url='https://www.python.org/',
      license='MIT',
      keywords='svg',
      project_urls={
            'Documentation': 'https://packaging.python.org/tutorials/distributing-packages/',
            'Funding': 'https://donate.pypi.org',
            'Source': 'https://github.com/pypa/sampleproject/',
            'Tracker': 'https://github.com/pypa/sampleproject/issues',
      },
      package_dir={"": "src"},
      packages=setuptools.find_packages(where="src"),
      install_requires=[],
      python_requires='>=3'
     )

'''
https://www.cnblogs.com/yinzhengjie/p/14124623.html
creat python project:
python setup.py sdist
twine upload dist/*
# 1.0.15 适用于arch。poly，random，在前端表现合格
# 1.0.16 修改在4边有一边为弧线的类矩形上的角点匹配错误
# 1.0.17 修改在4边有一边为弧线的类矩形上的角点匹配错误. 选用新的配置条件，轮廓中直线长度占一半时，转用角点而不是弧线中的对角线原理
# 1.0.18 修改s_hz获取速度慢的问题
# 1.2.0  修改trans_points里各个函数运行速度慢的问题，重复使用的函数提前获取参数常量，再复用
'''