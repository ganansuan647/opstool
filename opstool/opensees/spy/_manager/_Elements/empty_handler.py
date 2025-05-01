from typing import Any

import openseespy.opensees as ops

from .._BaseHandler import BaseHandler


class BeamColumnHandler(BaseHandler):
    def __init__(self, registry: dict[str, dict], element_store: dict[int, dict]):
        """
        registry: eleType → handler  的全局映射 (供 manager 生成)
        element_store: ElementManager.elements 共享引用
        """
        self.elements = element_store
        self._register(registry)

    @property
    def _COMMAND_RULES(self) -> dict[str, dict[str, Any]]:
        rules = {"alternative": True}

        # ndm for 2D/3D if needed
        ndm = ops.getNDM()[0]
        assert len(ops.getNDM()) == 1, f"Invalid length of ndm, expected 1, got {len(ops.getNDM()) =}"  # noqa: S101

        # 添加不同元素类型的规则
        if ndm == 2:
            rules["elasticBeamColumn"] = {
                "positional": ["eleType", "eleTag", "eleNodes*2", "secTag", "transfTag"],
                "options": {
                    "-mass?": "mass",
                    "-cMass?*0": "cMass",
                    "-release?": "releaseCode",
                }
            }
        elif ndm == 3:
            rules["elasticBeamColumn"] = {
                "positional": ["eleType", "eleTag", "eleNodes*2","secTag", "transfTag"],
                "options": {
                    "-mass?": "mass",
                    "-cMass?*0": "cMass",
                    "-releasez?": "releaseCodeZ",
                    "-releasey?": "releaseCodeY",
                }
            }
        else:
            raise NotImplementedError(f"Invalid {ndm =} for `elasticBeamColumn`")

        rules["ModElasticBeam2d"] = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "Area", "E_mod", "Iz", "K11", "K33", "K44", "transfTag"],
            "options": {
                "-mass?": "massDens",
                "-cMass?*0": "cMass",
            }
        }
        return {"element": rules}

    # ---------- eleType to handle ----------
    @staticmethod
    def handles() -> list[str]:
        return [
            "elasticBeamColumn", "ModElasticBeam2d"
        ]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        args, kwargs = arg_map["args"], arg_map["kwargs"]
        ele_type = args[0]
        dispatch = {
            "elasticBeamColumn": self._handle_elasticBeamColumn,
            "ModElasticBeam2d": self._handle_ModElasticBeam2d,
        }.get(ele_type, self._unknown)
        dispatch(*args, **kwargs)

    def _handle_elasticBeamColumn(self, *args, **kwargs) -> dict[str, Any]:
        """handle elasticBeamColumn element"""
        # First try to parse with default format: element('elasticBeamColumn', eleTag, *eleNodes, secTag, transfTag, ...)
        arg_map = self._parse("element", *args, **kwargs)
        command_type = 1
        # Check if there are unparsed positional args, if yes, it means we should use the second format
        if len(arg_map.get("args",[])) > 1:
            command_type = 2
            ndm = ops.getNDM()[0]
            if ndm == 2:
                rule = {
                    "positional": ["eleType", "eleTag", "eleNodes*2", "Area", "E_mod", "Iz", "transfTag"],
                    "options": {
                        "-mass?": "massDens",
                        "-cMass?*0": "cMass",
                        "-release?": "releaseCode",
                    }
                }
            elif ndm == 3:
                rule = {
                    "positional": ["eleType", "eleTag", "eleNodes*2", "Area", "E_mod", "G_mod", "Jxx", "Iy", "Iz", "transfTag"],
                    "options": {
                        "-mass?": "massDens",
                        "-cMass?*0": "cMass",
                        "-releasez?": "releaseCodeZ",
                        "-releasey?": "releaseCodeY",
                    }
                }
            # Parse with the rule directly
            arg_map = self._parse_rule_based_command(rule, *args, **kwargs)

        # Get parameters
        eleTag = arg_map.get("eleTag")
        eleinfo = {
                "eleType": arg_map.get("eleType"),
                "eleTag": eleTag,
                "eleNodes": arg_map.get("eleNodes", []),
                "transfTag": arg_map.get("transfTag"),
            }

        if command_type == 1:
            eleinfo["secTag"] = arg_map.get("secTag")
        else:
            if ndm==2:
                eleinfo["Area"] = arg_map.get("Area")
                eleinfo["E_mod"] = arg_map.get("E_mod")
                eleinfo["Iz"] = arg_map.get("Iz")
            elif ndm==3:
                eleinfo["Area"] = arg_map.get("Area")
                eleinfo["E_mod"] = arg_map.get("E_mod")
                eleinfo["G_mod"] = arg_map.get("G_mod")
                eleinfo["Jxx"] = arg_map.get("Jxx")
                eleinfo["Iy"] = arg_map.get("Iy")
                eleinfo["Iz"] = arg_map.get("Iz")

        if 'massDens' in arg_map:
            eleinfo['massDens'] = arg_map.get('massDens',0.0)

        if 'cMass' in arg_map:
            eleinfo['cMass'] = None

        if 'releaseCode' in arg_map:
            eleinfo['releaseCode'] = arg_map.get('releaseCode',0)

        if 'releaseCodeZ' in arg_map:
            eleinfo['releaseCodeZ'] = arg_map.get('releaseCodeZ',0)

        if 'releaseCodeY' in arg_map:
            eleinfo['releaseCodeY'] = arg_map.get('releaseCodeY',0)

        self.elements[eleTag] = eleinfo

    def _handle_ModElasticBeam2d(self, *args, **kwargs) -> dict[str, Any]:
        """Handle ModElasticBeam2d element"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "Area": arg_map.get("Area"),
            "E_mod": arg_map.get("E_mod"),
            "Iz": arg_map.get("Iz"),
            "K11": arg_map.get("K11"),
            "K33": arg_map.get("K33"),
            "K44": arg_map.get("K44"),
            "transfTag": arg_map.get("transfTag"),
        }

        # Handle optional parameters
        if 'massDens' in arg_map:
            eleinfo['massDens'] = arg_map.get('massDens',0.0)

        if 'cMass' in arg_map:
            eleinfo['cMass'] = None

        self.elements[eleTag] = eleinfo

    def _unknown(self, *args, **kwargs):
        # should never use this function but use ElementManager.handle_unknown_element()
        raise NotImplementedError

    def clear(self):
        self.elements.clear()
