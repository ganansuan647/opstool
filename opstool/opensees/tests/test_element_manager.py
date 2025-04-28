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

# 然后导入ElementManager
element_path = os.path.join(spy_manager_path, "_ElementManager.py")
spec = importlib.util.spec_from_file_location("ElementManager", element_path)
element_module = importlib.util.module_from_spec(spec)

# 在导入前添加所需的全局变量
element_module.BaseHandler = BaseHandler  # 提供BaseHandler给ElementManager使用

spec.loader.exec_module(element_module)
ElementManager = element_module.ElementManager


class TestElementManager(unittest.TestCase):
    def setUp(self):
        """每个测试前初始化一个ElementManager实例"""
        self.element_manager = ElementManager()

    def test_handle_truss(self):
        """测试桁架单元处理"""
        cmd = "element"
        args = ("Truss", 1, 10, 20, 100.5, 3)
        parsed = BaseHandler.parse_command(cmd, args, {})
        self.element_manager.handle(cmd, parsed)

        # 验证元素是否正确存储
        self.assertIn(1, self.element_manager.elements)
        element = self.element_manager.elements[1]
        self.assertEqual(element["type"], "Truss")
        self.assertEqual(element["nodes"], [10, 20])
        self.assertEqual(element["A"], 100.5)
        self.assertEqual(element["matTag"], 3)

        # 验证节点连接是否正确记录
        self.assertIn(1, self.element_manager.element_nodes)
        self.assertEqual(self.element_manager.element_nodes[1], [10, 20])

    def test_handle_elastic_beam_column(self):
        """测试弹性梁柱单元处理"""
        cmd = "element"
        args = ("elasticBeamColumn", 2, 10, 20, 100.0, 2.0e5, 1000.0, 1)
        parsed = BaseHandler.parse_command(cmd, args, {})
        self.element_manager.handle(cmd, parsed)

        # 验证元素是否正确存储
        self.assertIn(2, self.element_manager.elements)
        element = self.element_manager.elements[2]
        self.assertEqual(element["type"], "elasticBeamColumn")
        self.assertEqual(element["nodes"], [10, 20])
        self.assertEqual(element["A"], 100.0)
        self.assertEqual(element["E"], 2.0e5)
        self.assertEqual(element["Iz"], 1000.0)
        self.assertEqual(element["transfTag"], 1)

    def test_handle_disp_beam_column(self):
        """测试位移法非线性梁柱单元处理"""
        cmd = "element"
        args = ("dispBeamColumn", 3, 10, 20, 5, 2, 1)
        parsed = BaseHandler.parse_command(cmd, args, {})
        self.element_manager.handle(cmd, parsed)

        # 验证元素是否正确存储
        self.assertIn(3, self.element_manager.elements)
        element = self.element_manager.elements[3]
        self.assertEqual(element["type"], "dispBeamColumn")
        self.assertEqual(element["nodes"], [10, 20])
        self.assertEqual(element["numIntgrPts"], 5)
        self.assertEqual(element["secTag"], 2)
        self.assertEqual(element["transfTag"], 1)

    def test_handle_zero_length(self):
        """测试零长度单元处理"""
        cmd = "element"
        args = ("zeroLength", 4, 10, 20, "-mat", 1, 2, 3, "-dir", 1, 2, 3)
        parsed = BaseHandler.parse_command(cmd, args, {})
        self.element_manager.handle(cmd, parsed)

        # 验证元素是否正确存储
        self.assertIn(4, self.element_manager.elements)
        element = self.element_manager.elements[4]
        self.assertEqual(element["type"], "zeroLength")
        self.assertEqual(element["nodes"], [10, 20])
        self.assertEqual(element["materials"], [1, 2, 3])
        self.assertEqual(element["directions"], [1, 2, 3])

    def test_handle_quad(self):
        """测试四节点平面单元处理"""
        cmd = "element"
        args = ("quad", 5, 10, 20, 30, 40, 0.2, 1)
        parsed = BaseHandler.parse_command(cmd, args, {})
        self.element_manager.handle(cmd, parsed)

        # 验证元素是否正确存储
        self.assertIn(5, self.element_manager.elements)
        element = self.element_manager.elements[5]
        self.assertEqual(element["type"], "quad")
        self.assertEqual(element["nodes"], [10, 20, 30, 40])
        self.assertEqual(element["thickness"], 0.2)
        self.assertEqual(element["matTag"], 1)

    def test_handle_shell(self):
        """测试壳单元处理"""
        cmd = "element"
        args = ("ShellMITC4", 6, 10, 20, 30, 40, 2)
        parsed = BaseHandler.parse_command(cmd, args, {})
        self.element_manager.handle(cmd, parsed)

        # 验证元素是否正确存储
        self.assertIn(6, self.element_manager.elements)
        element = self.element_manager.elements[6]
        self.assertEqual(element["type"], "ShellMITC4")
        self.assertEqual(element["nodes"], [10, 20, 30, 40])
        self.assertEqual(element["secTag"], 2)

    def test_get_element_nodes(self):
        """测试获取元素节点功能"""
        # 创建测试元素
        cmd = "element"
        args = ("Truss", 1, 10, 20, 100.0, 1)
        parsed = BaseHandler.parse_command(cmd, args, {})
        self.element_manager.handle(cmd, parsed)

        # 测试获取节点
        nodes = self.element_manager.get_element_nodes(1)
        self.assertEqual(nodes, [10, 20])

        # 测试获取不存在元素的节点
        nodes = self.element_manager.get_element_nodes(999)
        self.assertEqual(nodes, [])

    def test_get_elements_by_nodes(self):
        """测试通过节点查找元素功能"""
        # 创建测试元素
        cmd = "element"
        args1 = ("Truss", 1, 10, 20, 100.0, 1)
        args2 = ("Truss", 2, 20, 30, 100.0, 1)
        args3 = ("Truss", 3, 10, 30, 100.0, 1)

        for args in [args1, args2, args3]:
            parsed = BaseHandler.parse_command(cmd, args, {})
            self.element_manager.handle(cmd, parsed)

        # 测试通过单个节点查询
        elements = self.element_manager.get_elements_by_nodes([10])
        self.assertEqual(set(elements), {1, 3})

        # 测试通过多个节点查询(精确匹配)
        elements = self.element_manager.get_elements_by_nodes([10, 20])
        self.assertEqual(set(elements), {1})

        # 测试无匹配情况
        elements = self.element_manager.get_elements_by_nodes([99])
        self.assertEqual(elements, [])

    def test_get_elements_by_type(self):
        """测试通过类型查找元素功能"""
        # 创建不同类型的测试元素
        cmd = "element"
        args1 = ("Truss", 1, 10, 20, 100.0, 1)
        args2 = ("elasticBeamColumn", 2, 20, 30, 100.0, 2.0e5, 1000.0, 1)
        args3 = ("Truss", 3, 30, 40, 200.0, 1)

        for args in [args1, args2, args3]:
            parsed = BaseHandler.parse_command(cmd, args, {})
            self.element_manager.handle(cmd, parsed)

        # 测试按类型查询
        elements = self.element_manager.get_elements_by_type("Truss")
        self.assertEqual(set(elements), {1, 3})

        elements = self.element_manager.get_elements_by_type("elasticBeamColumn")
        self.assertEqual(set(elements), {2})

        # 测试大小写不敏感
        elements = self.element_manager.get_elements_by_type("truss")
        self.assertEqual(set(elements), {1, 3})

        # 测试无匹配情况
        elements = self.element_manager.get_elements_by_type("unknownType")
        self.assertEqual(elements, [])


if __name__ == "__main__":
    unittest.main()
