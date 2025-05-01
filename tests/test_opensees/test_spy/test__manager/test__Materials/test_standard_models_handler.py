# tests/test_opensees/test_spy/test__manager/test__Materials/test_standard_models_handler.py
"""
测试StandardModelsHandler类
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

from opstool.opensees.spy._manager._Materials._StandardModelsHandler import StandardModelsHandler


@pytest.fixture
def standard_models_handler():
    """创建一个StandardModelsHandler实例供测试使用"""
    type2handler = {}
    materials = {}
    handler = StandardModelsHandler(type2handler, materials)
    yield handler


class DescribeStandardModelsHandler:
    """描述StandardModelsHandler类的行为"""

    def test_init(self, standard_models_handler):
        """测试初始化功能"""
        # 检查材料字典是否正确初始化
        type2handler = standard_models_handler.type2handler
        materials = standard_models_handler.materials

        assert standard_models_handler.materials == materials

        # 检查处理器映射是否正确初始化
        assert standard_models_handler.type2handler == type2handler

        # 检查支持的材料类型是否注册
        registered_types = [mat_type for mat_type, h in type2handler.items() if h == standard_models_handler]
        assert len(registered_types) > 0

        # 检查是否包含了标准模型
        standard_models = [
            "ElasticIsotropic", "ElasticOrthotropic", "J2Plasticity", "DruckerPrager",
            "PlaneStress", "PlaneStrain", "MultiaxialCyclicPlasticity", "BoundingCamClay",
            "PlateFiber", "FSAM", "ManzariDafalias", "PM4Sand", "PM4Silt",
            "StressDensityModel", "AcousticMedium"
        ]

        for model in standard_models:
            assert model in registered_types

    def test_command_rules(self, standard_models_handler):
        """测试命令规则"""
        rules = standard_models_handler._COMMAND_RULES
        assert "nDMaterial" in rules

        # 测试一些特定材料类型的规则
        elastic_isotropic_rules = rules["nDMaterial"]["ElasticIsotropic"]
        assert "positional" in elastic_isotropic_rules
        assert elastic_isotropic_rules["positional"] == ["matType", "matTag", "E", "nu", "rho?"]

        elastic_orthotropic_rules = rules["nDMaterial"]["ElasticOrthotropic"]
        assert "positional" in elastic_orthotropic_rules

        j2_plasticity_rules = rules["nDMaterial"]["J2Plasticity"]
        assert "positional" in j2_plasticity_rules

    def test_handles(self, standard_models_handler):
        """测试handles方法"""
        commands = standard_models_handler.handles()
        assert commands == ["nDMaterial"]

    def test_handle_elastic_isotropic(self, standard_models_handler):
        """测试处理ElasticIsotropic材料"""
        # 模拟参数
        func_name = "nDMaterial"
        arg_map = {
            "matType": "ElasticIsotropic",
            "matTag": 1,
            "E": 2.0e5,
            "nu": 0.3,
            "rho": 7.85e-9
        }

        # 调用待测试方法
        standard_models_handler.handle(func_name, arg_map)

        # 验证结果
        materials = standard_models_handler.materials
        assert 1 in materials
        material = materials[1]
        assert material["matType"] == "ElasticIsotropic"
        assert material["matTag"] == 1
        assert material["E"] == 2.0e5
        assert material["nu"] == 0.3
        assert material["rho"] == 7.85e-9
        assert material["materialCommandType"] == "nDMaterial"

    def test_handle_elastic_orthotropic(self, standard_models_handler):
        """测试处理ElasticOrthotropic材料"""
        # 模拟参数
        func_name = "nDMaterial"
        arg_map = {
            "matType": "ElasticOrthotropic",
            "matTag": 2,
            "Ex": 2.0e5,
            "Ey": 1.5e5,
            "Ez": 1.8e5,
            "nu_xy": 0.25,
            "nu_yz": 0.3,
            "nu_zx": 0.3,
            "Gxy": 8.0e4,
            "Gyz": 7.5e4,
            "Gzx": 7.5e4,
            "rho": 7.85e-9
        }

        # 调用待测试方法
        standard_models_handler.handle(func_name, arg_map)

        # 验证结果
        materials = standard_models_handler.materials
        assert 2 in materials
        material = materials[2]
        assert material["matType"] == "ElasticOrthotropic"
        assert material["matTag"] == 2
        assert material["Ex"] == 2.0e5
        assert material["Ey"] == 1.5e5
        assert material["Ez"] == 1.8e5
        assert material["nu_xy"] == 0.25
        assert material["nu_yz"] == 0.3
        assert material["nu_zx"] == 0.3
        assert material["Gxy"] == 8.0e4
        assert material["Gyz"] == 7.5e4
        assert material["Gzx"] == 7.5e4
        assert material["rho"] == 7.85e-9
        assert material["materialCommandType"] == "nDMaterial"

    def test_handle_plane_stress(self, standard_models_handler):
        """测试处理PlaneStress材料"""
        # 模拟参数
        func_name = "nDMaterial"
        arg_map = {
            "matType": "PlaneStress",
            "matTag": 3,
            "mat3DTag": 1
        }

        # 调用待测试方法
        standard_models_handler.handle(func_name, arg_map)

        # 验证结果
        materials = standard_models_handler.materials
        assert 3 in materials
        material = materials[3]
        assert material["matType"] == "PlaneStress"
        assert material["matTag"] == 3
        assert material["mat3DTag"] == 1
        assert material["materialCommandType"] == "nDMaterial"

    def test_handle_pm4sand(self, standard_models_handler):
        """测试处理PM4Sand材料"""
        # 模拟参数（包含必须参数和可选参数）
        func_name = "nDMaterial"
        arg_map = {
            "matType": "PM4Sand",
            "matTag": 4,
            "D_r": 0.6,
            "G_o": 700,
            "h_po": 0.53,
            "Den": 1.8,
            "P_atm": 101.3,
            "h_o": 0.5,
            "e_max": 0.8,
            "e_min": 0.5
        }

        # 调用待测试方法
        standard_models_handler.handle(func_name, arg_map)

        # 验证结果
        materials = standard_models_handler.materials
        assert 4 in materials
        material = materials[4]
        assert material["matType"] == "PM4Sand"
        assert material["matTag"] == 4
        assert material["D_r"] == 0.6
        assert material["G_o"] == 700
        assert material["h_po"] == 0.53
        assert material["Den"] == 1.8
        assert material["P_atm"] == 101.3
        assert material["h_o"] == 0.5
        assert material["e_max"] == 0.8
        assert material["e_min"] == 0.5
        assert material["materialCommandType"] == "nDMaterial"

    def test_handle_unknown_material(self, standard_models_handler):
        """测试处理未知类型的材料"""
        # 模拟参数
        func_name = "nDMaterial"
        arg_map = {
            "matType": "CustomMaterial",
            "matTag": 5,
            "param1": 100,
            "param2": 200,
            "args": [300, 400]
        }

        # 调用待测试方法
        standard_models_handler.handle(func_name, arg_map)

        # 验证结果
        materials = standard_models_handler.materials
        assert 5 in materials
        material = materials[5]
        assert material["matType"] == "CustomMaterial"
        assert material["matTag"] == 5
        assert material["param1"] == 100
        assert material["param2"] == 200
        assert material["args"] == [300, 400]
        assert material["materialCommandType"] == "nDMaterial"

    def test_ignore_other_commands(self, standard_models_handler):
        """测试忽略非nDMaterial命令"""
        # 模拟参数
        func_name = "someOtherCommand"
        arg_map = {"matType": "ElasticIsotropic", "matTag": 6}

        # 调用待测试方法
        standard_models_handler.handle(func_name, arg_map)

        # 验证材料未被添加
        materials = standard_models_handler.materials
        assert len(materials) == 0


# pytest 不需要这部分代码
