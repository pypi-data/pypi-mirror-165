#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/7/4 14:56
# @Author  : zbc@mail.ustc.edu.cn
# @File    : setup.py
# @Software: PyCharm

from setuptools import setup

with open('README.md', 'r', encoding='utf-8')as f:
    long_description = f.read()

setup(
    name='rdu',
    version='0.0.8',
    author='zbc',
    author_email='zbc@mail.ustc.edu.cn',
    url='https://github.com/zbc0315/rdu',
    description=u'reaction data utils',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['rdu'],
    install_requires=['pandas'],
    include_package_data=True,
    entry_points={
        'console_scripts': [

        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6'
)


if __name__ == "__main__":
    pass
