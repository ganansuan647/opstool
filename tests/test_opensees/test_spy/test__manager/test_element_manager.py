from typing import Any, Optional

import openseespy.opensees as ops
import pytest

from opstool.opensees.spy import BaseHandler, ElementManager


@pytest.fixture
def element_manager() -> ElementManager:
    """每个测试前初始化一个ElementManager实例"""
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 6)
    return ElementManager()

def test_handle_zeroLength(element_manager: ElementManager) -> None:
    """测试zeroLength单元的数据处理功能"""
    # 3D单元情况
    cmd = "element"
    args = ("zeroLength", 1, *[1,20], "-mat", *[911, 923], "-dir", *[1, 5], "-doRayleigh", 0, "-orient", *[0,0,1], *[1,1,1])
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查节点是否正确存储
    assert 1 in element_manager.zerolength
    element_data = element_manager.zerolength[1]
    assert element_data["type"] == "zeroLength"
    assert element_data["nodes"] == [1, 20]
    assert element_data["mat"] == [911, 923]
    assert element_data["dir"] == [1, 5]
    assert element_data["rFlag"] == 0
    assert element_data["vecx"] == [0,0,1]
    assert element_data["vecyp"] == [1,1,1]
