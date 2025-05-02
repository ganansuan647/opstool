import openseespy.opensees as ops
import pytest

from opstool.opensees.spy import MaterialManager


@pytest.fixture
def material_manager() -> MaterialManager:
    """每个测试前初始化一个MaterialManager实例"""
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 6)
    return MaterialManager()


def test_handle_Steel01(material_manager: MaterialManager) -> None:
    """测试Steel01材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("Steel01", 1, 420.0, 200000.0, 0.01, 0.5, 1.0, 0.0, 1.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 1 in material_manager.materials
    material_data = material_manager.materials[1]
    assert material_data["matType"] == "Steel01"
    assert material_data["matTag"] == 1
    assert material_data["Fy"] == 420.0
    assert material_data["E0"] == 200000.0
    assert material_data["b"] == 0.01
    assert material_data["a1"] == 0.5
    assert material_data["a2"] == 1.0
    assert material_data["a3"] == 0.0
    assert material_data["a4"] == 1.0


def test_handle_Steel02(material_manager: MaterialManager) -> None:
    """测试Steel02材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("Steel02", 2, 420.0, 200000.0, 0.01, 15.0, 0.925, 0.15, 0.5, 1.0, 0.0, 1.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 2 in material_manager.materials
    material_data = material_manager.materials[2]
    assert material_data["matType"] == "Steel02"
    assert material_data["matTag"] == 2
    assert material_data["Fy"] == 420.0
    assert material_data["E0"] == 200000.0
    assert material_data["b"] == 0.01
    assert material_data["R0"] == 15.0
    assert material_data["cR1"] == 0.925
    assert material_data["cR2"] == 0.15
    assert material_data["a1"] == 0.5
    assert material_data["a2"] == 1.0
    assert material_data["a3"] == 0.0
    assert material_data["a4"] == 1.0


def test_handle_Steel4(material_manager: MaterialManager) -> None:
    """测试Steel4材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("Steel4", 3, 420.0, 200000.0, 0.01)
    kwargs = {
        "R0": 20.0, 
        "cR1": 0.925, 
        "cR2": 0.15
    }
    material_manager.handle(cmd, {"args": args, "kwargs": kwargs})

    # 检查材料是否正确存储
    assert 3 in material_manager.materials
    material_data = material_manager.materials[3]
    assert material_data["matType"] == "Steel4"
    assert material_data["matTag"] == 3
    assert material_data["Fy"] == 420.0
    assert material_data["E0"] == 200000.0
    assert material_data["b"] == 0.01
    assert material_data["R0"] == 20.0
    assert material_data["cR1"] == 0.925
    assert material_data["cR2"] == 0.15


def test_handle_ReinforcingSteel(material_manager: MaterialManager) -> None:
    """测试ReinforcingSteel材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("ReinforcingSteel", 4, 420.0, 525.0, 200000.0, 10000.0, 0.02, 0.1, 0.3, 0.3, 10.0, 1.0, 1.0, 0.5)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 4 in material_manager.materials
    material_data = material_manager.materials[4]
    assert material_data["matType"] == "ReinforcingSteel"
    assert material_data["matTag"] == 4
    assert material_data["fy"] == 420.0
    assert material_data["fu"] == 525.0
    assert material_data["Es"] == 200000.0
    assert material_data["Esh"] == 10000.0
    assert material_data["eps_sh"] == 0.02
    assert material_data["eps_ult"] == 0.1
    assert material_data["rel_reloading"] == 0.3
    assert material_data["rel_unloading"] == 0.3
    assert material_data["lsr"] == 10.0
    assert material_data["beta"] == 1.0
    assert material_data["r"] == 1.0
    assert material_data["gama"] == 0.5


def test_handle_Dodd_Restrepo(material_manager: MaterialManager) -> None:
    """测试Dodd_Restrepo材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("Dodd_Restrepo", 5, 420.0, 525.0, 0.02, 0.1, 200000.0, 0.015, 460.0, 1.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 5 in material_manager.materials
    material_data = material_manager.materials[5]
    assert material_data["matType"] == "Dodd_Restrepo"
    assert material_data["matTag"] == 5
    assert material_data["Fy"] == 420.0
    assert material_data["Fsu"] == 525.0
    assert material_data["ESH"] == 0.02
    assert material_data["ESU"] == 0.1
    assert material_data["Youngs"] == 200000.0
    assert material_data["ESHI"] == 0.015
    assert material_data["FSHI"] == 460.0
    assert material_data["OmegaFac"] == 1.0


def test_handle_RambergOsgoodSteel(material_manager: MaterialManager) -> None:
    """测试RambergOsgoodSteel材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("RambergOsgoodSteel", 6, 420.0, 200000.0, 0.7, 8.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 6 in material_manager.materials
    material_data = material_manager.materials[6]
    assert material_data["matType"] == "RambergOsgoodSteel"
    assert material_data["matTag"] == 6
    assert material_data["fy"] == 420.0
    assert material_data["E0"] == 200000.0
    assert material_data["a"] == 0.7
    assert material_data["n"] == 8.0


def test_handle_SteelMPF(material_manager: MaterialManager) -> None:
    """测试SteelMPF材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("SteelMPF", 7, 420.0, -420.0, 200000.0, 0.01, 0.01, [10, 0.925, 0.15], 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 7 in material_manager.materials
    material_data = material_manager.materials[7]
    assert material_data["matType"] == "SteelMPF"
    assert material_data["matTag"] == 7
    assert material_data["fyp"] == 420.0
    assert material_data["fyn"] == -420.0
    assert material_data["E0"] == 200000.0
    assert material_data["bp"] == 0.01
    assert material_data["bn"] == 0.01
    assert material_data["params"] == [10, 0.925, 0.15]
    assert material_data["a1"] == 0.0
    assert material_data["a2"] == 1.0
    assert material_data["a3"] == 0.0
    assert material_data["a4"] == 1.0


def test_handle_Steel01Thermal(material_manager: MaterialManager) -> None:
    """测试Steel01Thermal材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("Steel01Thermal", 8, 420.0, 200000.0, 0.01, 0.5, 1.0, 0.0, 1.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 8 in material_manager.materials
    material_data = material_manager.materials[8]
    assert material_data["matType"] == "Steel01Thermal"
    assert material_data["matTag"] == 8
    assert material_data["Fy"] == 420.0
    assert material_data["E0"] == 200000.0
    assert material_data["b"] == 0.01
    assert material_data["a1"] == 0.5
    assert material_data["a2"] == 1.0
    assert material_data["a3"] == 0.0
    assert material_data["a4"] == 1.0


def test_handle_unknown_steel_material(material_manager: MaterialManager) -> None:
    """测试处理未知的钢材材料"""
    cmd = "uniaxialMaterial"
    args = ("CustomSteelMaterial", 9, 420.0, 200000.0, 0.01)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 9 in material_manager.materials
    material_data = material_manager.materials[9]
    assert material_data["matType"] == "CustomSteelMaterial"
    assert material_data["matTag"] == 9
    assert material_data["materialType"] == cmd
    assert "args" in material_data  # 未知材料应该将额外参数保存在args中
