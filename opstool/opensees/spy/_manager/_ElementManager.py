from collections import defaultdict
from typing import Any, Optional

import openseespy.opensees as ops

from ._BaseHandler import BaseHandler


class ElementManager(BaseHandler):
    def __init__(self):
        self.elements = {}
        self.zerolength = {}
        self.zerolengthND = {}
        self.truss = {}
        self.beamcolumn = {}
        self.joint = {}
        self.link = {}
        self.bearing = {}
        self.quadrilateral = {}
        self.triangular = {}
        self.brick = {}
        self.tetrahedron = {}
        self.ucsd_up = {}
        self.other_up = {}
        self.contact = {}
        self.cable = {}
        self.pfem = {}
        self.misc = {}

    @property
    def _COMMAND_RULES(self) -> dict[str, dict[str, Any]]:
        # element(eleType, tag, *eleNodes, *eleArgs), use defaultdict to set default rule(simplified)
        alternative_rules = defaultdict(lambda: {"positional": ["eleType", "tag", "args*"]}.copy())
        alternative_rules["alternative"] = True

        # ndm for vector if needed
        ndm = ops.getNDM()[0]
        assert len(ops.getNDM()) == 1, f"Invalid length of ndm, expected 1, got {len(ops.getNDM()) =}"  # noqa: S101

        # add rule for different element types
        alternative_rules["zeroLength"] = {
            "positional": ["eleType", "tag", "eleNodes*2"],
            "options": {
                "-mat": "mat*",
                "-dir": "dir*",
                "-doRayleigh": "rFlag",
                "-orient": [f"vecx?*{ndm}",f"vecyp?*{ndm}"],      # vecx and vecyp
            }
        }
        alternative_rules["zeroLengthND"] = {
            "positional": ["eleType", "tag", "eleNodes*2", "matTag", "uniTag?"],
            "options": {
                "-orient": [f"vecx*{ndm}",f"vecyp*{ndm}"],      # vecx and vecyp
            }
        }

        return {
            # element(eleType, tag, *eleNodes, *eleArgs)
            "element": alternative_rules
        }


    def handles(self):
        return ["element"]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        args,kwargs = arg_map.get("args"),arg_map.get("kwargs")
        eleType = args[0]
        assert isinstance(eleType,str)  # eleType should be string

        if eleType == "zeroLength":
            self._handle_zeroLength(*args,**kwargs)
        elif eleType == "zeroLengthND":
            self._handle_zerolengthND(*args,**kwargs)
        elif eleType == "mass":
            self._handle_mass(*args,**kwargs)
        elif eleType == "model":
            self._handle_model(*args,**kwargs)
        else:
            self.handle_unknown_element(*args,**kwargs)

    def handle_unknown_element(self, *args, **kwargs):
        """处理未知元素"""
        pass

    def _handle_zeroLength(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `zeroLength` element

        rule = {
            "positional": ["eleType", "tag", "eleNodes*2"],
            "options": {
                "-mat": "mat*",
                "-dir": "dir*",
                "doRayleigh": "rFlag",
                "-orient": [f"vecx*{ndm}",f"vecyp*{ndm}"],      # vecx and vecyp
            }
        }
        """
        arg_map = self._parse("element", *args, **kwargs)

        # positional arguments
        eleType = arg_map.get("eleType")
        tag = arg_map.get("tag")
        if not tag:
            return
        eleNodes = arg_map.get("eleNodes")

        # optional arguments
        mat = arg_map.get("mat", [])
        direction = arg_map.get("dir", [])
        rFlag = arg_map.get("rFlag", 0)
        vecx = arg_map.get("vecx", [])
        vecyp = arg_map.get("vecyp", [])

        # 保存零长度单元信息
        eleinfo = {
            "type": eleType,
            "tag": tag,
            "nodes": eleNodes,
            "mat": mat,
            "dir": direction,
            "rFlag": rFlag,
            "vecx": vecx,
            "vecyp": vecyp,
        }
        self.zerolength[tag] = eleinfo
        self.elements[tag] = eleinfo

    def _handle_zerolengthND(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `zeroLengthND` element

        element('zeroLengthND', eleTag, *eleNodes, matTag, <uniTag>, <'-orient', *vecx, vecyp>)

        rule = {
            "positional": ["eleType", "tag", "eleNodes*2", "matTag", "uniTag?"],
            "options": {
                "-orient": [f"vecx*{ndm}",f"vecyp*{ndm}"],      # vecx and vecyp
            }
        }
        """
        arg_map = self._parse("element", *args, **kwargs)

        # positional arguments
        eleType = arg_map.get("eleType")
        tag = arg_map.get("tag")
        if not tag:
            return
        eleNodes = arg_map.get("eleNodes")
        matTag = arg_map.get("matTag")
        uniTag = arg_map.get("uniTag", None)

        # optional arguments
        vecx = arg_map.get("vecx", [])
        vecyp = arg_map.get("vecyp", [])

        # 保存zeroLengthND单元信息
        eleinfo = {
            "type": eleType,
            "tag": tag,
            "nodes": eleNodes,
            "matTag": matTag,
            "uniTag": uniTag,
            "vecx": vecx,
            "vecyp": vecyp,
        }
        self.zerolengthND[tag] = eleinfo
        self.elements[tag] = eleinfo

    def get_element(self, tag: int) -> Optional[dict]:
        """获取指定标签的元素信息"""
        return self.elements.get(tag)

    def get_element_nodes(self, tag: int) -> list[int]:
        """获取指定元素连接的节点"""
        return self.element_nodes.get(tag, [])

    def get_elements_by_nodes(self, node_tags: list[int]) -> list[int]:
        """获取连接指定节点的所有元素"""
        result = []
        for elem_tag, nodes in self.element_nodes.items():
            if all(node in nodes for node in node_tags):
                result.append(elem_tag)
        return result

    def get_elements_by_type(self, element_type: str) -> list[int]:
        """获取指定类型的所有元素"""
        return [tag for tag, data in self.elements.items() if data.get("type", "").lower() == element_type.lower()]

    def clear(self):
        self.elements.clear()
        self.element_nodes.clear()
