from typing import Any

from .._BaseHandler import SubBaseHandler


class OtherUniaxialHandler(SubBaseHandler):
    def __init__(self, registry: dict[str, dict], materials_store: dict[int, dict]):
        """
        registry: matType → handler 的全局映射 (供 manager 生成)
        materials_store: MaterialManager.materials 共享引用
        """
        self.materials = materials_store
        self._register(registry)

    @property
    def _COMMAND_RULES(self) -> dict[str, dict[str, Any]]:
        return {
            "uniaxialMaterial": {
                "alternative": True,
                "Hardening": {
                    "positional": ["matType", "matTag", "E", "sigmaY", "H_iso", "H_kin"],
                    "optional": {"eta": 0.0}
                },
                "Cast": {
                    "positional": ["matType", "matTag", "n", "bo", "h", "fy", "E", "L", "b", "Ro", "cR1", "cR2"],
                    "optional": {"a1": "s2*Pp/Kp", "a2": 1.0, "a3": "a4*Pp/Kp", "a4": 1.0}
                },
                "ViscousDamper": {
                    "positional": ["matType", "matTag", "K_el", "Cd", "alpha"],
                    "optional": {"LGap": 0.0, "NM": 1, "RelTol": 1e-6, "AbsTol": 1e-10, "MaxHalf": 15}
                },
                "BilinearOilDamper": {
                    "positional": ["matType", "matTag", "K_el", "Cd"],
                    "optional": {"Fr": 1.0, "p": 1.0, "LGap": 0.0, "NM": 1, "RelTol": 1e-6, "AbsTol": 1e-10, "MaxHalf": 15}
                },
                "Bilin": {
                    "positional": ["matType", "matTag", "K0", "as_Plus", "as_Neg", "My_Plus", "My_Neg", "Lamda_S", "Lamda_C", "Lamda_A", "Lamda_K", "c_S", "c_C", "c_A", "c_K", "theta_p_Plus", "theta_p_Neg", "theta_pc_Plus", "theta_pc_Neg", "Res_Pos", "Res_Neg", "theta_u_Plus", "theta_u_Neg", "D_Plus", "D_Neg"],
                    "optional": {"nFactor": 0.0}
                },
                "ModIMKPeakOriented": {
                    "positional": ["matType", "matTag", "K0", "as_Plus", "as_Neg", "My_Plus", "My_Neg", "Lamda_S", "Lamda_C", "Lamda_A", "Lamda_K", "c_S", "c_C", "c_A", "c_K", "theta_p_Plus", "theta_p_Neg", "theta_pc_Plus", "theta_pc_Neg", "Res_Pos", "Res_Neg", "theta_u_Plus", "theta_u_Neg", "D_Plus", "D_Neg"]
                },
                "ModIMKPinching": {
                    "positional": ["matType", "matTag", "K0", "as_Plus", "as_Neg", "My_Plus", "My_Neg", "FprPos", "FprNeg", "A_pinch", "Lamda_S", "Lamda_C", "Lamda_A", "Lamda_K", "c_S", "c_C", "c_A", "c_K", "theta_p_Plus", "theta_p_Neg", "theta_pc_Plus", "theta_pc_Neg", "Res_Pos", "Res_Neg", "theta_u_Plus", "theta_u_Neg", "D_Plus", "D_Neg"]
                },
                "SAWS": {
                    "positional": ["matType", "matTag", "F0", "FI", "DU", "S0", "R1", "R2", "R3", "R4", "alpha", "beta"]
                },
                "BarSlip": {
                    "positional": ["matType", "matTag", "fc", "fy", "Es", "fu", "Eh", "db", "ld", "nb", "depth", "height"],
                    "optional": {"ancLratio": 1.0, "bsFlag": None, "type": None, "damage": "Damage", "unit": "psi"}
                },
                "Bond_SP01": {
                    "positional": ["matType", "matTag", "Fy", "Sy", "Fu", "Su", "b", "R"]
                },
                "Fatigue": {
                    "positional": ["matType", "matTag", "otherTag"],
                    "optional": {"-E0": None, "E0": 0.191, "-m": None, "m": -0.458, "-min": None, "min": -1e16, "-max": None, "max": 1e16}
                },
                "ImpactMaterial": {
                    "positional": ["matType", "matTag", "K1", "K2", "sigy", "gap"]
                },
                "HyperbolicGapMaterial": {
                    "positional": ["matType", "matTag", "Kmax", "Kur", "Rf", "Fult", "gap"]
                },
                "LimitState": {
                    "positional": ["matType", "matTag", "s1p", "e1p", "s2p", "e2p", "s3p", "e3p", "s1n", "e1n", "s2n", "e2n", "s3n", "e3n", "pinchX", "pinchY", "damage1", "damage2", "beta", "curveTag", "curveType"]
                },
                "MinMax": {
                    "positional": ["matType", "matTag", "otherTag"],
                    "optional": {"-min": None, "minStrain": 1e-16, "-max": None, "maxStrain": 1e16}
                },
                "ElasticBilin": {
                    "positional": ["matType", "matTag", "EP1", "EP2", "epsP2"],
                    "optional": {"EN1": "EP1", "EN2": "EP2", "epsN2": "-epsP2"}
                },
                "ElasticMultiLinear": {
                    "positional": ["matType", "matTag"],
                    "optional": {"eta": 0.0, "-strain": [], "-stress": []}
                },
                "MultiLinear": {
                    "positional": ["matType", "matTag", "*pts"]
                },
                "InitStrainMaterial": {
                    "positional": ["matType", "matTag", "otherTag", "initStrain"]
                },
                "InitStressMaterial": {
                    "positional": ["matType", "matTag", "otherTag", "initStress"]
                },
                "PathIndependent": {
                    "positional": ["matType", "matTag", "OtherTag"]
                },
                "Pinching4": {
                    "positional": ["matType", "matTag", "ePf1", "ePd1", "ePf2", "ePd2", "ePf3", "ePd3", "ePf4", "ePd4"],
                    "optional": {"eNf1": None, "eNd1": None, "eNf2": None, "eNd2": None, "eNf3": None, "eNd3": None, "eNf4": None, "eNd4": None, "rDispP": None, "rForceP": None, "uForceP": None, "rDispN": None, "rForceN": None, "uForceN": None, "gK1": None, "gK2": None, "gK3": None, "gK4": None, "gKLim": None, "gD1": None, "gD2": None, "gD3": None, "gD4": None, "gDLim": None, "gF1": None, "gF2": None, "gF3": None, "gF4": None, "gFLim": None, "gE": None, "dmgType": None}
                },
                "ECC01": {
                    "positional": ["matType", "matTag", "sigt0", "epst0", "sigt1", "epst1", "epst2", "sigc0", "epsc0", "epsc1", "alphaT1", "alphaT2", "alphaC", "alphaCU", "betaT", "betaC"]
                },
                "SelfCentering": {
                    "positional": ["matType", "matTag", "k1", "k2", "sig_act_p", "sig_act_n", "n1", "n2", "a_pos", "a_neg", "delta_a", "delta_b"],
                    "optional": {"epsSlip": 0, "epsBear": 0, "rBear": "k1"}
                },
                "Viscous": {
                    "positional": ["matType", "matTag", "C", "alpha"]
                },
                "BoucWen": {
                    "positional": ["matType", "matTag", "alpha", "ko", "n", "gamma", "beta", "Ao", "deltaA", "deltaNu", "deltaEta"]
                },
                "BWBN": {
                    "positional": ["matType", "matTag", "alpha", "ko", "n", "gamma", "beta", "Ao", "q", "zetas", "p", "Shi", "deltaShip", "lamb", "tol"]
                },
                "KikuchiAikenHDR": {
                    "positional": ["matType", "matTag", "tp", "ar", "hr", "temp", "rk", "rq", "rs", "rf"]
                },
                "KikuchiAikenLRB": {
                    "positional": ["matType", "matTag", "type", "ar", "hr", "gr", "ap", "tp", "alph", "beta", "temp", "rk", "rb", "ts"]
                },
                "AxialSp": {
                    "positional": ["matType", "matTag", "sce", "fty", "fcy", "bte", "bty", "bcy", "fcr", "ath", "thetap", "thetapc", "thetau", "thetad"]
                },
                "AxialSpHD": {
                    "positional": ["matType", "matTag", "sce", "fty", "fcy", "bte", "bty", "bcy", "fcr", "ath", "thetap", "thetapc", "thetau", "thetad", "thetaPf", "thetaPd", "k", "aa", "as", "es", "es0", "es0p", "es0n", "stype", "itype"]
                },
                "PinchingLimitStateMaterial": {
                    "positional": ["matType", "matTag", "stress1p", "strain1p", "stress2p", "strain2p", "stress3p", "strain3p", "stress4p", "strain4p"]
                },
                "CFSWSWP": {
                    "positional": ["matType", "matTag", "height", "width", "fuf", "fyf", "tf", "Af", "fus", "fys", "ts", "np", "ds", "vs", "sc", "nc", "type"]
                },
                "CFSSSWP": {
                    "positional": ["matType", "matTag", "height", "width", "fuf", "fyf", "tf", "Af", "fus", "fys", "ts", "np", "ds", "vs", "sc", "nc", "type"]
                },
                "Backbone": {
                    "positional": ["matType", "matTag", "matTag1"]
                },
                "Masonry": {
                    "positional": ["matType", "matTag", "E1", "E2", "d1", "d2", "s0", "alpha", "e0", "ex", "eta"]
                },
                "Pipe": {
                    "positional": ["matType", "matTag", "nt"]
                }
            }
        }

    # ---------- matType to handle ----------
    @staticmethod
    def handles() -> list[str]:
        return ["uniaxialMaterial"]

    @staticmethod
    def types() -> list[str]:
        return [
            "Hardening", "Cast", "ViscousDamper", "BilinearOilDamper", "Bilin",
            "ModIMKPeakOriented", "ModIMKPinching", "SAWS", "BarSlip", "Bond_SP01",
            "Fatigue", "ImpactMaterial", "HyperbolicGapMaterial", "LimitState",
            "MinMax", "ElasticBilin", "ElasticMultiLinear", "MultiLinear",
            "InitStrainMaterial", "InitStressMaterial", "PathIndependent", "Pinching4",
            "ECC01", "SelfCentering", "Viscous", "BoucWen", "BWBN",
            "KikuchiAikenHDR", "KikuchiAikenLRB", "AxialSp", "AxialSpHD",
            "PinchingLimitStateMaterial", "CFSWSWP", "CFSSSWP", "Backbone", "Masonry",
            "Pipe"
        ]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        args, kwargs = arg_map["args"], arg_map["kwargs"]
        matType = args[0]
        handler_method = getattr(self, f"_handle_{matType}", self._unknown)
        return handler_method(*args, **kwargs)

    # ---------- 具体材料类型处理方法 ----------
    def _handle_Hardening(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `Hardening` Material

        uniaxialMaterial('Hardening', matTag, E, sigmaY, H_iso, H_kin, eta=0.0)

        rule = {
            "positional": ["matType", "matTag", "E", "sigmaY", "H_iso", "H_kin"],
            "optional": {"eta": 0.0}
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "E": arg_map.get("E"),
            "sigmaY": arg_map.get("sigmaY"),
            "H_iso": arg_map.get("H_iso"),
            "H_kin": arg_map.get("H_kin"),
            "eta": arg_map.get("eta", 0.0),
            "materialCommandType": "uniaxialMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_Cast(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `Cast` Material

        uniaxialMaterial('Cast', matTag, n, bo, h, fy, E, L, b, Ro, cR1, cR2, a1=s2*Pp/Kp, a2=1.0, a3=a4*Pp/Kp, a4=1.0)

        rule = {
            "positional": ["matType", "matTag", "n", "bo", "h", "fy", "E", "L", "b", "Ro", "cR1", "cR2"],
            "optional": {"a1": "s2*Pp/Kp", "a2": 1.0, "a3": "a4*Pp/Kp", "a4": 1.0}
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "n": arg_map.get("n"),
            "bo": arg_map.get("bo"),
            "h": arg_map.get("h"),
            "fy": arg_map.get("fy"),
            "E": arg_map.get("E"),
            "L": arg_map.get("L"),
            "b": arg_map.get("b"),
            "Ro": arg_map.get("Ro"),
            "cR1": arg_map.get("cR1"),
            "cR2": arg_map.get("cR2"),
            "a1": arg_map.get("a1", "s2*Pp/Kp"),
            "a2": arg_map.get("a2", 1.0),
            "a3": arg_map.get("a3", "a4*Pp/Kp"),
            "a4": arg_map.get("a4", 1.0),
            "materialCommandType": "uniaxialMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_ViscousDamper(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `ViscousDamper` Material

        uniaxialMaterial('ViscousDamper', matTag, K_el, Cd, alpha, LGap=0.0, NM=1, RelTol=1e-6, AbsTol=1e-10, MaxHalf=15)

        rule = {
            "positional": ["matType", "matTag", "K_el", "Cd", "alpha"],
            "optional": {"LGap": 0.0, "NM": 1, "RelTol": 1e-6, "AbsTol": 1e-10, "MaxHalf": 15}
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "K_el": arg_map.get("K_el"),
            "Cd": arg_map.get("Cd"),
            "alpha": arg_map.get("alpha"),
            "LGap": arg_map.get("LGap", 0.0),
            "NM": arg_map.get("NM", 1),
            "RelTol": arg_map.get("RelTol", 1e-6),
            "AbsTol": arg_map.get("AbsTol", 1e-10),
            "MaxHalf": arg_map.get("MaxHalf", 15),
            "materialCommandType": "uniaxialMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _unknown(self, *args, **kwargs):
        # should never use this function but use MaterialManager.handle_unknown_material()
        raise NotImplementedError

    def _handle_BilinearOilDamper(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `BilinearOilDamper` Material

        uniaxialMaterial('BilinearOilDamper', matTag, K_el, Cd, Fr=1.0, p=1.0, LGap=0.0, NM=1, RelTol=1e-6, AbsTol=1e-10, MaxHalf=15)

        rule = {
            "positional": ["matType", "matTag", "K_el", "Cd"],
            "optional": {"Fr": 1.0, "p": 1.0, "LGap": 0.0, "NM": 1, "RelTol": 1e-6, "AbsTol": 1e-10, "MaxHalf": 15}
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "K_el": arg_map.get("K_el"),
            "Cd": arg_map.get("Cd"),
            "Fr": arg_map.get("Fr", 1.0),
            "p": arg_map.get("p", 1.0),
            "LGap": arg_map.get("LGap", 0.0),
            "NM": arg_map.get("NM", 1),
            "RelTol": arg_map.get("RelTol", 1e-6),
            "AbsTol": arg_map.get("AbsTol", 1e-10),
            "MaxHalf": arg_map.get("MaxHalf", 15),
            "materialCommandType": "uniaxialMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_Bilin(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `Bilin` Material

        uniaxialMaterial('Bilin', matTag, K0, as_Plus, as_Neg, My_Plus, My_Neg, Lamda_S, Lamda_C, Lamda_A, Lamda_K, c_S, c_C, c_A, c_K, theta_p_Plus, theta_p_Neg, theta_pc_Plus, theta_pc_Neg, Res_Pos, Res_Neg, theta_u_Plus, theta_u_Neg, D_Plus, D_Neg, nFactor=0.0)

        rule = {
            "positional": ["matType", "matTag", "K0", "as_Plus", "as_Neg", "My_Plus", "My_Neg", "Lamda_S", "Lamda_C", "Lamda_A", "Lamda_K", "c_S", "c_C", "c_A", "c_K", "theta_p_Plus", "theta_p_Neg", "theta_pc_Plus", "theta_pc_Neg", "Res_Pos", "Res_Neg", "theta_u_Plus", "theta_u_Neg", "D_Plus", "D_Neg"],
            "optional": {"nFactor": 0.0}
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "K0": arg_map.get("K0"),
            "as_Plus": arg_map.get("as_Plus"),
            "as_Neg": arg_map.get("as_Neg"),
            "My_Plus": arg_map.get("My_Plus"),
            "My_Neg": arg_map.get("My_Neg"),
            "Lamda_S": arg_map.get("Lamda_S"),
            "Lamda_C": arg_map.get("Lamda_C"),
            "Lamda_A": arg_map.get("Lamda_A"),
            "Lamda_K": arg_map.get("Lamda_K"),
            "c_S": arg_map.get("c_S"),
            "c_C": arg_map.get("c_C"),
            "c_A": arg_map.get("c_A"),
            "c_K": arg_map.get("c_K"),
            "theta_p_Plus": arg_map.get("theta_p_Plus"),
            "theta_p_Neg": arg_map.get("theta_p_Neg"),
            "theta_pc_Plus": arg_map.get("theta_pc_Plus"),
            "theta_pc_Neg": arg_map.get("theta_pc_Neg"),
            "Res_Pos": arg_map.get("Res_Pos"),
            "Res_Neg": arg_map.get("Res_Neg"),
            "theta_u_Plus": arg_map.get("theta_u_Plus"),
            "theta_u_Neg": arg_map.get("theta_u_Neg"),
            "D_Plus": arg_map.get("D_Plus"),
            "D_Neg": arg_map.get("D_Neg"),
            "nFactor": arg_map.get("nFactor", 0.0),
            "materialCommandType": "uniaxialMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_ModIMKPeakOriented(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `ModIMKPeakOriented` Material

        uniaxialMaterial('ModIMKPeakOriented', matTag, K0, as_Plus, as_Neg, My_Plus, My_Neg, Lamda_S, Lamda_C, Lamda_A, Lamda_K, c_S, c_C, c_A, c_K, theta_p_Plus, theta_p_Neg, theta_pc_Plus, theta_pc_Neg, Res_Pos, Res_Neg, theta_u_Plus, theta_u_Neg, D_Plus, D_Neg)

        rule = {
            "positional": ["matType", "matTag", "K0", "as_Plus", "as_Neg", "My_Plus", "My_Neg", "Lamda_S", "Lamda_C", "Lamda_A", "Lamda_K", "c_S", "c_C", "c_A", "c_K", "theta_p_Plus", "theta_p_Neg", "theta_pc_Plus", "theta_pc_Neg", "Res_Pos", "Res_Neg", "theta_u_Plus", "theta_u_Neg", "D_Plus", "D_Neg"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "K0": arg_map.get("K0"),
            "as_Plus": arg_map.get("as_Plus"),
            "as_Neg": arg_map.get("as_Neg"),
            "My_Plus": arg_map.get("My_Plus"),
            "My_Neg": arg_map.get("My_Neg"),
            "Lamda_S": arg_map.get("Lamda_S"),
            "Lamda_C": arg_map.get("Lamda_C"),
            "Lamda_A": arg_map.get("Lamda_A"),
            "Lamda_K": arg_map.get("Lamda_K"),
            "c_S": arg_map.get("c_S"),
            "c_C": arg_map.get("c_C"),
            "c_A": arg_map.get("c_A"),
            "c_K": arg_map.get("c_K"),
            "theta_p_Plus": arg_map.get("theta_p_Plus"),
            "theta_p_Neg": arg_map.get("theta_p_Neg"),
            "theta_pc_Plus": arg_map.get("theta_pc_Plus"),
            "theta_pc_Neg": arg_map.get("theta_pc_Neg"),
            "Res_Pos": arg_map.get("Res_Pos"),
            "Res_Neg": arg_map.get("Res_Neg"),
            "theta_u_Plus": arg_map.get("theta_u_Plus"),
            "theta_u_Neg": arg_map.get("theta_u_Neg"),
            "D_Plus": arg_map.get("D_Plus"),
            "D_Neg": arg_map.get("D_Neg"),
            "materialCommandType": "uniaxialMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_ModIMKPinching(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `ModIMKPinching` Material

        uniaxialMaterial('ModIMKPinching', matTag, K0, as_Plus, as_Neg, My_Plus, My_Neg, FprPos, FprNeg, A_pinch, Lamda_S, Lamda_C, Lamda_A, Lamda_K, c_S, c_C, c_A, c_K, theta_p_Plus, theta_p_Neg, theta_pc_Plus, theta_pc_Neg, Res_Pos, Res_Neg, theta_u_Plus, theta_u_Neg, D_Plus, D_Neg)
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "K0": arg_map.get("K0"),
            "as_Plus": arg_map.get("as_Plus"),
            "as_Neg": arg_map.get("as_Neg"),
            "My_Plus": arg_map.get("My_Plus"),
            "My_Neg": arg_map.get("My_Neg"),
            "FprPos": arg_map.get("FprPos"),
            "FprNeg": arg_map.get("FprNeg"),
            "A_pinch": arg_map.get("A_pinch"),
            "Lamda_S": arg_map.get("Lamda_S"),
            "Lamda_C": arg_map.get("Lamda_C"),
            "Lamda_A": arg_map.get("Lamda_A"),
            "Lamda_K": arg_map.get("Lamda_K"),
            "c_S": arg_map.get("c_S"),
            "c_C": arg_map.get("c_C"),
            "c_A": arg_map.get("c_A"),
            "c_K": arg_map.get("c_K"),
            "theta_p_Plus": arg_map.get("theta_p_Plus"),
            "theta_p_Neg": arg_map.get("theta_p_Neg"),
            "theta_pc_Plus": arg_map.get("theta_pc_Plus"),
            "theta_pc_Neg": arg_map.get("theta_pc_Neg"),
            "Res_Pos": arg_map.get("Res_Pos"),
            "Res_Neg": arg_map.get("Res_Neg"),
            "theta_u_Plus": arg_map.get("theta_u_Plus"),
            "theta_u_Neg": arg_map.get("theta_u_Neg"),
            "D_Plus": arg_map.get("D_Plus"),
            "D_Neg": arg_map.get("D_Neg"),
            "materialCommandType": "uniaxialMaterial"
        }
        self.materials[matTag] = material_info
        return material_info
    def _handle_SAWS(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `SAWS` Material

        uniaxialMaterial('SAWS', matTag, F0, FI, DU, S0, R1, R2, R3, R4, alpha, beta)
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "F0": arg_map.get("F0"),
            "FI": arg_map.get("FI"),
            "DU": arg_map.get("DU"),
            "S0": arg_map.get("S0"),
            "R1": arg_map.get("R1"),
            "R2": arg_map.get("R2"),
            "R3": arg_map.get("R3"),
            "R4": arg_map.get("R4"),
            "alpha": arg_map.get("alpha"),
            "beta": arg_map.get("beta"),
            "materialCommandType": "uniaxialMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_BarSlip(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `BarSlip` Material

        uniaxialMaterial('BarSlip', matTag, fc, fy, Es, fu, Eh, db, ld, nb, depth, height, ancLratio=1.0, bsFlag, type, damage='Damage', unit='psi')
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "fc": arg_map.get("fc"),
            "fy": arg_map.get("fy"),
            "Es": arg_map.get("Es"),
            "fu": arg_map.get("fu"),
            "Eh": arg_map.get("Eh"),
            "db": arg_map.get("db"),
            "ld": arg_map.get("ld"),
            "nb": arg_map.get("nb"),
            "depth": arg_map.get("depth"),
            "height": arg_map.get("height"),
            "ancLratio": arg_map.get("ancLratio", 1.0),
            "bsFlag": arg_map.get("bsFlag"),
            "type": arg_map.get("type"),
            "damage": arg_map.get("damage", "Damage"),
            "unit": arg_map.get("unit", "psi"),
            "materialCommandType": "uniaxialMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_Bond_SP01(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `Bond_SP01` Material

        uniaxialMaterial('Bond_SP01', matTag, Fy, Sy, Fu, Su, b, R)
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "Fy": arg_map.get("Fy"),
            "Sy": arg_map.get("Sy"),
            "Fu": arg_map.get("Fu"),
            "Su": arg_map.get("Su"),
            "b": arg_map.get("b"),
            "R": arg_map.get("R"),
            "materialCommandType": "uniaxialMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_Fatigue(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `Fatigue` Material

        uniaxialMaterial('Fatigue', matTag, otherTag, '-E0', E0=0.191, '-m', m=-0.458, '-min', min=-1e16, '-max', max=1e16)
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "otherTag": arg_map.get("otherTag"),
            "-E0": arg_map.get("-E0"),
            "E0": arg_map.get("E0", 0.191),
            "-m": arg_map.get("-m"),
            "m": arg_map.get("m", -0.458),
            "-min": arg_map.get("-min"),
            "min": arg_map.get("min", -1e16),
            "-max": arg_map.get("-max"),
            "max": arg_map.get("max", 1e16),
            "materialCommandType": "uniaxialMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_ImpactMaterial(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `ImpactMaterial` Material

        uniaxialMaterial('ImpactMaterial', matTag, K1, K2, sigy, gap)
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "K1": arg_map.get("K1"),
            "K2": arg_map.get("K2"),
            "sigy": arg_map.get("sigy"),
            "gap": arg_map.get("gap"),
            "materialCommandType": "uniaxialMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_HyperbolicGapMaterial(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `HyperbolicGapMaterial` Material

        uniaxialMaterial('HyperbolicGapMaterial', matTag, Kmax, Kur, Rf, Fult, gap)
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "Kmax": arg_map.get("Kmax"),
            "Kur": arg_map.get("Kur"),
            "Rf": arg_map.get("Rf"),
            "Fult": arg_map.get("Fult"),
            "gap": arg_map.get("gap"),
            "materialCommandType": "uniaxialMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_LimitState(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `LimitState` Material

        uniaxialMaterial('LimitState', matTag, s1p, e1p, s2p, e2p, s3p, e3p, s1n, e1n, s2n, e2n, s3n, e3n, pinchX, pinchY, damage1, damage2, beta, curveTag, curveType)
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "s1p": arg_map.get("s1p"),
            "e1p": arg_map.get("e1p"),
            "s2p": arg_map.get("s2p"),
            "e2p": arg_map.get("e2p"),
            "s3p": arg_map.get("s3p"),
            "e3p": arg_map.get("e3p"),
            "s1n": arg_map.get("s1n"),
            "e1n": arg_map.get("e1n"),
            "s2n": arg_map.get("s2n"),
            "e2n": arg_map.get("e2n"),
            "s3n": arg_map.get("s3n"),
            "e3n": arg_map.get("e3n"),
            "pinchX": arg_map.get("pinchX"),
            "pinchY": arg_map.get("pinchY"),
            "damage1": arg_map.get("damage1"),
            "damage2": arg_map.get("damage2"),
            "beta": arg_map.get("beta"),
            "curveTag": arg_map.get("curveTag"),
            "curveType": arg_map.get("curveType"),
            "materialCommandType": "uniaxialMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_MinMax(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `MinMax` Material

        uniaxialMaterial('MinMax', matTag, otherTag, '-min', minStrain=1e-16, '-max', maxStrain=1e16)
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "otherTag": arg_map.get("otherTag"),
            "-min": arg_map.get("-min"),
            "minStrain": arg_map.get("minStrain", 1e-16),
            "-max": arg_map.get("-max"),
            "maxStrain": arg_map.get("maxStrain", 1e16),
            "materialCommandType": "uniaxialMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_ElasticBilin(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `ElasticBilin` Material

        uniaxialMaterial('ElasticBilin', matTag, EP1, EP2, epsP2, EN1=EP1, EN2=EP2, epsN2=-epsP2)
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        EP1 = arg_map.get("EP1")
        EP2 = arg_map.get("EP2")
        epsP2 = arg_map.get("epsP2")

        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "EP1": EP1,
            "EP2": EP2,
            "epsP2": epsP2,
            "EN1": arg_map.get("EN1", EP1),
            "EN2": arg_map.get("EN2", EP2),
            "epsN2": arg_map.get("epsN2", f"-{epsP2}"),
            "materialCommandType": "uniaxialMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_ElasticMultiLinear(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `ElasticMultiLinear` Material

        uniaxialMaterial('ElasticMultiLinear', matTag, eta=0.0, '-strain', *strain, '-stress', *stress)
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "eta": arg_map.get("eta", 0.0),
            "-strain": arg_map.get("-strain", []),
            "-stress": arg_map.get("-stress", []),
            "materialCommandType": "uniaxialMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_MultiLinear(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `MultiLinear` Material

        uniaxialMaterial('MultiLinear', matTag, *pts)
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "pts": arg_map.get("*pts", []),
            "materialCommandType": "uniaxialMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_InitStrainMaterial(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `InitStrainMaterial` Material

        uniaxialMaterial('InitStrainMaterial', matTag, otherTag, initStrain)
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "otherTag": arg_map.get("otherTag"),
            "initStrain": arg_map.get("initStrain"),
            "materialCommandType": "uniaxialMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_InitStressMaterial(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `InitStressMaterial` Material

        uniaxialMaterial('InitStressMaterial', matTag, otherTag, initStress)
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "otherTag": arg_map.get("otherTag"),
            "initStress": arg_map.get("initStress"),
            "materialCommandType": "uniaxialMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_PathIndependent(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `PathIndependent` Material

        uniaxialMaterial('PathIndependent', matTag, OtherTag)
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "OtherTag": arg_map.get("OtherTag"),
            "materialCommandType": "uniaxialMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_Pinching4(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `Pinching4` Material

        uniaxialMaterial('Pinching4', matTag, ePf1, ePd1, ePf2, ePd2, ePf3, ePd3, ePf4, ePd4, <eNf1, eNd1, eNf2, eNd2, eNf3, eNd3, eNf4, eNd4>,
                         rDispP, rForceP, uForceP, <rDispN, rForceN, uForceN>, gK1, gK2, gK3, gK4, gKLim, gD1, gD2, gD3, gD4, gDLim, gF1, gF2, gF3, gF4, gFLim, gE, dmgType)
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "ePf1": arg_map.get("ePf1"),
            "ePd1": arg_map.get("ePd1"),
            "ePf2": arg_map.get("ePf2"),
            "ePd2": arg_map.get("ePd2"),
            "ePf3": arg_map.get("ePf3"),
            "ePd3": arg_map.get("ePd3"),
            "ePf4": arg_map.get("ePf4"),
            "ePd4": arg_map.get("ePd4"),
            "eNf1": arg_map.get("eNf1"),
            "eNd1": arg_map.get("eNd1"),
            "eNf2": arg_map.get("eNf2"),
            "eNd2": arg_map.get("eNd2"),
            "eNf3": arg_map.get("eNf3"),
            "eNd3": arg_map.get("eNd3"),
            "eNf4": arg_map.get("eNf4"),
            "eNd4": arg_map.get("eNd4"),
            "rDispP": arg_map.get("rDispP"),
            "rForceP": arg_map.get("rForceP"),
            "uForceP": arg_map.get("uForceP"),
            "rDispN": arg_map.get("rDispN"),
            "rForceN": arg_map.get("rForceN"),
            "uForceN": arg_map.get("uForceN"),
            "gK1": arg_map.get("gK1"),
            "gK2": arg_map.get("gK2"),
            "gK3": arg_map.get("gK3"),
            "gK4": arg_map.get("gK4"),
            "gKLim": arg_map.get("gKLim"),
            "gD1": arg_map.get("gD1"),
            "gD2": arg_map.get("gD2"),
            "gD3": arg_map.get("gD3"),
            "gD4": arg_map.get("gD4"),
            "gDLim": arg_map.get("gDLim"),
            "gF1": arg_map.get("gF1"),
            "gF2": arg_map.get("gF2"),
            "gF3": arg_map.get("gF3"),
            "gF4": arg_map.get("gF4"),
            "gFLim": arg_map.get("gFLim"),
            "gE": arg_map.get("gE"),
            "dmgType": arg_map.get("dmgType"),
            "materialCommandType": "uniaxialMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_ECC01(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `ECC01` Material

        uniaxialMaterial('ECC01', matTag, sigt0, epst0, sigt1, epst1, epst2, sigc0, epsc0, epsc1, alphaT1, alphaT2, alphaC, alphaCU, betaT, betaC)
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "sigt0": arg_map.get("sigt0"),
            "epst0": arg_map.get("epst0"),
            "sigt1": arg_map.get("sigt1"),
            "epst1": arg_map.get("epst1"),
            "epst2": arg_map.get("epst2"),
            "sigc0": arg_map.get("sigc0"),
            "epsc0": arg_map.get("epsc0"),
            "epsc1": arg_map.get("epsc1"),
            "alphaT1": arg_map.get("alphaT1"),
            "alphaT2": arg_map.get("alphaT2"),
            "alphaC": arg_map.get("alphaC"),
            "alphaCU": arg_map.get("alphaCU"),
            "betaT": arg_map.get("betaT"),
            "betaC": arg_map.get("betaC"),
            "materialCommandType": "uniaxialMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_SelfCentering(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `SelfCentering` Material

        uniaxialMaterial('SelfCentering', matTag, k1, k2, sigAct, beta, epsSlip=0, epsBear=0, rBear=k1)
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        k1 = arg_map.get("k1")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "k1": k1,
            "k2": arg_map.get("k2"),
            "sigAct": arg_map.get("sigAct"),
            "beta": arg_map.get("beta"),
            "epsSlip": arg_map.get("epsSlip", 0),
            "epsBear": arg_map.get("epsBear", 0),
            "rBear": arg_map.get("rBear", k1),
            "materialCommandType": "uniaxialMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_Viscous(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `Viscous` Material

        uniaxialMaterial('Viscous', matTag, C, alpha)
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "C": arg_map.get("C"),
            "alpha": arg_map.get("alpha"),
            "materialCommandType": "uniaxialMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_BoucWen(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `BoucWen` Material

        uniaxialMaterial('BoucWen', matTag, alpha, ko, n, gamma, beta, Ao, deltaA, deltaNu, deltaEta)
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "alpha": arg_map.get("alpha"),
            "ko": arg_map.get("ko"),
            "n": arg_map.get("n"),
            "gamma": arg_map.get("gamma"),
            "beta": arg_map.get("beta"),
            "Ao": arg_map.get("Ao"),
            "deltaA": arg_map.get("deltaA"),
            "deltaNu": arg_map.get("deltaNu"),
            "deltaEta": arg_map.get("deltaEta"),
            "materialCommandType": "uniaxialMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_BWBN(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `BWBN` Material

        uniaxialMaterial('BWBN', matTag, alpha, ko, n, gamma, beta, Ao, q, zetas, p, Shi, deltaShi, lambda, tol, maxIter)
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "alpha": arg_map.get("alpha"),
            "ko": arg_map.get("ko"),
            "n": arg_map.get("n"),
            "gamma": arg_map.get("gamma"),
            "beta": arg_map.get("beta"),
            "Ao": arg_map.get("Ao"),
            "q": arg_map.get("q"),
            "zetas": arg_map.get("zetas"),
            "p": arg_map.get("p"),
            "Shi": arg_map.get("Shi"),
            "deltaShi": arg_map.get("deltaShi"),
            "lambda": arg_map.get("lambda"),
            "tol": arg_map.get("tol"),
            "maxIter": arg_map.get("maxIter"),
            "materialCommandType": "uniaxialMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_KikuchiAikenHDR(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `KikuchiAikenHDR` Material

        uniaxialMaterial('KikuchiAikenHDR', matTag, tp, ar, hr, <'-coGHU', cg, ch, cu>, <'-coMSS', rs, rf>)
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "tp": arg_map.get("tp"),
            "ar": arg_map.get("ar"),
            "hr": arg_map.get("hr"),
            "-coGHU": arg_map.get("-coGHU"),
            "cg": arg_map.get("cg"),
            "ch": arg_map.get("ch"),
            "cu": arg_map.get("cu"),
            "-coMSS": arg_map.get("-coMSS"),
            "rs": arg_map.get("rs"),
            "rf": arg_map.get("rf"),
            "materialCommandType": "uniaxialMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_KikuchiAikenLRB(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `KikuchiAikenLRB` Material

        uniaxialMaterial('KikuchiAikenLRB', matTag, type, ar, hr, gr, ap, tp, alph, beta, <'-T', temp>, <'-coKQ', rk, rq>, <'-coMSS', rs, rf>)
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "type": arg_map.get("type"),
            "ar": arg_map.get("ar"),
            "hr": arg_map.get("hr"),
            "gr": arg_map.get("gr"),
            "ap": arg_map.get("ap"),
            "tp": arg_map.get("tp"),
            "alph": arg_map.get("alph"),
            "beta": arg_map.get("beta"),
            "-T": arg_map.get("-T"),
            "temp": arg_map.get("temp"),
            "-coKQ": arg_map.get("-coKQ"),
            "rk": arg_map.get("rk"),
            "rq": arg_map.get("rq"),
            "-coMSS": arg_map.get("-coMSS"),
            "rs": arg_map.get("rs"),
            "rf": arg_map.get("rf"),
            "materialCommandType": "uniaxialMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_AxialSp(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `AxialSp` Material

        uniaxialMaterial('AxialSp', matTag, sce, fty, fcy, <bte, bty, bcy, fcr>)
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "sce": arg_map.get("sce"),
            "fty": arg_map.get("fty"),
            "fcy": arg_map.get("fcy"),
            "bte": arg_map.get("bte"),
            "bty": arg_map.get("bty"),
            "bcy": arg_map.get("bcy"),
            "fcr": arg_map.get("fcr"),
            "materialCommandType": "uniaxialMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_AxialSpHD(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `AxialSpHD` Material

        uniaxialMaterial('AxialSpHD', matTag, sce, fty, fcy, <bte, bty, bth, bcy, fcr, ath>)
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "sce": arg_map.get("sce"),
            "fty": arg_map.get("fty"),
            "fcy": arg_map.get("fcy"),
            "bte": arg_map.get("bte"),
            "bty": arg_map.get("bty"),
            "bth": arg_map.get("bth"),
            "bcy": arg_map.get("bcy"),
            "fcr": arg_map.get("fcr"),
            "ath": arg_map.get("ath"),
            "materialCommandType": "uniaxialMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_PinchingLimitStateMaterial(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `PinchingLimitStateMaterial` Material

        uniaxialMaterial('PinchingLimitStateMaterial', matTag, nodeT, nodeB, driftAxis, Kelas, crvTyp, crvTag, YpinchUPN, YpinchRPN, XpinchRPN, YpinchUNP, YpinchRNP, XpinchRNP, dmgStrsLimE, dmgDispMax, dmgE1, dmgE2, dmgE3, dmgE4, dmgELim, dmgR1, dmgR2, dmgR3, dmgR4, dmgRLim, dmgRCyc, dmgS1, dmgS2, dmgS3, dmgS4, dmgSLim, dmgSCyc)
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "nodeT": arg_map.get("nodeT"),
            "nodeB": arg_map.get("nodeB"),
            "driftAxis": arg_map.get("driftAxis"),
            "Kelas": arg_map.get("Kelas"),
            "crvTyp": arg_map.get("crvTyp"),
            "crvTag": arg_map.get("crvTag"),
            "YpinchUPN": arg_map.get("YpinchUPN"),
            "YpinchRPN": arg_map.get("YpinchRPN"),
            "XpinchRPN": arg_map.get("XpinchRPN"),
            "YpinchUNP": arg_map.get("YpinchUNP"),
            "YpinchRNP": arg_map.get("YpinchRNP"),
            "XpinchRNP": arg_map.get("XpinchRNP"),
            "dmgStrsLimE": arg_map.get("dmgStrsLimE"),
            "dmgDispMax": arg_map.get("dmgDispMax"),
            "dmgE1": arg_map.get("dmgE1"),
            "dmgE2": arg_map.get("dmgE2"),
            "dmgE3": arg_map.get("dmgE3"),
            "dmgE4": arg_map.get("dmgE4"),
            "dmgELim": arg_map.get("dmgELim"),
            "dmgR1": arg_map.get("dmgR1"),
            "dmgR2": arg_map.get("dmgR2"),
            "dmgR3": arg_map.get("dmgR3"),
            "dmgR4": arg_map.get("dmgR4"),
            "dmgRLim": arg_map.get("dmgRLim"),
            "dmgRCyc": arg_map.get("dmgRCyc"),
            "dmgS1": arg_map.get("dmgS1"),
            "dmgS2": arg_map.get("dmgS2"),
            "dmgS3": arg_map.get("dmgS3"),
            "dmgS4": arg_map.get("dmgS4"),
            "dmgSLim": arg_map.get("dmgSLim"),
            "dmgSCyc": arg_map.get("dmgSCyc"),
            "materialCommandType": "uniaxialMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_CFSWSWP(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `CFSWSWP` Material (Wood-Sheathed Cold-Formed Steel Shear Wall Panel)

        uniaxialMaterial('CFSWSWP', matTag, height, width, fut, tf, Ife, Ifi, ts, np, ds, Vs, sc, nc, type, openingArea, openingLength)
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "height": arg_map.get("height"),
            "width": arg_map.get("width"),
            "fut": arg_map.get("fut"),
            "tf": arg_map.get("tf"),
            "Ife": arg_map.get("Ife"),
            "Ifi": arg_map.get("Ifi"),
            "ts": arg_map.get("ts"),
            "np": arg_map.get("np"),
            "ds": arg_map.get("ds"),
            "Vs": arg_map.get("Vs"),
            "sc": arg_map.get("sc"),
            "nc": arg_map.get("nc"),
            "type": arg_map.get("type"),
            "openingArea": arg_map.get("openingArea"),
            "openingLength": arg_map.get("openingLength"),
            "materialCommandType": "uniaxialMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_CFSSSWP(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `CFSSSWP` Material (Steel-Sheathed Cold-formed Steel Shear Wall Panel)

        uniaxialMaterial('CFSSSWP', matTag, height, width, fuf, fyf, tf, Af, fus, fys, ts, np, ds, Vs, sc, dt, openingArea, openingLength)
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "height": arg_map.get("height"),
            "width": arg_map.get("width"),
            "fuf": arg_map.get("fuf"),
            "fyf": arg_map.get("fyf"),
            "tf": arg_map.get("tf"),
            "Af": arg_map.get("Af"),
            "fus": arg_map.get("fus"),
            "fys": arg_map.get("fys"),
            "ts": arg_map.get("ts"),
            "np": arg_map.get("np"),
            "ds": arg_map.get("ds"),
            "Vs": arg_map.get("Vs"),
            "sc": arg_map.get("sc"),
            "dt": arg_map.get("dt"),
            "openingArea": arg_map.get("openingArea"),
            "openingLength": arg_map.get("openingLength"),
            "materialCommandType": "uniaxialMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_Backbone(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `Backbone` Material

        uniaxialMaterial('Backbone', matTag, backboneTag)
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "backboneTag": arg_map.get("backboneTag"),
            "materialCommandType": "uniaxialMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_Masonry(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `Masonry` Material

        uniaxialMaterial('Masonry', matTag, Fm, Ft, Um, Uult, Ucl, Emo, L, a1, a2, D1, D2, Ach, Are, Ba, Bch, Gun, Gplu, Gplr, Exp1, Exp2, IENV)
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "Fm": arg_map.get("Fm"),
            "Ft": arg_map.get("Ft"),
            "Um": arg_map.get("Um"),
            "Uult": arg_map.get("Uult"),
            "Ucl": arg_map.get("Ucl"),
            "Emo": arg_map.get("Emo"),
            "L": arg_map.get("L"),
            "a1": arg_map.get("a1"),
            "a2": arg_map.get("a2"),
            "D1": arg_map.get("D1"),
            "D2": arg_map.get("D2"),
            "Ach": arg_map.get("Ach"),
            "Are": arg_map.get("Are"),
            "Ba": arg_map.get("Ba"),
            "Bch": arg_map.get("Bch"),
            "Gun": arg_map.get("Gun"),
            "Gplu": arg_map.get("Gplu"),
            "Gplr": arg_map.get("Gplr"),
            "Exp1": arg_map.get("Exp1"),
            "Exp2": arg_map.get("Exp2"),
            "IENV": arg_map.get("IENV"),
            "materialCommandType": "uniaxialMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_Pipe(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `Pipe` Material

        uniaxialMaterial('Pipe', matTag, nt, T1, E1, xnu1, alpT1, <T2, E2, xnu2, alpT2, ... >)
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        nt = arg_map.get("nt")

        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "nt": nt,
            "materialCommandType": "uniaxialMaterial"
        }

        # 获取所有温度点的参数
        for i in range(1, nt + 1):
            material_info[f"T{i}"] = arg_map.get(f"T{i}")
            material_info[f"E{i}"] = arg_map.get(f"E{i}")
            material_info[f"xnu{i}"] = arg_map.get(f"xnu{i}")
            material_info[f"alpT{i}"] = arg_map.get(f"alpT{i}")

        self.materials[matTag] = material_info
        return material_info

    def clear(self):
        self.materials.clear()
