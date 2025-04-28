"""Pytest configuration file to stub unavailable external dependencies."""

from types import ModuleType
import sys

# Create a minimal dummy module for `openseespy` and its sub-module `opensees`.
openseespy_stub = ModuleType("openseespy")
opensees_module_stub = ModuleType("openseespy.opensees")
# Expose the sub-module as an attribute of the parent to mimic the real package structure.
setattr(openseespy_stub, "opensees", opensees_module_stub)

# Create a minimal dummy module for `gmsh` since it relies on native bindings
# that are unavailable in most CI environments.
gmsh_stub = ModuleType("gmsh")


# Provide dummy API frequently referenced in the codebase.  We only implement
# symbols that are *imported* at module level inside `opstool`, so the exact
# behaviour is irrelevant – they are never invoked by our unit-tests.
def _noop(*_args, **_kwargs):  # type: ignore
    """A dummy no-operation replacement for OpenSeesPy functions."""


for _name in (
    "initialize",
    "model",
    "finalize",
):
    setattr(gmsh_stub, _name, _noop)
# Register the stub before any library tries to import ``gmsh``.
sys.modules.setdefault("gmsh", gmsh_stub)

# Register stubs in ``sys.modules`` so that ``import openseespy`` and
# ``import openseespy.opensees as ops`` both succeed without requiring the
# native OpenSeesPy binaries that are unavailable in CI or test environments.
sys.modules.setdefault("openseespy", openseespy_stub)
sys.modules.setdefault("openseespy.opensees", opensees_module_stub)

# Prevent accidental attribute errors when the tested code accesses common
# OpenSeesPy API by providing no-op fallbacks.  We keep the surface minimal –
# extend as needed by additional tests.

for _name in (
    "wipe",
    "model",
    "node",
    "element",
    "uniaxialMaterial",
):
    setattr(opensees_module_stub, _name, _noop)

# Stub for the Windows-only helper package automatically imported by
# `openseespy`.  This avoids the initial ImportError raised by the real
# package when the native DLL is missing.
openseespywin_stub = ModuleType("openseespywin")
sys.modules.setdefault("openseespywin", openseespywin_stub)
