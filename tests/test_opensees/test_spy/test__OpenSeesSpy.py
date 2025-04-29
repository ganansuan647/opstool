"""
测试OpenSeesSpy类
"""
import pytest
# 从模块导入需要测试的类
from opstool.opensees.spy import OpenSeesSpy


class TestOpenSeesSpy():
    """测试OpenSeesSpy类"""

    def setUp(self):
        """初始化测试环境"""
        import matplotlib.pyplot as plt
        import openseespy.opensees as ops
        # 创建 spy 并挂钩所有命令
        self.spy = OpenSeesSpy(ops)
        self.spy.hook_all()

    def test_model(self):
        """测试模型设置处理功能"""
        cmd = "model"
        args = ("basic", "-ndm", 3, "-ndf", 6)
        parsed = BaseHandler.parse_command(cmd, args, {})
        self.spy.node_manager.handle(cmd, parsed)

        # 检查模型维度和自由度是否正确设置
        self.assertEqual(self.spy.node_manager.dims, 3)
        self.assertEqual(self.spy.node_manager.dofs, 6)

