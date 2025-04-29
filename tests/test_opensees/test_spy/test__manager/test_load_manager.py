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

# 然后导入LoadManager
load_path = os.path.join(spy_manager_path, "_LoadManager.py")
spec = importlib.util.spec_from_file_location("LoadManager", load_path)
load_module = importlib.util.module_from_spec(spec)

# 在导入前添加所需的全局变量
load_module.BaseHandler = BaseHandler  # 提供BaseHandler给LoadManager使用

spec.loader.exec_module(load_module)
LoadManager = load_module.LoadManager


class TestLoadManager(unittest.TestCase):
    def setUp(self):
        """每个测试前初始化一个LoadManager实例"""
        self.load_manager = LoadManager()

    def test_handle_pattern(self):
        """测试荷载模式处理"""
        cmd = "pattern"
        args = ("Plain", 1, 1, "-factor", 1.5)
        parsed = BaseHandler.parse_command(cmd, args, {})
        self.load_manager.handle(cmd, parsed)

        # 验证荷载模式是否正确存储
        self.assertIn(1, self.load_manager.patterns)
        pattern = self.load_manager.patterns[1]
        self.assertEqual(pattern["type"], "Plain")
        self.assertEqual(pattern["tsTag"], 1)
        self.assertEqual(pattern["factor"], 1.5)

        # 验证当前荷载模式是否正确设置
        self.assertEqual(self.load_manager.current_pattern, 1)

    def test_handle_load(self):
        """测试节点荷载处理"""
        # 先设置荷载模式
        cmd = "pattern"
        args = ("Plain", 1, 1)
        parsed = BaseHandler.parse_command(cmd, args, {})
        self.load_manager.handle(cmd, parsed)

        # 添加节点荷载
        cmd = "load"
        args = (10, 1000.0, 0.0, -500.0)
        parsed = BaseHandler.parse_command(cmd, args, {})
        self.load_manager.handle(cmd, parsed)

        # 验证节点荷载是否正确存储
        load_key = (1, 10)  # (patternTag, nodeTag)
        self.assertIn(load_key, self.load_manager.node_loads)
        load = self.load_manager.node_loads[load_key]
        self.assertEqual(load, [1000.0, 0.0, -500.0])

    def test_handle_ele_load(self):
        """测试单元荷载处理"""
        # 先设置荷载模式
        cmd = "pattern"
        args = ("Plain", 1, 1)
        parsed = BaseHandler.parse_command(cmd, args, {})
        self.load_manager.handle(cmd, parsed)

        # 添加单元荷载 - 使用-ele选项
        cmd = "eleLoad"
        args = ("-ele", 1, 2, 3, "-type", "-beamUniform", 0.0, -10.0)
        parsed = BaseHandler.parse_command(cmd, args, {})
        self.load_manager.handle(cmd, parsed)

        # 验证单元荷载是否正确存储
        for ele_tag in [1, 2, 3]:
            load_key = (1, ele_tag)  # (patternTag, eleTag)
            self.assertIn(load_key, self.load_manager.ele_loads)
            load = self.load_manager.ele_loads[load_key]
            self.assertEqual(load["type"], "-beamUniform")
            self.assertEqual(load["values"], [0.0, -10.0])

        # 添加单元荷载 - 使用-range选项
        cmd = "eleLoad"
        args = ("-range", 5, 7, "-type", "-beamUniform", 0.0, -5.0)
        parsed = BaseHandler.parse_command(cmd, args, {})
        self.load_manager.handle(cmd, parsed)

        # 验证单元荷载是否正确存储
        for ele_tag in [5, 6, 7]:
            load_key = (1, ele_tag)  # (patternTag, eleTag)
            self.assertIn(load_key, self.load_manager.ele_loads)
            load = self.load_manager.ele_loads[load_key]
            self.assertEqual(load["type"], "-beamUniform")
            self.assertEqual(load["values"], [0.0, -5.0])

    def test_get_pattern(self):
        """测试获取荷载模式功能"""
        # 创建测试荷载模式
        cmd = "pattern"
        args = ("Plain", 1, 1)
        parsed = BaseHandler.parse_command(cmd, args, {})
        self.load_manager.handle(cmd, parsed)

        # 测试获取荷载模式
        pattern = self.load_manager.get_pattern(1)
        self.assertEqual(pattern["type"], "Plain")
        self.assertEqual(pattern["tsTag"], 1)

        # 测试获取不存在的荷载模式
        pattern = self.load_manager.get_pattern(999)
        self.assertIsNone(pattern)

    def test_get_node_load(self):
        """测试获取节点荷载功能"""
        # 先设置荷载模式并添加荷载
        cmd = "pattern"
        args = ("Plain", 1, 1)
        parsed = BaseHandler.parse_command(cmd, args, {})
        self.load_manager.handle(cmd, parsed)

        cmd = "load"
        args = (10, 1000.0, 0.0, -500.0)
        parsed = BaseHandler.parse_command(cmd, args, {})
        self.load_manager.handle(cmd, parsed)

        # 测试获取节点荷载
        load = self.load_manager.get_node_load(1, 10)
        self.assertEqual(load, [1000.0, 0.0, -500.0])

        # 测试获取不存在的节点荷载
        load = self.load_manager.get_node_load(1, 999)
        self.assertEqual(load, [])

    def test_get_ele_load(self):
        """测试获取单元荷载功能"""
        # 先设置荷载模式并添加荷载
        cmd = "pattern"
        args = ("Plain", 1, 1)
        parsed = BaseHandler.parse_command(cmd, args, {})
        self.load_manager.handle(cmd, parsed)

        cmd = "eleLoad"
        args = ("-ele", 1, "-type", "-beamUniform", 0.0, -10.0)
        parsed = BaseHandler.parse_command(cmd, args, {})
        self.load_manager.handle(cmd, parsed)

        # 测试获取单元荷载
        load = self.load_manager.get_ele_load(1, 1)
        self.assertEqual(load["type"], "-beamUniform")
        self.assertEqual(load["values"], [0.0, -10.0])

        # 测试获取不存在的单元荷载
        load = self.load_manager.get_ele_load(1, 999)
        self.assertEqual(load, {})

    def test_get_patterns_by_time_series(self):
        """测试通过时程标签获取荷载模式功能"""
        # 创建使用相同时程的多个荷载模式
        cmd = "pattern"
        args1 = ("Plain", 1, 1)
        args2 = ("Plain", 2, 2)
        args3 = ("Plain", 3, 1)  # 使用与第一个相同的时程

        for args in [args1, args2, args3]:
            parsed = BaseHandler.parse_command(cmd, args, {})
            self.load_manager.handle(cmd, parsed)

        # 测试通过时程标签查询
        patterns = self.load_manager.get_patterns_by_time_series(1)
        self.assertEqual(set(patterns), {1, 3})

        patterns = self.load_manager.get_patterns_by_time_series(2)
        self.assertEqual(set(patterns), {2})

        # 测试无匹配情况
        patterns = self.load_manager.get_patterns_by_time_series(999)
        self.assertEqual(patterns, [])


if __name__ == "__main__":
    unittest.main()
