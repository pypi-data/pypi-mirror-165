#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Time  : 2022/8/21 0:23
@File  : conftest.py
'''
from saf import Create_ZenTao_BUG
import pytest

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    """
    :param item:
    """
    outcome = yield
    report = outcome.get_result()
    if report.outcome == 'failed':
        doc = item.function.__doc__
        doc = str(doc).replace('\n', '<br>')
        Create_ZenTao_BUG(title=item.function.__name__,
                          steps=f'{doc}预期结果：passed<br>测试结果：{report.outcome}')