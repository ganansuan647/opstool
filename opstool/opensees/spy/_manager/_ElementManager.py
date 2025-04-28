from ._BaseHandler import BaseHandler
from typing import Any, Optional


class ElementManager(BaseHandler):
    def __init__(self):
        self.elements = {}
        self.element_nodes = {}  # 存储元素节点连接关系

    def handles(self):
        return ["element"]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        tag = int(arg_map.get("tag", 0))
        if tag == 0:
            return

        typeName = arg_map.get("typeName", "")
        args = arg_map.get("args", [])

        # 根据元素类型分发到对应的处理函数
        handler = getattr(self, f"_handle_{typeName}", self._handle_default)
        element_data = handler(tag, *args)

        if element_data:
            self.elements[tag] = element_data

            # 记录元素节点连接关系
            if "nodes" in element_data:
                self.element_nodes[tag] = element_data["nodes"]

    def _handle_default(self, tag: int, *args) -> dict[str, Any]:
        """默认处理函数，尝试提取节点信息"""
        if len(args) >= 2:
            try:
                # 假设前两个参数是节点标签
                nodes = [int(args[0]), int(args[1])]
                return {"type": "Unknown", "nodes": nodes}
            except (ValueError, IndexError):
                pass
        return {"type": "Unknown"}

    def _handle_Truss(self, tag: int, *args) -> dict[str, Any]:
        """处理桁架单元"""
        if len(args) < 4:
            return self._handle_default(tag, *args)

        try:
            return {"type": "Truss", "nodes": [int(args[0]), int(args[1])], "A": float(args[2]), "matTag": int(args[3])}
        except (ValueError, IndexError):
            return self._handle_default(tag, *args)

    def _handle_elasticBeamColumn(self, tag: int, *args) -> dict[str, Any]:
        """处理弹性梁柱单元"""
        if len(args) < 7:  # 最小需要 iNode, jNode, A, E, I, transfTag 这些参数
            return self._handle_default(tag, *args)

        try:
            return {
                "type": "elasticBeamColumn",
                "nodes": [int(args[0]), int(args[1])],
                "A": float(args[2]),
                "E": float(args[3]),
                "Iz": float(args[4]),  # 对于2D问题
                "transfTag": int(args[5]),
            }
        except (ValueError, IndexError):
            return self._handle_default(tag, *args)

    def _handle_dispBeamColumn(self, tag: int, *args) -> dict[str, Any]:
        """处理位移法非线性梁柱单元"""
        if len(args) < 5:  # 最小需要 iNode, jNode, numIntgrPts, secTag, transfTag
            return self._handle_default(tag, *args)

        try:
            return {
                "type": "dispBeamColumn",
                "nodes": [int(args[0]), int(args[1])],
                "numIntgrPts": int(args[2]),
                "secTag": int(args[3]),
                "transfTag": int(args[4]),
            }
        except (ValueError, IndexError):
            return self._handle_default(tag, *args)

    def _handle_zeroLength(self, tag: int, *args) -> dict[str, Any]:
        """处理零长度单元"""
        if len(args) < 4:  # 最少需要两个节点和材料标签
            return self._handle_default(tag, *args)

        try:
            # 零长度单元参数格式: iNode, jNode, -mat matTag1 matTag2..., -dir dir1 dir2...
            nodes = [int(args[0]), int(args[1])]

            # 提取材料标签和自由度方向
            mats = []
            dirs = []

            if "-mat" in args:
                mat_idx = args.index("-mat")
                # 从-mat后找到下一个关键字前的所有材料标签
                for i in range(mat_idx + 1, len(args)):
                    if args[i].startswith("-"):
                        break
                    mats.append(int(args[i]))

            if "-dir" in args:
                dir_idx = args.index("-dir")
                # 从-dir后找到下一个关键字前的所有方向
                for i in range(dir_idx + 1, len(args)):
                    if args[i].startswith("-"):
                        break
                    dirs.append(int(args[i]))

            return {"type": "zeroLength", "nodes": nodes, "materials": mats, "directions": dirs}
        except (ValueError, IndexError):
            return self._handle_default(tag, *args)

    def _handle_quad(self, tag: int, *args) -> dict[str, Any]:
        """处理四节点平面单元"""
        if len(args) < 7:  # iNode, jNode, kNode, lNode, thickness, matTag, type
            return self._handle_default(tag, *args)

        try:
            return {
                "type": "quad",
                "nodes": [int(args[0]), int(args[1]), int(args[2]), int(args[3])],
                "thickness": float(args[4]),
                "matTag": int(args[5]),
                "pressure": float(args[6]) if len(args) > 6 else 0.0,
                "rho": float(args[7]) if len(args) > 7 else 0.0,
                "b1": float(args[8]) if len(args) > 8 else 0.0,
                "b2": float(args[9]) if len(args) > 9 else 0.0,
            }
        except (ValueError, IndexError):
            return self._handle_default(tag, *args)

    def _handle_ShellMITC4(self, tag: int, *args) -> dict[str, Any]:
        """处理四节点壳单元"""
        if len(args) < 5:  # iNode, jNode, kNode, lNode, secTag
            return self._handle_default(tag, *args)

        try:
            return {
                "type": "ShellMITC4",
                "nodes": [int(args[0]), int(args[1]), int(args[2]), int(args[3])],
                "secTag": int(args[4]),
            }
        except (ValueError, IndexError):
            return self._handle_default(tag, *args)

    def _handle_forceBeamColumn(self, tag: int, *args) -> dict[str, Any]:
        """处理力法非线性梁柱单元"""
        if len(args) < 5:
            return self._handle_default(tag, *args)

        try:
            return {
                "type": "forceBeamColumn",
                "nodes": [int(args[0]), int(args[1])],
                "transfTag": int(args[2]),
                "integrationTag": int(args[3]) if "-integration" in args else None,
                "maxIter": int(args[4]) if len(args) > 4 else 10,
                "tol": float(args[5]) if len(args) > 5 else 1e-8,
            }
        except (ValueError, IndexError):
            return self._handle_default(tag, *args)

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
