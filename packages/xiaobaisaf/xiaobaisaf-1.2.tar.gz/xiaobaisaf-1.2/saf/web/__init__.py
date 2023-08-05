#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Time  : 2022/8/20 22:47
@File  : __init__.py
'''
'''
PO模式：
    1、基础元素定位函数的封装（基础定位、键盘、鼠标事件，解决：定位不稳定问题）
    2、页面元素的定位（定位层）
    3、页面元素的操作（操作层）
    4、界面业务的操作（业务层）
    5、基于单元模块的用例（用例层）
'''
from saf import WebDriver, By
from time import sleep

def get_element(driver: WebDriver = None, loc: str = None, total_time: int = 30, step_time: float = 0.5):
    '''
    通用定位元素方法
    :param driver:          浏览器对象
    :param loc:             定位表达式
    :param total_time:      定位超时时间（单位：秒）
    :param step_time:       每次间隔定位时间（单位：秒）
    :return:
    '''
    while 1:
        if total_time > 0:
            if 0 == len(driver.find_elements(by=By.XPATH, value=loc)):
                sleep(step_time)
                total_time -= step_time
            else:
                return driver.find_element(by=By.XPATH, value=loc)
        else:
            break
    return None