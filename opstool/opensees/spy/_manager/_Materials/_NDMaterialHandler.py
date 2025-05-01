from typing import Any

from .._BaseHandler import BaseHandler
from ._StandardModelsHandler import StandardModelsHandler


class NDMaterialHandler(BaseHandler):
    """
    处理多维材料类型的处理器
    作为材料处理的主入口, 根据不同材料类型分发到对应子处理器
    """

    def __init__(self, type2handler: dict[str, BaseHandler], materials: dict[int, dict]):
        self.type2handler = type2handler
        self.materials = materials

        # 初始化标准模型处理器
        self.standard_models_handler = StandardModelsHandler(type2handler, materials)

        # 注册该处理器可以处理的材料类型
        # 特定材料模型不在这里注册, 而是由各个子处理器负责注册
        supported_material_types = [
            # 清华沙土模型
            "CycLiqCP", "CycLiqCPSP",

            # 混凝土墙体建模材料
            "PlateFromPlaneStress", "PlateRebar", "PlasticDamageConcretePlaneStress",

            # 2D和3D接触材料
            "ContactMaterial2D", "ContactMaterial3D",

            # 初始状态分析包装材料
            "InitialStateAnalysisWrapper", "InitialStressMaterial", "InitialStrainMaterial",

            # UC San Diego土壤模型
            "PressureIndependMultiYield", "PressureDependMultiYield",
            "PressureDependMultiYield02", "PressureDependMultiYield03",

            # UC San Diego饱和非排水土壤
            "FluidSolidPorousMaterial"
        ]

        for mat_type in supported_material_types:
            self.type2handler[mat_type] = self

    @property
    def _COMMAND_RULES(self) -> dict[str, dict[str, Any]]:
        return {
            "nDMaterial": {
                "positional": ["matType", "matTag", "args*"]
            }
        }

    @staticmethod
    def commands():
        return ["nDMaterial"]
    
    @staticmethod
    def types():
        # 返回支持的多维材料类型
        return [
            # 清华沙土模型
            "CycLiqCP", "CycLiqCPSP",
            
            # 混凝土墙体建模材料
            "PlateFromPlaneStress", "PlateRebar", "PlasticDamageConcretePlaneStress",
            
            # 2D和3D接触材料
            "ContactMaterial2D", "ContactMaterial3D",
            
            # 初始状态分析包装材料
            "InitialStateAnalysisWrapper", "InitialStressMaterial", "InitialStrainMaterial",
            
            # UC San Diego土壤模型
            "PressureIndependMultiYield", "PressureDependMultiYield",
            "PressureDependMultiYield02", "PressureDependMultiYield03",
            
            # UC San Diego饱和非排水土壤
            "FluidSolidPorousMaterial",
            
            # 标准模型
            "ElasticIsotropic", "ElasticOrthotropic", "J2Plasticity", "DruckerPrager",
            "PlaneStress", "PlaneStrain", "MultiaxialCyclicPlasticity", "BoundingCamClay",
            "PlateFiber", "FSAM", "ManzariDafalias", "PM4Sand", "PM4Silt",
            "StressDensityModel", "AcousticMedium"
        ]
    
    @staticmethod
    def handles():
        # 保持向后兼容
        return ["nDMaterial"]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        """
        处理nDMaterial命令
        根据材料类型将处理分发到对应的处理器
        """
        if func_name != "nDMaterial":
            return

        matType = arg_map.get("matType")
        handler = self.type2handler.get(matType)

        # 如果找到了特定处理器, 则交由该处理器处理
        if handler and handler is not self:
            handler.handle(func_name, arg_map)
        else:
            # 否则使用基本处理逻辑
            matTag = int(arg_map.get("matTag"))
            args = arg_map.get("args", [])

            # 构建材料信息字典
            mat_info = {
                "matType": matType,
                "matTag": matTag,
                "args": args,
                "materialCommandType": "nDMaterial"
            }

            # 保存到数据仓库
            self.materials[matTag] = mat_info
