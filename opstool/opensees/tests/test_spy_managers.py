"""
测试OpenSeesSpy管理器模块的集成测试
"""

import sys
import os
from pathlib import Path
import unittest

# 添加目录到sys.path以便导入spy模块
spy_path = str(Path(__file__).resolve().parents[1])
sys.path.insert(0, spy_path)

# 从模块导入需要测试的类
from opstool.opensees.spy._manager._BaseHandler import BaseHandler
from opstool.opensees.spy._manager._NodeManager import NodeManager
from opstool.opensees.spy._manager._ElementManager import ElementManager
from opstool.opensees.spy._manager._LoadManager import LoadManager


class TestSpyManagers(unittest.TestCase):
    """测试所有spy管理器的集成测试类"""

    def setUp(self):
        """初始化测试环境"""
        self.node_manager = NodeManager()
        self.element_manager = ElementManager()
        self.load_manager = LoadManager()

    def test_node_manager(self):
        """测试NodeManager的基本功能"""
        # 测试model命令处理
        model_data = {"args": ["basic", "-ndm", 2, "-ndf", 3]}
        self.node_manager.handle("model", model_data)

        self.assertEqual(self.node_manager.dims, 2)
        self.assertEqual(self.node_manager.ndf, 3)

        # 测试node命令处理
        node_data = {"tag": 1, "coords": [10.0, 20.0]}
        self.node_manager.handle("node", node_data)

        node_data2 = {"tag": 2, "coords": [30.0, 40.0], "mass": [1.0, 2.0, 3.0]}
        self.node_manager.handle("node", node_data2)

        # 验证节点是否被正确存储
        self.assertIn(1, self.node_manager.nodes)
        self.assertIn(2, self.node_manager.nodes)

        # 验证节点坐标是否正确
        self.assertEqual(self.node_manager.nodes[1]["coords"], [10.0, 20.0])
        self.assertEqual(self.node_manager.nodes[2]["coords"], [30.0, 40.0])

        # 验证质量是否正确存储
        self.assertEqual(self.node_manager.nodes[2].get("mass"), [1.0, 2.0, 3.0])

        # 测试按坐标查找节点
        nodes = self.node_manager.get_nodes_by_coords(x=10.0)
        self.assertEqual(set(nodes), {1})

    def test_element_manager(self):
        """测试ElementManager的基本功能"""
        # 测试创建桁架单元
        truss_data = {"typeName": "Truss", "tag": 1, "args": [1, 2, 100.0, 3]}
        self.element_manager.handle("element", truss_data)

        # 测试创建弹性梁柱单元
        beam_data = {"typeName": "elasticBeamColumn", "tag": 2, "args": [2, 3, 200.0, 2.0e5, 1000.0, 1]}
        self.element_manager.handle("element", beam_data)

        # 验证元素是否被正确存储
        self.assertIn(1, self.element_manager.elements)
        self.assertIn(2, self.element_manager.elements)

        # 验证元素类型是否正确
        self.assertEqual(self.element_manager.elements[1]["type"], "Truss")
        self.assertEqual(self.element_manager.elements[2]["type"], "elasticBeamColumn")

        # 验证节点连接关系是否正确
        self.assertEqual(self.element_manager.element_nodes[1], [1, 2])
        self.assertEqual(self.element_manager.element_nodes[2], [2, 3])

        # 测试按节点查找元素
        elements = self.element_manager.get_elements_by_nodes([2])
        self.assertEqual(set(elements), {1, 2})

        # 测试按类型查找元素
        elements = self.element_manager.get_elements_by_type("Truss")
        self.assertEqual(elements, [1])

    def test_load_manager(self):
        """测试LoadManager的基本功能"""
        # 测试创建荷载模式
        pattern_data = {"typeName": "Plain", "tag": 1, "args": [1, "-factor", 1.5]}
        self.load_manager.handle("pattern", pattern_data)

        # 验证荷载模式是否被正确存储
        self.assertIn(1, self.load_manager.patterns)
        self.assertEqual(self.load_manager.patterns[1]["type"], "Plain")
        self.assertEqual(self.load_manager.patterns[1]["tsTag"], 1)
        self.assertEqual(self.load_manager.patterns[1]["factor"], 1.5)

        # 验证当前荷载模式是否正确设置
        self.assertEqual(self.load_manager.current_pattern, 1)

        # 测试添加节点荷载
        load_data = {"tag": 1, "args": [1000.0, 0.0, -500.0]}
        self.load_manager.handle("load", load_data)

        # 验证节点荷载是否正确存储
        load_key = (1, 1)  # (patternTag, nodeTag)
        self.assertIn(load_key, self.load_manager.node_loads)
        self.assertEqual(self.load_manager.node_loads[load_key], [1000.0, 0.0, -500.0])

        # 测试获取节点荷载
        node_load = self.load_manager.get_node_load(1, 1)
        self.assertEqual(node_load, [1000.0, 0.0, -500.0])


if __name__ == "__main__":
    unittest.main()
