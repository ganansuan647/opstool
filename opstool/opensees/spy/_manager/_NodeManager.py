from ._BaseHandler import BaseHandler
from typing import Any, Optional, override


class NodeManager(BaseHandler):
    def __init__(self):
        self.nodes = {}  # tag -> {coords: [], mass: [], ndf: int}
        self.dims = 0  # 模型维度
        self.dofs = 0  # 默认自由度数

    @property
    def _COMMAND_RULES(self) -> dict[str, dict[str, Any]]:
        return {
            # node(nodeTag, *crds, '-ndf', ndf, '-mass', *mass, '-disp', ...)
            "node": {
                "positional": ["tag", "coords*"],
                "options": {
                    "-ndf": "dofs",
                    "-mass": "mass*",
                    "-disp": "disp*",
                    "-vel": "vel*",
                    "-accel": "accel*",
                },
            },
            # mass(nodeTag, *massValues)
            "mass": {
                "positional": ["tag", "mass*"],
            },
            # model(typeName, *args)
            "model": {
                "positional": ["typeName"],
                "options": {
                    "-ndm": "dims",
                    "-ndf": "dofs",
                },
            },
        }

    def handles(self):
        return ["node", "mass", "model"]

    def handle(self, func_name: str, args: dict[str, Any]):
        if func_name == "node":
            self._handle_node(args)
        elif func_name == "mass":
            self._handle_mass(args)
        elif func_name == "model":
            self._handle_model(args)

    def _handle_node(self, args: dict[str, Any]):
        arg_map = self.parse_command("node", **args)

        # 使用parse_command处理的结果
        tag = arg_map.get("tag")
        if not tag:
            return

        coords = arg_map.get("coords", [])
        dims = arg_map.get("dims", self.dims)
        dofs = arg_map.get("dofs", self.dofs)  # 使用模型默认值
        mass = arg_map.get("mass", [])

        # 保存节点信息
        node_info = {"coords": coords, "ndm": dims, "dofs": dofs}

        # 如果有质量信息，也保存下来
        if mass:
            node_info["mass"] = mass
            # 更新全局质量记录
            if len(mass) > 0:
                total_mass = sum(mass)
                self._add_nodal_mass(tag, total_mass)

        self.nodes[tag] = node_info

    def _handle_mass(self, args: dict[str, Any]):
        arg_map = self.parse_command("mass", **args)
        tag = arg_map.get("tag")
        if not tag:
            return

        mass_values = arg_map.get("mass", [])
        if not mass_values:
            return

        # 更新节点质量信息
        node_info = self.nodes.get(tag, {})
        node_info["mass"] = mass_values
        self.nodes[tag] = node_info

        # 更新全局质量记录
        if mass_values:
            total_mass = sum(mass_values)
            self._add_nodal_mass(tag, total_mass)

    def _handle_model(self, args: dict[str, Any]):
        arg_map = self.parse_command("model", **args)
        # 处理模型维度和自由度设置
        args = arg_map.get("args", [])

        # 检查是否有维度参数
        if "dims" in arg_map:
            self.dims = arg_map["dims"]

        # 检查是否有自由度参数
        if "dofs" in arg_map:
            self.ndf = arg_map["dofs"]

    def get_node_coords(self, tag: int) -> list[float]:
        """获取节点坐标"""
        node = self.nodes.get(tag, {})
        return node.get("coords", [])

    def get_node_mass(self, tag: int) -> list[float]:
        """获取节点质量"""
        node = self.nodes.get(tag, {})
        return node.get("mass", [])

    def get_nodes_by_coords(
        self, x: Optional[float] = None, y: Optional[float] = None, z: Optional[float] = None
    ) -> list[int]:
        """根据坐标查找节点"""
        result = []
        for tag, node in self.nodes.items():
            coords = node.get("coords", [])
            if len(coords) < 1:
                continue

            match = True
            if x is not None and (len(coords) < 1 or abs(coords[0] - x) > 1e-6):
                match = False
            if y is not None and (len(coords) < 2 or abs(coords[1] - y) > 1e-6):
                match = False
            if z is not None and (len(coords) < 3 or abs(coords[2] - z) > 1e-6):
                match = False

            if match:
                result.append(tag)

        return result

    def clear(self):
        self.nodes.clear()
        self.dims = 0
        self.ndf = 0
