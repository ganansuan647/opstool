import openseespy.opensees as ops
import pytest

from opstool.opensees.spy import MaterialManager


@pytest.fixture
def material_manager() -> MaterialManager:
    """每个测试前初始化一个MaterialManager实例"""
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 6)
    return MaterialManager()


def test_handle_Hardening(material_manager: MaterialManager) -> None:
    """测试Hardening材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("Hardening", 1, 30000.0, 20.0, 10.0, 5.0, 0.3)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 1 in material_manager.materials
    material_data = material_manager.materials[1]
    assert material_data["matType"] == "Hardening"
    assert material_data["matTag"] == 1
    assert material_data["E"] == 30000.0
    assert material_data["sigmaY"] == 20.0
    assert material_data["H_iso"] == 10.0
    assert material_data["H_kin"] == 5.0
    assert material_data["eta"] == 0.3
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_Cast(material_manager: MaterialManager) -> None:
    """测试Cast材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("Cast", 2, 29000.0, 0.03, 0.04, 0.05, 500.0, 0.2, 2.0, 1.0, 0.3, 0.4, 1.0, 2.0, 0.35, 5000.0, 1.2)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 2 in material_manager.materials
    material_data = material_manager.materials[2]
    assert material_data["matType"] == "Cast"
    assert material_data["matTag"] == 2
    assert material_data["n"] == 29000.0
    assert material_data["bo"] == 0.03
    assert material_data["h1"] == 0.04
    assert material_data["h2"] == 0.05
    assert material_data["a1"] == 500.0
    assert material_data["a2"] == 0.2
    assert material_data["a3"] == 2.0
    assert material_data["a4"] == 1.0
    assert material_data["b1"] == 0.3
    assert material_data["b2"] == 0.4
    assert material_data["b3"] == 1.0
    assert material_data["b4"] == 2.0
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_ViscousDamper(material_manager: MaterialManager) -> None:
    """测试ViscousDamper材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("ViscousDamper", 3, 1.5, 1.0, 0.5, 0.5, 0.5, 2.0, 0.7)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 3 in material_manager.materials
    material_data = material_manager.materials[3]
    assert material_data["matType"] == "ViscousDamper"
    assert material_data["matTag"] == 3
    assert material_data["K_el"] == 1.5
    assert material_data["Cd"] == 1.0
    assert material_data["alpha"] == 0.5
    assert material_data["LGap"] == 0.5
    assert material_data["NM"] == 0.5
    assert material_data["RelTol"] == 2.0
    assert material_data["AbsTol"] == 0.7
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_BilinearOilDamper(material_manager: MaterialManager) -> None:
    """测试BilinearOilDamper材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("BilinearOilDamper", 4, 100.0, 20.0, 200.0, 10.0, 0.5, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 0.8, 2.0, 0.2)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 4 in material_manager.materials
    material_data = material_manager.materials[4]
    assert material_data["matType"] == "BilinearOilDamper"
    assert material_data["matTag"] == 4
    assert material_data["K_el"] == 100.0
    assert material_data["Cd"] == 20.0
    assert material_data["Fr"] == 200.0
    assert material_data["p"] == 10.0
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_Viscous(material_manager: MaterialManager) -> None:
    """测试Viscous材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("Viscous", 5, 15.0, 0.5)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 5 in material_manager.materials
    material_data = material_manager.materials[5]
    assert material_data["matType"] == "Viscous"
    assert material_data["matTag"] == 5
    assert material_data["C"] == 15.0
    assert material_data["alpha"] == 0.5
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_BoucWen(material_manager: MaterialManager) -> None:
    """测试BoucWen材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("BoucWen", 3, 2000.0, 50.0, 2.0, 0.75, 0.5, 0.5, 0.5, 10.0, 0.2)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 3 in material_manager.materials
    material_data = material_manager.materials[3]
    assert material_data["matType"] == "BoucWen"
    assert material_data["matTag"] == 3
    assert material_data["alpha"] == 2000.0
    assert material_data["ko"] == 50.0
    assert material_data["n"] == 2.0
    assert material_data["gamma"] == 0.75
    assert material_data["beta"] == 0.5
    assert material_data["Ao"] == 0.5
    assert material_data["deltaA"] == 0.5
    assert material_data["deltaNu"] == 10.0
    assert material_data["deltaEta"] == 0.2
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_BWBN(material_manager: MaterialManager) -> None:
    """测试BWBN材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("BWBN", 4, 100.0, 1.0, 1.0, 1.5, 0.5, 0.5, 0.5, 0.05, 1.0, 0.2, 0.3, 0.4, 0.5)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 4 in material_manager.materials
    material_data = material_manager.materials[4]
    assert material_data["matType"] == "BWBN"
    assert material_data["matTag"] == 4
    assert material_data["alpha"] == 100.0
    assert material_data["ko"] == 1.0
    assert material_data["n"] == 1.0
    assert material_data["gamma"] == 1.5
    assert material_data["beta"] == 0.5
    assert material_data["Ao"] == 0.5
    assert material_data["q"] == 0.5
    assert material_data["zetas"] == 0.05
    assert material_data["p"] == 1.0
    assert material_data["Shi"] == 0.2
    assert material_data["deltaShip"] == 0.3
    assert material_data["lamb"] == 0.4
    assert material_data["tol"] == 0.5
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_Bilin(material_manager: MaterialManager) -> None:
    """测试Bilin材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("Bilin", 6, 29000.0, 0.02, 0.1, 0.1, 1.0, 0.02, 0.3, 0.3, 1.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 6 in material_manager.materials
    material_data = material_manager.materials[6]
    assert material_data["matType"] == "Bilin"
    assert material_data["matTag"] == 6
    assert material_data["K0"] == 29000.0
    assert material_data["as_Plus"] == 0.02
    assert material_data["as_Neg"] == 0.1
    assert material_data["My_Plus"] == 0.1
    assert material_data["My_Neg"] == 1.0
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_SelfCentering(material_manager: MaterialManager) -> None:
    """测试SelfCentering材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("SelfCentering", 7, 100.0, 20.0, 0.5, 10.0, 0.6, 0.2, 5.0, 0.1, 0.8, 0.3, 0.1)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 7 in material_manager.materials
    material_data = material_manager.materials[7]
    assert material_data["matType"] == "SelfCentering"
    assert material_data["matTag"] == 7
    assert material_data["k1"] == 100.0
    assert material_data["k2"] == 20.0
    assert material_data["sig_act_p"] == 0.5
    assert material_data["sig_act_n"] == 10.0
    assert material_data["n1"] == 0.6
    assert material_data["n2"] == 0.2
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_KikuchiAikenHDR(material_manager: MaterialManager) -> None:
    """测试KikuchiAikenHDR材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("KikuchiAikenHDR", 5, 1, 200.0, 20.0, 5.0, 0.1, 0.1, 1.0, 10.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 8 in material_manager.materials
    material_data = material_manager.materials[8]
    assert material_data["matType"] == "KikuchiAikenHDR"
    assert material_data["matTag"] == 8
    assert material_data["tp"] == 1
    assert material_data["ar"] == 200.0
    assert material_data["hr"] == 20.0
    assert material_data["temp"] == 5.0
    assert material_data["rk"] == 0.1
    assert material_data["rq"] == 0.1
    assert material_data["rs"] == 1.0
    assert material_data["rf"] == 10.0
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_Pipe(material_manager: MaterialManager) -> None:
    """测试Pipe材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("Pipe", 11, 2, 20.0, 200000.0, 0.3, 1.2e-5, 100.0, 180000.0, 0.3, 1.3e-5)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 11 in material_manager.materials
    material_data = material_manager.materials[11]
    assert material_data["matType"] == "Pipe"
    assert material_data["matTag"] == 11
    assert material_data["nt"] == 2
    assert material_data["T1"] == 20.0
    assert material_data["E1"] == 200000.0
    assert material_data["xnu1"] == 0.3
    assert material_data["alpT1"] == 1.2e-5
    assert material_data["T2"] == 100.0
    assert material_data["E2"] == 180000.0
    assert material_data["xnu2"] == 0.3
    assert material_data["alpT2"] == 1.3e-5
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_Backbone(material_manager: MaterialManager) -> None:
    """测试Backbone材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("Backbone", 12, 13)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 12 in material_manager.materials
    material_data = material_manager.materials[12]
    assert material_data["matType"] == "Backbone"
    assert material_data["matTag"] == 12
    assert material_data["matTag1"] == 13
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_PinchingLimitStateMaterial(material_manager: MaterialManager) -> None:
    """测试PinchingLimitStateMaterial材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("PinchingLimitStateMaterial", 14, 0.05, 0.15, 0.15, 0.15, 0.0, 0.0, 0.3, 1.0, 0.25, 0.05,
            0.5, 0.05, 0.5, 0.0, 0.9, 0.15, 0.0, 0.08, 0.08, 0.0, 0.1, 0.0, 0.0, 1, 0.0, 0.0, 0.0,
            2, 100, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 14 in material_manager.materials
    material_data = material_manager.materials[14]
    assert material_data["matType"] == "PinchingLimitStateMaterial"
    assert material_data["matTag"] == 14
    assert material_data["stress1p"] == 0.05
    assert material_data["strain1p"] == 0.15
    assert material_data["stress2p"] == 0.15
    assert material_data["strain2p"] == 0.15
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_unknown_other_uniaxial_material(material_manager: MaterialManager) -> None:
    """测试处理未知的单轴材料"""
    cmd = "uniaxialMaterial"
    args = ("CustomUniaxialMaterial", 20, 10.0, 20.0, 30.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 20 in material_manager.materials
    material_data = material_manager.materials[20]
    assert material_data["matType"] == "CustomUniaxialMaterial"
    assert material_data["matTag"] == 20
    assert material_data["materialType"] == cmd
    assert "args" in material_data  # 未知材料应该将额外参数保存在args中


def test_handle_CFSWSWP(material_manager: MaterialManager) -> None:
    """测试CFSWSWP材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("CFSWSWP", 15, 100.0, 1.0, 0.5, 0.7, 0.3, 2.5, 0.6, 0.8, 0.2, 0.15, 0.3, 0.2, 0.1, 0.2, 0.15)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 15 in material_manager.materials
    material_data = material_manager.materials[15]
    assert material_data["matType"] == "CFSWSWP"
    assert material_data["matTag"] == 15
    assert material_data["height"] == 100.0
    assert material_data["width"] == 1.0
    assert material_data["fuf"] == 0.5
    assert material_data["fyf"] == 0.7
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_CFSSSWP(material_manager: MaterialManager) -> None:
    """测试CFSSSWP材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("CFSSSWP", 16, 100.0, 1.0, 0.5, 0.7, 0.3, 2.5, 0.6, 0.8, 0.2, 0.15, 0.3, 0.2, 0.1, 0.2, 0.15)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 16 in material_manager.materials
    material_data = material_manager.materials[16]
    assert material_data["matType"] == "CFSSSWP"
    assert material_data["matTag"] == 16
    assert material_data["height"] == 100.0
    assert material_data["width"] == 1.0
    assert material_data["fuf"] == 0.5
    assert material_data["fyf"] == 0.7
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_Masonry(material_manager: MaterialManager) -> None:
    """测试Masonry材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("Masonry", 17, 1000.0, 2000.0, 0.05, 0.003, 0.001, 0.3, 0.7, 2.0, 100.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 17 in material_manager.materials
    material_data = material_manager.materials[17]
    assert material_data["matType"] == "Masonry"
    assert material_data["matTag"] == 17
    assert material_data["E1"] == 1000.0
    assert material_data["E2"] == 2000.0
    assert material_data["d1"] == 0.05
    assert material_data["d2"] == 0.003
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_ModIMKPeakOriented(material_manager: MaterialManager) -> None:
    """测试ModIMKPeakOriented材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("ModIMKPeakOriented", 21, 29000.0, 0.02, 0.1, 0.1, 1.0, 0.02, 0.3, 0.3, 1.0, 0.1, 0.2, 0.3, 0.4, 0.5)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 21 in material_manager.materials
    material_data = material_manager.materials[21]
    assert material_data["matType"] == "ModIMKPeakOriented"
    assert material_data["matTag"] == 21
    assert material_data["K0"] == 29000.0
    assert material_data["as_Plus"] == 0.02
    assert material_data["as_Neg"] == 0.1
    assert material_data["My_Plus"] == 0.1
    assert material_data["My_Neg"] == 1.0
    assert material_data["LamdaS"] == 0.02
    assert material_data["LamdaC"] == 0.3
    assert material_data["LamdaA"] == 0.3
    assert material_data["LamdaK"] == 1.0
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_ModIMKPinching(material_manager: MaterialManager) -> None:
    """测试ModIMKPinching材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("ModIMKPinching", 22, 29000.0, 0.02, 0.1, 0.1, 1.0, 0.02, 0.3, 0.3, 1.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 22 in material_manager.materials
    material_data = material_manager.materials[22]
    assert material_data["matType"] == "ModIMKPinching"
    assert material_data["matTag"] == 22
    assert material_data["K0"] == 29000.0
    assert material_data["as_Plus"] == 0.02
    assert material_data["as_Neg"] == 0.1
    assert material_data["My_Plus"] == 0.1
    assert material_data["My_Neg"] == 1.0
    assert material_data["LamdaS"] == 0.02
    assert material_data["LamdaC"] == 0.3
    assert material_data["LamdaA"] == 0.3
    assert material_data["LamdaK"] == 1.0
    assert material_data["FprPos"] == 0.1
    assert material_data["FprNeg"] == 0.2
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_SAWS(material_manager: MaterialManager) -> None:
    """测试SAWS材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("SAWS", 23, 1.0, 2.0, 3.0, 4.0, 0.5, 0.6, 0.7, 0.8, 0.9, 0.1)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 23 in material_manager.materials
    material_data = material_manager.materials[23]
    assert material_data["matType"] == "SAWS"
    assert material_data["matTag"] == 23
    assert material_data["F0"] == 1.0
    assert material_data["FI"] == 2.0
    assert material_data["DU"] == 3.0
    assert material_data["S0"] == 4.0
    assert material_data["R1"] == 0.5
    assert material_data["R2"] == 0.6
    assert material_data["R3"] == 0.7
    assert material_data["R4"] == 0.8
    assert material_data["alpha"] == 0.9
    assert material_data["beta"] == 0.1
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_BarSlip(material_manager: MaterialManager) -> None:
    """测试BarSlip材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("BarSlip", 24, 30.0, 60000.0, 29000.0, 90000.0, 29000.0, 1.0, 24.0, 2, 24.0, 18.0, 1.0, 1, 1, "Damage", "psi")
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 24 in material_manager.materials
    material_data = material_manager.materials[24]
    assert material_data["matType"] == "BarSlip"
    assert material_data["matTag"] == 24
    assert material_data["fc"] == 30.0
    assert material_data["fy"] == 60000.0
    assert material_data["Es"] == 29000.0
    assert material_data["fu"] == 90000.0
    assert material_data["Eh"] == 29000.0
    assert material_data["db"] == 1.0
    assert material_data["ld"] == 24.0
    assert material_data["nb"] == 2
    assert material_data["depth"] == 24.0
    assert material_data["height"] == 18.0
    assert material_data["ancLratio"] == 1.0
    assert material_data["bsFlag"] == 1
    assert material_data["type"] == 1
    assert material_data["damage"] == "Damage"
    assert material_data["unit"] == "psi"
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_Bond_SP01(material_manager: MaterialManager) -> None:
    """测试Bond_SP01材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("Bond_SP01", 25, 600.0, 0.4, 1000.0, 0.9, 0.5, 0.5)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 25 in material_manager.materials
    material_data = material_manager.materials[25]
    assert material_data["matType"] == "Bond_SP01"
    assert material_data["matTag"] == 25
    assert material_data["Fy"] == 600.0
    assert material_data["Sy"] == 0.4
    assert material_data["Fu"] == 1000.0
    assert material_data["Su"] == 0.9
    assert material_data["b"] == 0.5
    assert material_data["R"] == 0.5
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_Fatigue(material_manager: MaterialManager) -> None:
    """测试Fatigue材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("Fatigue", 26, 1, "-E0", 0.191, "-m", -0.458, "-min", -1e16, "-max", 1e16)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 26 in material_manager.materials
    material_data = material_manager.materials[26]
    assert material_data["matType"] == "Fatigue"
    assert material_data["matTag"] == 26
    assert material_data["otherTag"] == 1
    assert material_data["-E0"] == 0.191
    assert material_data["E0"] == 0.191
    assert material_data["-m"] == -0.458
    assert material_data["m"] == -0.458
    assert material_data["-min"] == -1e16
    assert material_data["min"] == -1e16
    assert material_data["-max"] == 1e16
    assert material_data["max"] == 1e16
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_ImpactMaterial(material_manager: MaterialManager) -> None:
    """测试ImpactMaterial材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("ImpactMaterial", 27, 5.0e6, 5.0e5, 1.0e6, 1.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 27 in material_manager.materials
    material_data = material_manager.materials[27]
    assert material_data["matType"] == "ImpactMaterial"
    assert material_data["matTag"] == 27
    assert material_data["K1"] == 5.0e6
    assert material_data["K2"] == 5.0e5
    assert material_data["sigy"] == 1.0e6
    assert material_data["gap"] == 1.0
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_HyperbolicGapMaterial(material_manager: MaterialManager) -> None:
    """测试HyperbolicGapMaterial材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("HyperbolicGapMaterial", 28, 1000.0, 500.0, 0.7, 1000.0, 0.5)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 28 in material_manager.materials
    material_data = material_manager.materials[28]
    assert material_data["matType"] == "HyperbolicGapMaterial"
    assert material_data["matTag"] == 28
    assert material_data["Kmax"] == 1000.0
    assert material_data["Kur"] == 500.0
    assert material_data["Rf"] == 0.7
    assert material_data["Fult"] == 1000.0
    assert material_data["gap"] == 0.5
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_LimitState(material_manager: MaterialManager) -> None:
    """测试LimitState材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("LimitState", 29, 0.5, 0.01, 0.6, 0.02, 0.1, 0.05, -0.5, -0.01, -0.6, -0.02, -0.1, -0.05, 0.8, 0.8, 0.0, 0.0, 0.0, 0, 0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 29 in material_manager.materials
    material_data = material_manager.materials[29]
    assert material_data["matType"] == "LimitState"
    assert material_data["matTag"] == 29
    assert material_data["s1p"] == 0.5
    assert material_data["e1p"] == 0.01
    assert material_data["s2p"] == 0.6
    assert material_data["e2p"] == 0.02
    assert material_data["s3p"] == 0.1
    assert material_data["e3p"] == 0.05
    assert material_data["s1n"] == -0.5
    assert material_data["e1n"] == -0.01
    assert material_data["s2n"] == -0.6
    assert material_data["e2n"] == -0.02
    assert material_data["s3n"] == -0.1
    assert material_data["e3n"] == -0.05
    assert material_data["pinchX"] == 0.8
    assert material_data["pinchY"] == 0.8
    assert material_data["damage1"] == 0.0
    assert material_data["damage2"] == 0.0
    assert material_data["beta"] == 0.0
    assert material_data["curveTag"] == 0
    assert material_data["curveType"] == 0
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_MinMax(material_manager: MaterialManager) -> None:
    """测试MinMax材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("MinMax", 30, 1, "-min", -0.01, "-max", 0.01)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 30 in material_manager.materials
    material_data = material_manager.materials[30]
    assert material_data["matType"] == "MinMax"
    assert material_data["matTag"] == 30
    assert material_data["otherTag"] == 1
    assert material_data["-min"] == -0.01
    assert material_data["minStrain"] == -0.01
    assert material_data["-max"] == 0.01
    assert material_data["maxStrain"] == 0.01
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_ElasticBilin(material_manager: MaterialManager) -> None:
    """测试ElasticBilin材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("ElasticBilin", 31, 29000.0, 5000.0, 0.01)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 31 in material_manager.materials
    material_data = material_manager.materials[31]
    assert material_data["matType"] == "ElasticBilin"
    assert material_data["matTag"] == 31
    assert material_data["EP1"] == 29000.0
    assert material_data["EP2"] == 5000.0
    assert material_data["epsP2"] == 0.01
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_ElasticMultiLinear(material_manager: MaterialManager) -> None:
    """测试ElasticMultiLinear材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("ElasticMultiLinear", 32, 0.5, "-strain", -0.02, 0.0, 0.02, "-stress", -50.0, 0.0, 50.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 32 in material_manager.materials
    material_data = material_manager.materials[32]
    assert material_data["matType"] == "ElasticMultiLinear"
    assert material_data["matTag"] == 32
    assert material_data["eta"] == 0.5
    assert material_data["-strain"] == -0.02
    assert material_data["-stress"] == -50.0
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_MultiLinear(material_manager: MaterialManager) -> None:
    """测试MultiLinear材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("MultiLinear", 33, "-strain", -0.02, 0.0, 0.02, "-stress", -50.0, 0.0, 50.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 33 in material_manager.materials
    material_data = material_manager.materials[33]
    assert material_data["matType"] == "MultiLinear"
    assert material_data["matTag"] == 33
    assert material_data["-strain"] == -0.02
    assert material_data["-stress"] == -50.0
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_InitStrainMaterial(material_manager: MaterialManager) -> None:
    """测试InitStrainMaterial材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("InitStrainMaterial", 34, 1, 0.005)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 34 in material_manager.materials
    material_data = material_manager.materials[34]
    assert material_data["matType"] == "InitStrainMaterial"
    assert material_data["matTag"] == 34
    assert material_data["otherTag"] == 1
    assert material_data["initStrain"] == 0.005
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_InitStressMaterial(material_manager: MaterialManager) -> None:
    """测试InitStressMaterial材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("InitStressMaterial", 35, 1, 100.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 35 in material_manager.materials
    material_data = material_manager.materials[35]
    assert material_data["matType"] == "InitStressMaterial"
    assert material_data["matTag"] == 35
    assert material_data["otherTag"] == 1
    assert material_data["initStress"] == 100.0
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_PathIndependent(material_manager: MaterialManager) -> None:
    """测试PathIndependent材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("PathIndependent", 36, 1)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 36 in material_manager.materials
    material_data = material_manager.materials[36]
    assert material_data["matType"] == "PathIndependent"
    assert material_data["matTag"] == 36
    assert material_data["otherTag"] == 1
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_Pinching4(material_manager: MaterialManager) -> None:
    """测试Pinching4材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("Pinching4", 37, 10.0, 15.0, 0.5, 0.4, 0.2, 0.3, 0.1, 0.3, 0.1, 0.3, 1.0, 0.0, 0.1, 1.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 37 in material_manager.materials
    material_data = material_manager.materials[37]
    assert material_data["matType"] == "Pinching4"
    assert material_data["matTag"] == 37
    assert material_data["ePf1"] == 10.0
    assert material_data["ePf2"] == 15.0
    assert material_data["ePf3"] == 0.5
    assert material_data["ePf4"] == 0.4
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_ECC01(material_manager: MaterialManager) -> None:
    """测试ECC01材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("ECC01", 38, 30000.0, 2.0, 0.002, 0, 0.3, 20)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 38 in material_manager.materials
    material_data = material_manager.materials[38]
    assert material_data["matType"] == "ECC01"
    assert material_data["matTag"] == 38
    assert material_data["sigt0"] == 30000.0
    assert material_data["epst0"] == 2.0
    assert material_data["sigt1"] == 0.002
    assert material_data["epst1"] == 0
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_KikuchiAikenLRB(material_manager: MaterialManager) -> None:
    """测试KikuchiAikenLRB材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("KikuchiAikenLRB", 39, 1, 100.0, 10.0, 20.0, 0.1, 0.01, 0.5, 2.0, 0.5, 0.2, 0.2)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 39 in material_manager.materials
    material_data = material_manager.materials[39]
    assert material_data["matType"] == "KikuchiAikenLRB"
    assert material_data["matTag"] == 39
    assert material_data["type"] == 1
    assert material_data["ar"] == 100.0
    assert material_data["hr"] == 10.0
    assert material_data["gr"] == 20.0
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_AxialSp(material_manager: MaterialManager) -> None:
    """测试AxialSp材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("AxialSp", 40, 100.0, 10.0, 1.0, 0.2, 0.3, 0.1, 0.4, 0.5, 0.1, 5, 1.0, 0.5)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 40 in material_manager.materials
    material_data = material_manager.materials[40]
    assert material_data["matType"] == "AxialSp"
    assert material_data["matTag"] == 40
    assert material_data["sce"] == 100.0
    assert material_data["fty"] == 10.0
    assert material_data["fcy"] == 1.0
    assert material_data["bte"] == 0.2
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_AxialSpHD(material_manager: MaterialManager) -> None:
    """测试AxialSpHD材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("AxialSpHD", 41, 100.0, 10.0, 1.0, 0.2, 0.3, 0.1, 0.4, 0.5, 0.1, 5, 1.0, 0.5, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 41 in material_manager.materials
    material_data = material_manager.materials[41]
    assert material_data["matType"] == "AxialSpHD"
    assert material_data["matTag"] == 41
    assert material_data["sce"] == 100.0
    assert material_data["fty"] == 10.0
    assert material_data["fcy"] == 1.0
    assert material_data["bte"] == 0.2
    assert material_data["materialCommandType"] == "uniaxialMaterial"
