import unittest
import importlib.util
from pathlib import Path

# Dynamically load BaseHandler to avoid importing the full opstool package
file_path = Path(__file__).resolve().parents[1] / "opstool" / "opensees" / "spy" / "_manager" / "_BaseHandler.py"
spec = importlib.util.spec_from_file_location("_BaseHandler", str(file_path))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)  # type: ignore
BaseHandler = module.BaseHandler


class TestParseCommand(unittest.TestCase):
    def test_node(self):
        args = (1, 0.0, 0.0, "-ndf", 3, "-mass", 1.0, 1.0, 0.0)
        parsed = BaseHandler.parse_command("node", args, {})
        self.assertEqual(parsed["tag"], 1)
        self.assertEqual(parsed["coords"], [0.0, 0.0])
        self.assertEqual(parsed["ndf"], 3)
        self.assertEqual(parsed["mass"], [1.0, 1.0, 0.0])

    def test_mass(self):
        args = (1, 1.0, 1.0, 1.0)
        parsed = BaseHandler.parse_command("mass", args, {})
        self.assertEqual(parsed["tag"], 1)
        self.assertEqual(parsed["mass"], [1.0, 1.0, 1.0])

    def test_element(self):
        args = ("Truss", 1, 1, 2, 3.14, 1)
        parsed = BaseHandler.parse_command("element", args, {})
        self.assertEqual(parsed["typeName"], "Truss")
        self.assertEqual(parsed["tag"], 1)
        self.assertEqual(parsed["args"], [1, 2, 3.14, 1])

    def test_uniaxial_material(self):
        args = ("Elastic", 1, 2.0e5, 200.0)
        parsed = BaseHandler.parse_command("uniaxialMaterial", args, {})
        self.assertEqual(parsed["matType"], "Elastic")
        self.assertEqual(parsed["matTag"], 1)
        self.assertEqual(parsed["args"], [2.0e5, 200.0])

    def test_region(self):
        args = (1, "-ele", 1, 2, 3, "-rayleigh", 0.02, 0.03, 0.0, 0.0)
        parsed = BaseHandler.parse_command("region", args, {})
        self.assertEqual(parsed["tag"], 1)
        self.assertEqual(parsed["ele"], [1, 2, 3])
        self.assertEqual(parsed["rayleigh"], [0.02, 0.03, 0.0, 0.0])


if __name__ == "__main__":
    unittest.main()
