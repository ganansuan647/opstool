from collections import defaultdict
from copy import deepcopy
from typing import Any, Literal, Optional

from ._BaseHandler import BaseHandler
from ._Elements import (
    ZeroLengthHandler,
    TrussHandler,
    BeamColumnHandler,
    JointHandler,
    LinkHandler,
    BearingHandler,
    QuadrilateralHandler,
    TriangularHandler,
    BrickHandler,
    TetrahedronHandler,
    UCSDUpHandler,
    OtherUpHandler,
    ContactHandler,
    # CableHandler,
    # PfemHandler,
    # MiscHandler
)


class ElementManager(BaseHandler):
    def __init__(self):
        # 统一数据仓库
        self.elements: dict[int, dict] = {}

        # 构建 handler 映射
        self._type2handler: dict[str, BaseHandler] = {}
        handler_classes = [
            ZeroLengthHandler,
            TrussHandler,
            BeamColumnHandler,
            JointHandler,
            LinkHandler,
            BearingHandler,
            QuadrilateralHandler,
            TriangularHandler,
            BrickHandler,
            TetrahedronHandler,
            UCSDUpHandler,
            OtherUpHandler,
            ContactHandler,
            # CableHandler,
            # PfemHandler,
            # MiscHandler
        ]
        for cls in handler_classes:
            cls(self._type2handler, self.elements)  # 注册 eleType → handler

    @property
    def _COMMAND_RULES(self) -> dict[str, dict[str, Any]]:
        """聚合各子 Handler 的 rule"""
        merged: defaultdict[str, dict[str, Any]] = defaultdict(lambda: defaultdict(lambda: deepcopy({"positional": ["eleType", "eleTag", "args*"]})))
        for h in set(self._type2handler.values()):
            for k, v in h._COMMAND_RULES.items():
                merged[k].update(v)
        return merged

    @staticmethod
    def handles():
        return ["element"]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        eleType = arg_map["args"][0]
        handler = self._type2handler.get(eleType)
        if handler:
            handler.handle(func_name, arg_map)
        else:
            self.handle_unknown_element(*arg_map["args"], **arg_map["kwargs"])

    def handle_unknown_element(self, *args, **kwargs):
        """Handle unknown elements"""
        arg_map = self._parse("element", *args, **kwargs)

        eleType = arg_map.get("eleType")
        eleTag = arg_map.get("eleTag")
        args = arg_map.get("args",[])
        eleinfo = {
            "eleType": eleType,
            "eleTag": eleTag,
            "args": args,
        }
        self.elements[eleTag] = eleinfo

    def get_element(self, eleTag: int) -> Optional[dict]:
        """Get element information by tag"""
        return self.elements.get(eleTag)

    def get_element_nodes(self, eleTag: int) -> list[int]:
        """Get nodes connected to the specified element"""
        return self.elements.get(eleTag).get("eleNodes",[])

    def get_elements_by_nodes(self, node_tags: list[int]) -> list[int]:
        """Get all elements connected to the specified nodes"""
        result = []
        for elem_tag, nodes in self.get_element_nodes.items():
            if all(node in nodes for node in node_tags):
                result.append(elem_tag)
        return result

    def get_elements_by_type(self, eleType: str) -> list[int]:
        """Get all elements of the specified type"""
        return [tag for tag, data in self.elements.items() if data.get("eleType", "").lower() == eleType.lower()]

    def get_elements(
            self,
            Type: Optional[Literal[
                "zerolength", "truss", "beamcolumn", "joint", "link",
                "bearing", "quadrilateral", "triangular", "brick",
                "tetrahedron", "ucsd_up", "other_up", "contact",
                "cable", "pfem", "misc"]] = None
        ):
        """Get elements by type"""
        if Type is None:
            return self.elements

        element_types = {
            "zerolength": ZeroLengthHandler.handles(),
            "truss": TrussHandler.handles(),
            "beamcolumn": BeamColumnHandler.handles(),
            "joint": JointHandler.handles(),
            "link": LinkHandler.handles(),
            "bearing": BearingHandler.handles(),
            "quadrilateral": QuadrilateralHandler.handles(),
            "triangular": TriangularHandler.handles(),
            "brick": BrickHandler.handles(),
            "tetrahedron": TetrahedronHandler.handles(),
            "ucsd_up": UCSDUpHandler.handles(),
            "other_up": OtherUpHandler.handles(),
            "contact": ContactHandler.handles(),
            # "cable": CableHandler.handles(),
            # "pfem": PfemHandler.handles(),
            # "misc": MiscHandler.handles()
        }

        element_list = []
        for eleType in element_types[Type]:
            element_list.extend([tag for tag, data in self.elements.items() if data.get("eleType", "") == eleType])

        return element_list

    def clear(self):
        self.elements.clear()
