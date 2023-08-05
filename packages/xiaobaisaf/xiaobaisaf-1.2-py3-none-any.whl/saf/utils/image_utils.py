#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Time  : 2022/8/24 1:37
@File  : image_utils.py
'''
''' 将图片验证码转为字符串的样例 '''
import logging
from saf import *

c = selenium_webdriver.Chrome(ChromeDriverManager(log_level=logging.ERROR).install())
c.get('http://121.62.63.73:10721/admin/login')

c.find_element(by=By.XPATH, value='//*[@class="pictrue"]').screenshot('1.png')
f = open('1.png', 'rb')
print(img2str(f.read()))
os.remove('1.png')