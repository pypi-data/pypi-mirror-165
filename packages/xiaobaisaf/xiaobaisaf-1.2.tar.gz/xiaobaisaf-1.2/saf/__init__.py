#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Time  : 2022/8/20 22:22
@File  : __init__.py
'''
from typing import Union
from collections import OrderedDict
import datetime

# 将pip更新源设置为：https://pypi.douban.com/simple
# pip config set global.index-url https://pypi.douban.com/simple

from selenium import webdriver as selenium_webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys     # 键盘事件
from selenium.webdriver.common.action_chains import ActionChains  # 鼠标事件
from webdriver_manager.chrome import ChromeDriverManager
from loguru import logger
from requests import request, Session
from appium import webdriver as appium_webdriver
from jmespath import search
from yaml import full_load
import click

# 当前版本的httpx，只有在异步请求时才略优于requests，此处可使用到发送消息使用
# from httpx import request
try:
    from ddddocr import DdddOcr
    img2str = DdddOcr(show_ad=False).classification
except ImportError as e:
    import os; os.system('pip install ddddocr -i https://pypi.douban.com/simple')
    # 如果运行ddddocr运行报错更新opencv库：
    os.system('pip uninstall opencv-python')
    os.system('pip uninstall opencv-contrib-python')
    os.system('pip install opencv-contrib-python')
    os.system('pip install opencv-python')

from iniconfig import IniConfig
from saf.data.config import *

def send_message(
        url: str = None,
        msg: dict = None,
        assert_path: str = None,
        assert_value: Union[str, int] = None
):
    '''
    发送消息函数
    :param url:             WebHook的URL地址
    :param msg:             WebHook发送的信息
    :param assert_path:     判断内容的路径
    :param assert_value:    判断内容的值
    :return:
    '''
    if not url and not msg:
        raise ('url或者msg信息不能为空，必填内容！')
    else:
        response = request(
                        method='POST',
                        url=url,
                        headers={'Content-Type': 'application/json'},
                        json=msg
                    )
    if assert_path and assert_value:
        try:
            assert assert_value == search(assert_path, response.json())
        except AssertionError as e:
            raise ('信息发送失败！')

def feishu_webhook_send_message(msg:str = '本次测试结束'):
    '''
    使用飞书的webhook发送机器人消息
    :param msg:     需要发送的信息内容，
    :return:

    调用飞书机器人发送飞书群消息
    @feishu_help_document = https://open.feishu.cn/document/ukTMukTMukTM/ucTM5YjL3ETO24yNxkjN
    '''
    send_message(url=feishu.webhook(),
                 msg={
                     'msg_type': 'text',
                     'content': {
                         'text': msg
                     }
                 },
                 assert_path='StatusCode',
                 assert_value=0
    )

def dingding_webhook_send_message(msg:str = '本次测试结束'):
    '''
    使用钉钉的webhook发送机器人消息
    :param msg:     需要发送的信息内容，
    :return:

    调用钉钉机器人发送钉钉群消息
    @dingding_help_document = https://open.dingtalk.com/document/group/custom-robot-access
    '''
    send_message(url=dingding.webhook(),
                 msg={'msgtype': 'text',
                        'text': {
                         'content': msg
                        }
                 },
                 assert_path='errcode',
                 assert_value=0
    )

def robot_send_message(robot_name: str= 'feishu', msg: str = '本次测试结束'):
    ''' 统一调用机器人发送消息 '''
    if 'feishu' in robot_name:
        feishu_webhook_send_message(msg)
    if 'dingding' in robot_name:
        dingding_webhook_send_message(msg)

session = Session()
def login_zentao():
    ''' 禅道的免密登录，使用session模式登录 '''
    global session
    # if 'zentaosid' not in session.cookies.keys():
        # 创建应用免密模式
    url = f'{zenTao.baseURL()}/api.php?m=user&f=apilogin&account={zenTao.account()}&code={zenTao.getCode()}&time={zenTao.getTime()}&token={zenTao.getToken()}'
    session.get(url)
def Create_ZenTao_BUG(product: int = 1,
                      branch: int = '',
                      module: int = '',
                      title: str = f'BUG标题-{int(time.time())}',
                      openedBuild: Union[int, str] = 'trunk',
                      execution: int = 0,
                      assignedTo: str = '',
                      deadline: datetime.date = datetime.date.today() + datetime.timedelta(3),  # 为期3天
                      feedbackBy: str = '',
                      type: str = '',
                      os_name: str = '',
                      browser: str = '',
                      color: str = '',
                      serverity: int = 3,
                      pri: int = 3,
                      steps: str = '',
                      story: int = '',
                      task: int = '',
                      mailto: str = '',
                      keywords: str = ''
                      ):
    '''
    禅道提BUG单
    :param product          : 所属产品ID *必填
    :param branch           : 分支/平台
    :param module           : 所属模块
    :param title            : Bug标题 *必填
    :param openedBuild      : 影响版本 *必填
    :param execution        : 所属执行 为0
    :param assignedTo       : 指派给
    :param deadline         : 截止日期 日期格式：YY-mm-dd，如：2022-08-28
    :param type             : Bug类型 取值范围： | codeerror | config | install | security | performance | standard | automation | designdefect | others
    :param os_name          : 操作系统 取值范围： | all | windows | win10 | win8 | win7 | vista | winxp | win2012 | win2008 | win2003 | win2000 | android | ios | wp8 | wp7 | symbian | linux | freebsd | osx | unix | others
    :param browser          : 浏览器 取值范围： | all | ie | ie11 | ie10 | ie9 | ie8 | ie7 | ie6 | chrome | firefox | firefox4 | firefox3 | firefox2 | opera | oprea11 | oprea10 | opera9 | safari | maxthon | uc | other
    :param color            : 标题颜色 颜色格式：#RGB，如：#3da7f5
    :param serverity        : 严重程度 取值范围：1 | 2 | 3 | 4
    :param pri              : 优先级 取值范围：0 | 1 | 2 | 3 | 4
    :param steps            : 重现步骤
    :param story            : 需求ID
    :param task             : 任务ID
    :param mailto           : 抄送给 填写帐号，多个账号用','分隔。
    :param keywords         : 关键词
    :return:

    帮助文档：https://www.zentao.net/book/zentaopmshelp/integration-287.html
    '''
    login_zentao()
    add_bug_url = f'{zenTao.baseURL()}/bug-create-{product}-{branch}-moduleID={module}.json?tid=h96emyim'
    payload = f"------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"product\"\r\n\r\n{product}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"module\"\r\n\r\n{module}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"project\"\r\n\r\n1\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"execution\"\r\n\r\n{execution}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"openedBuild[]\"\r\n\r\n{openedBuild}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"assignedTo\"\r\n\r\n{assignedTo}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"deadline\"\r\n\r\n{str(deadline)}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"feedbackBy\"\r\n\r\n{feedbackBy}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"notifyEmail\"\r\n\r\n\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"type\"\r\n\r\n{type}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"os\"\r\n\r\n{os_name}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"browser\"\r\n\r\n{browser}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"title\"\r\n\r\n{title}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"color\"\r\n\r\n{color}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"severity\"\r\n\r\n{serverity}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"pri\"\r\n\r\n{pri}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"steps\"\r\n\r\n{steps}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"story\"\r\n\r\n{story}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"task\"\r\n\r\n{task}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"oldTaskID\"\r\n\r\n0\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"mailto[]\"\r\n\r\n{mailto}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"keywords\"\r\n\r\n{keywords}\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"status\"\r\n\r\nactive\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"issueKey\"\r\n\r\n\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"labels[]\"\r\n\r\n\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"files[]\"\r\n\r\n\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"uid\"\r\n\r\n\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"case\"\r\n\r\n0\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"caseVersion\"\r\n\r\n0\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"result\"\r\n\r\n0\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs\r\nContent-Disposition: form-data; name=\"testtask\"\r\n\r\n0\r\n------WebKitFormBoundaryRWJBJ0CsyWBBWFKs--".encode('UTF-8')
    headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryRWJBJ0CsyWBBWFKs',
            'Referer': f'{zenTao.baseURL()}/bug-create-{product}-{branch}-moduleID={module}.json?tid=h96emyim',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.63',
            'X-Requested-With': 'XMLHttpRequest'
    }
    s = session.post(url=add_bug_url, headers=headers, data=payload)
    print(s.json())

def view_bug(id: int = 1):
    login_zentao()
    view_bug_url = f'{zenTao.baseURL()}/bug-view-{id}.json?tid=gz3p07qa'
    session.get(url=view_bug_url)


if __name__ == '__main__':
    # robot_send_message(robot_name='feishu')
    # view_bug()
    Create_ZenTao_BUG()
    Create_ZenTao_BUG()
    # login_zentao()


