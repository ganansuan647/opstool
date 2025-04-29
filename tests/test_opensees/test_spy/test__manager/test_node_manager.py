import unittest
import importlib.util
from pathlib import Path
import sys
import os

# 首先将spy/_manager目录添加到sys.path，以便动态导入模块
spy_manager_path = str(Path(__file__).resolve().parents[1] / "opstool" / "opensees" / "spy" / "_manager")
sys.path.insert(0, spy_manager_path)

# 先导入BaseHandler
base_path = os.path.join(spy_manager_path, "_BaseHandler.py")
spec = importlib.util.spec_from_file_location("BaseHandler", base_path)
base_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base_module)
BaseHandler = base_module.BaseHandler

# 然后导入NodeManager
node_path = os.path.join(spy_manager_path, "_NodeManager.py")
# 创建一个自定义加载器，用于重写模块的__file__属性
spec = importlib.util.spec_from_file_location("NodeManager", node_path)
node_module = importlib.util.module_from_spec(spec)

# 在导入前添加所需的全局变量
node_module.BaseHandler = BaseHandler  # 提供BaseHandler给NodeManager使用

spec.loader.exec_module(node_module)
NodeManager = node_module.NodeManager


class TestNodeManager(unittest.TestCase):
    def setUp(self):
        """每个测试前初始化一个NodeManager实例"""
        self.node_manager = NodeManager()

    def test_handle_node(self):
        """测试节点数据处理功能"""
        # 2D节点情况
        cmd = "node"
        args = (1, 10.0, 20.0)
        parsed = BaseHandler.parse_command(cmd, args, {})
        self.node_manager.handle(cmd, parsed)

        # 检查节点是否正确存储
        self.assertIn(1, self.node_manager.nodes)
        node_data = self.node_manager.nodes[1]
        self.assertEqual(node_data["coords"], [10.0, 20.0])

        # 3D节点情况
        cmd = "node"
        args = (2, 10.0, 20.0, 30.0, "-ndf", 6)
        parsed = BaseHandler.parse_command(cmd, args, {})
        self.node_manager.handle(cmd, parsed)

        # 检查节点是否正确存储
        self.assertIn(2, self.node_manager.nodes)
        node_data = self.node_manager.nodes[2]
        self.assertEqual(node_data["coords"], [10.0, 20.0, 30.0])
        self.assertEqual(node_data["ndf"], 6)

    def test_handle_mass(self):
        """测试质量处理功能"""
        # 先创建节点
        cmd = "node"
        args = (1, 10.0, 20.0)
        parsed = BaseHandler.parse_command(cmd, args, {})
        self.node_manager.handle(cmd, parsed)

        # 添加质量
        cmd = "mass"
        args = (1, 1.5, 2.5, 3.5)
        parsed = BaseHandler.parse_command(cmd, args, {})
        self.node_manager.handle(cmd, parsed)

        # 检查质量是否正确存储
        self.assertIn(1, self.node_manager.nodes)
        node_data = self.node_manager.nodes[1]
        self.assertIn("mass", node_data)
        self.assertEqual(node_data["mass"], [1.5, 2.5, 3.5])

    def test_handle_model(self):
        """测试模型设置处理功能"""
        cmd = "model"
        args = ("basic", "-ndm", 3, "-ndf", 6)
        parsed = BaseHandler.parse_command(cmd, args, {})
        self.node_manager.handle(cmd, parsed)

        # 检查模型维度和自由度是否正确设置
        self.assertEqual(self.node_manager.dims, 3)
        self.assertEqual(self.node_manager.ndf, 6)

    def test_get_node_coords(self):
        """测试获取节点坐标功能"""
        # 创建测试节点
        cmd = "node"
        args = (1, 10.0, 20.0, 30.0)
        parsed = BaseHandler.parse_command(cmd, args, {})
        self.node_manager.handle(cmd, parsed)

        # 测试获取坐标
        coords = self.node_manager.get_node_coords(1)
        self.assertEqual(coords, [10.0, 20.0, 30.0])

        # 测试获取不存在节点的坐标
        coords = self.node_manager.get_node_coords(999)
        self.assertEqual(coords, [])

    def test_get_nodes_by_coords(self):
        """测试通过坐标查找节点功能"""
        # 创建测试节点
        cmd = "node"
        args1 = (1, 10.0, 20.0, 30.0)
        args2 = (2, 10.0, 20.0, 40.0)
        args3 = (3, 20.0, 30.0, 40.0)

        for args in [args1, args2, args3]:
            parsed = BaseHandler.parse_command(cmd, args, {})
            self.node_manager.handle(cmd, parsed)

        # 测试通过x坐标查询
        nodes = self.node_manager.get_nodes_by_coords(x=10.0)
        self.assertEqual(set(nodes), {1, 2})

        # 测试通过x,y坐标查询
        nodes = self.node_manager.get_nodes_by_coords(x=10.0, y=20.0)
        self.assertEqual(set(nodes), {1, 2})

        # 测试通过完整坐标查询
        nodes = self.node_manager.get_nodes_by_coords(x=10.0, y=20.0, z=30.0)
        self.assertEqual(set(nodes), {1})

        # 测试无匹配情况
        nodes = self.node_manager.get_nodes_by_coords(x=99.0)
        self.assertEqual(nodes, [])


if __name__ == "__main__":
    unittest.main()
