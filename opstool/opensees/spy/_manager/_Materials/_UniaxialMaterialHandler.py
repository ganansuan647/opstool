from typing import Any, Dict

from .._BaseHandler import BaseHandler


class UniaxialMaterialHandler(BaseHandler):
    """
    处理单轴材料类型的处理器
    """

    def __init__(self, type2handler: Dict[str, BaseHandler], materials: Dict[int, Dict]):
        self.type2handler = type2handler
        self.materials = materials

        # 注册该处理器可以处理的材料类型
        supported_material_types = [
            # 钢材和钢筋材料
            "Steel01", "Steel02", "Steel4", "ReinforcingSteel", "Dodd_Restrepo",
            "RambergOsgoodSteel", "SteelMPF", "Steel01Thermal",

            # 混凝土材料
            "Concrete01", "Concrete02", "Concrete04", "Concrete06", "Concrete07",
            "Concrete01WithSITC", "ConfinedConcrete01", "ConcreteD", "FRPConfinedConcrete",
            "FRPConfinedConcrete02", "ConcreteCM", "TDConcrete", "TDConcreteEXP",
            "TDConcreteMC10", "TDConcreteMC10NL",

            # 标准单轴材料
            "Elastic", "ElasticPP", "ElasticPPGap", "ENT", "Hysteretic", "Parallel", "Series",

            # PyTzQz单轴材料
            "PySimple1", "TzSimple1", "QzSimple1", "PyLiq1", "TzLiq1", "QzLiq1",

            # 其他单轴材料
            "Hardening", "CastFuse", "ViscousDamper", "BilinearOilDamper", "Bilin",
            "ModIMKPeakOriented", "ModIMKPinching", "SAWS", "BarSlip", "Bond_SP01",
            "Fatigue", "Impact", "HyperbolicGap", "LimitState", "MinMax", "ElasticBilin",
            "ElasticMultiLinear", "MultiLinear", "InitialStrain", "InitialStress",
            "PathIndependent", "Pinching4", "ECC", "SelfCentering", "Viscous", "BoucWen",
            "BWBN", "KikuchiAikenHDR", "KikuchiAikenLRB", "AxialSp", "AxialSpHD",
            "PinchingLimitState", "CFSWSWP", "CFSSSWP", "Backbone", "Masonry", "Pipe"
        ]

        for mat_type in supported_material_types:
            self.type2handler[mat_type] = self

    @property
    def _COMMAND_RULES(self) -> Dict[str, Dict[str, Any]]:
        return {
            "uniaxialMaterial": {
                "positional": ["matType", "matTag", "args*"]
            }
        }

    @staticmethod
    def commands():
        return ["uniaxialMaterial"]
    
    @staticmethod
    def types():
        # 返回所有支持的单轴材料类型
        return [
            # 钢材和钢筋材料
            "Steel01", "Steel02", "Steel4", "ReinforcingSteel", "Dodd_Restrepo",
            "RambergOsgoodSteel", "SteelMPF", "Steel01Thermal",
            
            # 混凝土材料
            "Concrete01", "Concrete02", "Concrete04", "Concrete06", "Concrete07",
            "Concrete01WithSITC", "ConfinedConcrete01", "ConcreteD", "FRPConfinedConcrete",
            "FRPConfinedConcrete02", "ConcreteCM", "TDConcrete", "TDConcreteEXP",
            "TDConcreteMC10", "TDConcreteMC10NL",
            
            # 标准单轴材料
            "Elastic", "ElasticPP", "ElasticPPGap", "ENT", "Hysteretic", "Parallel", "Series",
            
            # PyTzQz单轴材料
            "PySimple1", "TzSimple1", "QzSimple1", "PyLiq1", "TzLiq1", "QzLiq1",
            
            # 其他单轴材料
            "Hardening", "CastFuse", "ViscousDamper", "BilinearOilDamper", "Bilin",
            "ModIMKPeakOriented", "ModIMKPinching", "SAWS", "BarSlip", "Bond_SP01",
            "Fatigue", "Impact", "HyperbolicGap", "LimitState", "MinMax", "ElasticBilin",
            "ElasticMultiLinear", "MultiLinear", "InitialStrain", "InitialStress",
            "PathIndependent", "Pinching4", "ECC", "SelfCentering", "Viscous", "BoucWen",
            "BWBN", "KikuchiAikenHDR", "KikuchiAikenLRB", "AxialSp", "AxialSpHD",
            "PinchingLimitState", "CFSWSWP", "CFSSSWP", "Backbone", "Masonry", "Pipe"
        ]
        
    @staticmethod
    def handles():
        # 保持向后兼容
        return ["uniaxialMaterial"]

    def handle(self, func_name: str, arg_map: Dict[str, Any]):
        """
        处理uniaxialMaterial命令
        """
        if func_name != "uniaxialMaterial":
            return

        matTag = int(arg_map.get("matTag"))
        matType = arg_map.get("matType")
        args = arg_map.get("args", [])

        # 构建材料信息字典
        mat_info = {
            "matType": matType,
            "matTag": matTag,
            "args": args,
            "materialCommandType": "uniaxialMaterial"
        }

        # 保存到数据仓库
        self.materials[matTag] = mat_info
