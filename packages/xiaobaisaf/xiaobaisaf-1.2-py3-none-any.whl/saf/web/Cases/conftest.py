#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Time  : 2022/8/21 0:23
@File  : conftest.py
'''
from saf import logger, robot_send_message
import pytest

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    :param item:
    """
    outcome = yield
    report = outcome.get_result()
    # 运行日志
    # logger.add(sink='auto_info_{time}.log', rotation='1 day')
    # logger.info(report)
    if report.outcome == 'failed':
        robot_send_message(robot_name='feishu',
                           msg=f'测试脚本：{report.nodeid.split("::")[0]}\n测试用例：{report.nodeid.split("::")[1]}\n测试结果：{report.outcome}'
                           )

'''
关于一些Chrome浏览器的设置
chrome_options = Options()
# 去除"Chrome正在受到自动化测试软件的控制"弹出框信息
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_experimental_option('excludeSwitches', ['--enable-automation'])
# 启动最大化
chrome_options.add_argument('--start-maximized')
# 规避不必要的BUG出现
chrome_options.add_argument('--disable-gpu')
prefs = {}
prefs["credentials_enable_service"] = False
prefs["profile.password_manager_enabled"] = False
chrome_options.add_experimental_option("prefs", prefs)
# 无头（无界面）模式
# chrome_options.add_argument('--headless')
# 设置手机浏览器头（模拟手机端web）
# chrome_options.add_argument('User-Agent=Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36')
# 禁止图片
# chrome_options.add_argument('blink-settings=imagesEnabled=false')
# 指定chrome.exe路径
# chrome_options.binary_location = '*\\chrome.exe'
try:
    b = webdriver.Chrome(chrome_options=chrome_options)
'''