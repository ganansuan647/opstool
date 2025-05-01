from typing import Any

from .._BaseHandler import BaseHandler


class StandardModelsHandler(BaseHandler):
    """
    处理NDMaterial标准模型的处理器
    包括: ElasticIsotropic, ElasticOrthotropic, J2Plasticity, DruckerPrager,
    PlaneStress, PlaneStrain, MultiaxialCyclicPlasticity, BoundingCamClay,
    PlateFiber, FSAM, ManzariDafalias, PM4Sand, PM4Silt, StressDensityModel, AcousticMedium
    """

    def __init__(self, type2handler: dict[str, BaseHandler], materials: dict[int, dict]):
        self.type2handler = type2handler
        self.materials = materials

        # 注册该处理器可以处理的材料类型
        supported_material_types = [
            # 标准模型
            "ElasticIsotropic", "ElasticOrthotropic", "J2Plasticity", "DruckerPrager",
            "PlaneStress", "PlaneStrain", "MultiaxialCyclicPlasticity", "BoundingCamClay",
            "PlateFiber", "FSAM", "ManzariDafalias", "PM4Sand", "PM4Silt",
            "StressDensityModel", "AcousticMedium"
        ]

        for mat_type in supported_material_types:
            self.type2handler[mat_type] = self

    @property
    def _COMMAND_RULES(self) -> dict[str, dict[str, Any]]:
        return {
            "nDMaterial": {
                "ElasticIsotropic": {
                    "positional": ["matType", "matTag", "E", "nu", "rho?"]
                },
                "ElasticOrthotropic": {
                    "positional": ["matType", "matTag", "Ex", "Ey", "Ez", "nu_xy", "nu_yz", "nu_zx", "Gxy", "Gyz", "Gzx", "rho?"]
                },
                "J2Plasticity": {
                    "positional": ["matType", "matTag", "K", "G", "sig0", "sigInf", "delta", "H"]
                },
                "DruckerPrager": {
                    "positional": ["matType", "matTag", "K", "G", "sigmaY", "rho", "rhoBar", "Kinf", "Ko", "delta1", "delta2", "H", "theta", "density", "atmPressure?"]
                },
                "PlaneStress": {
                    "positional": ["matType", "matTag", "mat3DTag"]
                },
                "PlaneStrain": {
                    "positional": ["matType", "matTag", "mat3DTag"]
                },
                "MultiaxialCyclicPlasticity": {
                    "positional": ["matType", "matTag", "rho", "K", "G", "Su", "Ho", "h", "m", "beta", "KCoeff"]
                },
                "BoundingCamClay": {
                    "positional": ["matType", "matTag", "massDensity", "C", "bulkMod", "OCR", "mu_o", "alpha", "lambda", "h", "m"]
                },
                "PlateFiber": {
                    "positional": ["matType", "matTag", "threeDTag"]
                },
                "FSAM": {
                    "positional": ["matType", "matTag", "rho", "sXTag", "sYTag", "concTag", "rouX", "rouY", "nu", "alfadow"]
                },
                "ManzariDafalias": {
                    "positional": ["matType", "matTag", "G0", "nu", "e_init", "Mc", "c", "lambda_c", "e0", "ksi", "P_atm", "m", "h0", "ch", "nb", "A0", "nd", "z_max", "cz", "Den"]
                },
                "PM4Sand": {
                    "positional": ["matType", "matTag", "D_r", "G_o", "h_po", "Den", "P_atm?", "h_o?", "e_max?", "e_min?", "n_b?", "n_d?", "A_do?", "z_max?", "c_z?", "c_e?", "phi_cv?", "nu?", "g_degr?", "c_dr?", "c_kaf?", "Q_bolt?", "R_bolt?", "m_par?", "F_sed?", "p_sed?"]
                },
                "PM4Silt": {
                    "positional": ["matType", "matTag", "S_u", "Su_Rat", "G_o", "h_po", "Den", "Su_factor?", "P_atm?", "nu?", "nG?", "h0?", "eInit?", "lambda?", "phicv?", "nb_wet?", "nb_dry?", "nd?", "Ado?", "ru_max?", "z_max?", "cz?", "ce?", "cgd?", "ckaf?", "m_m?", "CG_consol?"]
                },
                "StressDensityModel": {
                    "positional": ["matType", "matTag", "mDen", "eNot", "A", "n", "nu", "a1", "b1", "a2", "b2", "a3", "b3", "fd", "muNot", "muCyc", "sc", "M", "patm", "ssls*", "hsl", "p1"]
                },
                "AcousticMedium": {
                    "positional": ["matType", "matTag", "K", "rho"]
                }
            }
        }

    @staticmethod
    def handles():
        return ["nDMaterial"]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        """
        处理标准模型的nDMaterial命令
        """
        if func_name != "nDMaterial":
            return

        matTag = int(arg_map.get("matTag"))
        matType = arg_map.get("matType")

        # 根据不同的材料类型构建特定的材料信息
        mat_info = self._build_material_info(matType, matTag, arg_map)

        # 保存到数据仓库
        self.materials[matTag] = mat_info

    def _build_material_info(self, matType: str, matTag: int, arg_map: dict[str, Any]) -> dict[str, Any]:
        """
        根据材料类型构建材料信息
        """
        base_info = {
            "matType": matType,
            "matTag": matTag,
            "materialCommandType": "nDMaterial"
        }

        # 为不同类型的材料构建专用的信息字典
        if matType == "ElasticIsotropic":
            specific_info = {
                "E": arg_map.get("E"),
                "nu": arg_map.get("nu"),
                "rho": arg_map.get("rho", 0.0)
            }
        elif matType == "ElasticOrthotropic":
            specific_info = {
                "Ex": arg_map.get("Ex"),
                "Ey": arg_map.get("Ey"),
                "Ez": arg_map.get("Ez"),
                "nu_xy": arg_map.get("nu_xy"),
                "nu_yz": arg_map.get("nu_yz"),
                "nu_zx": arg_map.get("nu_zx"),
                "Gxy": arg_map.get("Gxy"),
                "Gyz": arg_map.get("Gyz"),
                "Gzx": arg_map.get("Gzx"),
                "rho": arg_map.get("rho", 0.0)
            }
        elif matType == "J2Plasticity":
            specific_info = {
                "K": arg_map.get("K"),
                "G": arg_map.get("G"),
                "sig0": arg_map.get("sig0"),
                "sigInf": arg_map.get("sigInf"),
                "delta": arg_map.get("delta"),
                "H": arg_map.get("H")
            }
        elif matType == "DruckerPrager":
            specific_info = {
                "K": arg_map.get("K"),
                "G": arg_map.get("G"),
                "sigmaY": arg_map.get("sigmaY"),
                "rho": arg_map.get("rho"),
                "rhoBar": arg_map.get("rhoBar"),
                "Kinf": arg_map.get("Kinf"),
                "Ko": arg_map.get("Ko"),
                "delta1": arg_map.get("delta1"),
                "delta2": arg_map.get("delta2"),
                "H": arg_map.get("H"),
                "theta": arg_map.get("theta"),
                "density": arg_map.get("density"),
                "atmPressure": arg_map.get("atmPressure", 101e3)
            }
        elif matType in ["PlaneStress", "PlaneStrain", "PlateFiber"]:
            specific_info = {
                "mat3DTag": arg_map.get("mat3DTag") if matType != "PlateFiber" else arg_map.get("threeDTag")
            }
        elif matType == "MultiaxialCyclicPlasticity":
            specific_info = {
                "rho": arg_map.get("rho"),
                "K": arg_map.get("K"),
                "G": arg_map.get("G"),
                "Su": arg_map.get("Su"),
                "Ho": arg_map.get("Ho"),
                "h": arg_map.get("h"),
                "m": arg_map.get("m"),
                "beta": arg_map.get("beta"),
                "KCoeff": arg_map.get("KCoeff")
            }
        elif matType == "BoundingCamClay":
            specific_info = {
                "massDensity": arg_map.get("massDensity"),
                "C": arg_map.get("C"),
                "bulkMod": arg_map.get("bulkMod"),
                "OCR": arg_map.get("OCR"),
                "mu_o": arg_map.get("mu_o"),
                "alpha": arg_map.get("alpha"),
                "lambda": arg_map.get("lambda"),
                "h": arg_map.get("h"),
                "m": arg_map.get("m")
            }
        elif matType == "FSAM":
            specific_info = {
                "rho": arg_map.get("rho"),
                "sXTag": arg_map.get("sXTag"),
                "sYTag": arg_map.get("sYTag"),
                "concTag": arg_map.get("concTag"),
                "rouX": arg_map.get("rouX"),
                "rouY": arg_map.get("rouY"),
                "nu": arg_map.get("nu"),
                "alfadow": arg_map.get("alfadow")
            }
        elif matType == "ManzariDafalias":
            specific_info = {
                "G0": arg_map.get("G0"),
                "nu": arg_map.get("nu"),
                "e_init": arg_map.get("e_init"),
                "Mc": arg_map.get("Mc"),
                "c": arg_map.get("c"),
                "lambda_c": arg_map.get("lambda_c"),
                "e0": arg_map.get("e0"),
                "ksi": arg_map.get("ksi"),
                "P_atm": arg_map.get("P_atm"),
                "m": arg_map.get("m"),
                "h0": arg_map.get("h0"),
                "ch": arg_map.get("ch"),
                "nb": arg_map.get("nb"),
                "A0": arg_map.get("A0"),
                "nd": arg_map.get("nd"),
                "z_max": arg_map.get("z_max"),
                "cz": arg_map.get("cz"),
                "Den": arg_map.get("Den")
            }
        elif matType == "PM4Sand":
            # PM4Sand有很多可选参数, 这里只列出必须参数
            specific_info = {
                "D_r": arg_map.get("D_r"),
                "G_o": arg_map.get("G_o"),
                "h_po": arg_map.get("h_po"),
                "Den": arg_map.get("Den")
            }
            # 添加可选参数
            optional_params = ["P_atm", "h_o", "e_max", "e_min", "n_b", "n_d", "A_do",
                              "z_max", "c_z", "c_e", "phi_cv", "nu", "g_degr", "c_dr",
                              "c_kaf", "Q_bolt", "R_bolt", "m_par", "F_sed", "p_sed"]
            for param in optional_params:
                if param in arg_map:
                    specific_info[param] = arg_map.get(param)
        elif matType == "PM4Silt":
            # PM4Silt有很多可选参数, 这里只列出必须参数
            specific_info = {
                "S_u": arg_map.get("S_u"),
                "Su_Rat": arg_map.get("Su_Rat"),
                "G_o": arg_map.get("G_o"),
                "h_po": arg_map.get("h_po"),
                "Den": arg_map.get("Den")
            }
            # 添加可选参数
            optional_params = ["Su_factor", "P_atm", "nu", "nG", "h0", "eInit", "lambda",
                              "phicv", "nb_wet", "nb_dry", "nd", "Ado", "ru_max", "z_max",
                              "cz", "ce", "cgd", "ckaf", "m_m", "CG_consol"]
            for param in optional_params:
                if param in arg_map:
                    specific_info[param] = arg_map.get(param)
        elif matType == "StressDensityModel":
            specific_info = {
                "mDen": arg_map.get("mDen"),
                "eNot": arg_map.get("eNot"),
                "A": arg_map.get("A"),
                "n": arg_map.get("n"),
                "nu": arg_map.get("nu"),
                "a1": arg_map.get("a1"),
                "b1": arg_map.get("b1"),
                "a2": arg_map.get("a2"),
                "b2": arg_map.get("b2"),
                "a3": arg_map.get("a3"),
                "b3": arg_map.get("b3"),
                "fd": arg_map.get("fd"),
                "muNot": arg_map.get("muNot"),
                "muCyc": arg_map.get("muCyc"),
                "sc": arg_map.get("sc"),
                "M": arg_map.get("M"),
                "patm": arg_map.get("patm")
            }
            # 处理ssls列表参数
            if "ssls" in arg_map:
                specific_info["ssls"] = arg_map.get("ssls")
            if "hsl" in arg_map:
                specific_info["hsl"] = arg_map.get("hsl")
            if "p1" in arg_map:
                specific_info["p1"] = arg_map.get("p1")
        elif matType == "AcousticMedium":
            specific_info = {
                "K": arg_map.get("K"),
                "rho": arg_map.get("rho")
            }
        else:
            # 对于未知的材料类型, 保存全部参数
            specific_info = {k: v for k, v in arg_map.items() if k not in ["matType", "matTag"]}
            specific_info["args"] = arg_map.get("args", [])

        # 合并基本信息和特定信息
        return {**base_info, **specific_info}
