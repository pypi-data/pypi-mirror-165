#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Time  : 2022/8/29 0:03
@File  : test_sendMsg.py
'''
import pytest

def test_xiaobai_coupon():
    assert 1 == 1

def test_xiaobai_collection():
    assert 1 == 2


if __name__ == '__main__':
    pytest.main(['-s', '-v', 'test_xiaobai_shop.py'])