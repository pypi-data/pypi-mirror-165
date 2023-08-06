#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Time  : 2022/8/27 23:10
@File  : test_zentao.py
'''
import pytest

''' 测试提交BUG单在conftest.py中，但是本用例触发 '''

def test_login():
    ''' 测试登录
        1、判断账户正确性
        2、判断密码正确性
        3、提交数据
    '''
    assert True

def test_search():
    ''' 测试搜索
        1、输入数据
        2、点击搜索按钮
    '''
    assert True

def test_order():
    ''' 测试下单
        1、选择商品
        2、点击下单按钮
    '''
    assert True