#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Time  : 2022/8/28 23:40
@File  : test_element.py
'''
from saf import *
from saf.utils.elementUtils import find_element
from saf.utils.imageUtils import image2str

c = selenium_webdriver.Chrome()
c.get('')
image2str()
find_element(driver=c, value='')