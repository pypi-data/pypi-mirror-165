"""
=========================
File: test_collection.py
Author: dancing
Time: 2022/8/28
E-mail: zhangqi_xxs@163.com
=========================
"""
import pytest


@pytest.mark.parametrize("name", ["采购", "销售"])
def test_xx(name):
    print("name")
