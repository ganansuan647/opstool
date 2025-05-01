from typing import Any, Optional

import pytest

from opstool.opensees.spy import MaterialManager


@pytest.fixture
def nd_material_handler() -> MaterialManager:
    """每个测试前初始化一个MaterialManager实例"""
    return MaterialManager()

def test_command_rules(self, nd_material_handler):
    """测试命令规则"""
    rules = nd_material_handler._COMMAND_RULES
    assert "nDMaterial" in rules
    nd_rules = rules["nDMaterial"]
    assert "positional" in nd_rules
    assert nd_rules["positional"] == ["matType", "matTag", "args*"]

def test_handles(self, nd_material_handler):
    """测试handles方法"""
    commands = nd_material_handler.handles()
    assert commands == ["nDMaterial"]

def test_handle_direct(self, nd_material_handler):
    """测试直接处理nDMaterial命令"""
    # 模拟参数（一个未由特定处理器处理的材料类型）
    func_name = "nDMaterial"
    arg_map = {
        "matType": "CustomType",  # 不存在的类型，会由NDMaterialHandler直接处理
        "matTag": 1,
        "args": [100, 200, 300]
    }

    # 调用待测试方法
    nd_material_handler.handle(func_name, arg_map)

    # 验证结果
    materials = nd_material_handler.materials
    assert 1 in materials
    material = materials[1]
    assert material["matType"] == "CustomType"
    assert material["matTag"] == 1
    assert material["args"] == [100, 200, 300]
    assert material["materialCommandType"] == "nDMaterial"

def test_handle_dispatch(self, nd_material_handler):
    """测试分发处理到特定处理器"""
    # 创建模拟处理器
    mock_handler = MagicMock()
    nd_material_handler.type2handler["ElasticIsotropic"] = mock_handler

    # 模拟参数
    func_name = "nDMaterial"
    arg_map = {
        "matType": "ElasticIsotropic",
        "matTag": 2,
        "E": 2.0e5,
        "nu": 0.3
    }

    # 调用待测试方法
    nd_material_handler.handle(func_name, arg_map)

    # 验证分发是否成功
    mock_handler.handle.assert_called_once_with(func_name, arg_map)

def test_ignore_other_commands(self, nd_material_handler):
    """测试忽略非nDMaterial命令"""
    # 模拟参数
    func_name = "someOtherCommand"
    arg_map = {"matType": "Type", "matTag": 3}

    # 调用待测试方法
    nd_material_handler.handle(func_name, arg_map)

    # 验证材料未被添加
    materials = nd_material_handler.materials
    assert len(materials) == 0

