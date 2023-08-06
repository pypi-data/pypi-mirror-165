"""
=========================
File: main.py
Author: dancing
Time: 2022/8/28
E-mail: zhangqi_xxs@163.com
=========================
"""
from typing import List


def pytest_collection_modifyitems(
        session: "Session", config: "Config", items: List["Item"]
) -> None:
    print("test pytest_collection_modifyitems")
    for item in items:
        item._nodeid = item.nodeid.encode('utf-8').decode('unicode-escape')