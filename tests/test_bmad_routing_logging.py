import ast
import unittest
from pathlib import Path

EXT_FILE = Path(__file__).resolve().parents[1] / "extensions" / "python" / "message_loop_prompts_after" / "_80_bmad_routing_manifest.py"


def _get_bare_excepts(source: str) -> list[dict]:
    """Find bare except blocks that only contain 'pass' or no body."""
    tree = ast.parse(source)
    bare = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler):
            body = node.body
            # Check if body is just 'pass'
            if len(body) == 1 and isinstance(body[0], ast.Pass):
                bare.append({"line": node.lineno, "type": "except_pass"})
            # Check if body is just Expr with a constant 'pass'-like no-op
            elif len(body) == 1 and isinstance(body[0], ast.Expr):
                # Could be a log call, that's fine
                pass
    return bare


def _find_function_at_line(source: str, target_line: int) -> str:
    """Find the function/class containing a given line number."""
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.lineno <= target_line <= (node.end_lineno or target_line):
                return node.name
    return "<module>"


class TestRoutingExtensionLogging(unittest.TestCase):
    # A5: No bare except: pass at top-level scope of execute() or _build_staleness_warnings()

    def test_imports_logging(self):
        source = EXT_FILE.read_text()
        self.assertIn("import logging", source)
        self.assertIn("logging.getLogger(__name__)", source)

    def test_imports_traceback(self):
        source = EXT_FILE.read_text()
        self.assertIn("import traceback", source)

    def test_no_bare_except_pass_at_top_level(self):
        """execute() and _build_staleness_warnings() must not have bare except: pass."""
        source = EXT_FILE.read_text()
        tree = ast.parse(source)

        # Find top-level functions and their except handlers
        top_level_funcs = {"execute", "_build_staleness_warnings"}
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.name in top_level_funcs:
                    for child in ast.walk(node):
                        if isinstance(child, ast.ExceptHandler):
                            body = child.body
                            # Bare except: pass is forbidden at top-level
                            if len(body) == 1 and isinstance(body[0], ast.Pass):
                                self.fail(
                                    f"Bare 'except: pass' at line {child.lineno} "
                                    f"in function {node.name}"
                                )

    def test_execute_except_calls_log_warning(self):
        """execute() outermost except should call log.warning, not pass."""
        source = EXT_FILE.read_text()
        tree = ast.parse(source)

        for node in ast.walk(tree):
            if isinstance(node, ast.AsyncFunctionDef) and node.name == "execute":
                # Find the outermost except handlers
                for child in ast.walk(node):
                    if isinstance(child, ast.Try):
                        for handler in child.handlers:
                            # Check if this handler is near the end of the function
                            if handler.lineno > 425:
                                body = handler.body
                                # Must have a log.warning call
                                has_log = any(
                                    isinstance(stmt, ast.Expr)
                                    and isinstance(stmt.value, ast.Call)
                                    and isinstance(stmt.value.func, ast.Attribute)
                                    and stmt.value.func.attr == "warning"
                                    for stmt in body
                                )
                                self.assertTrue(
                                    has_log,
                                    f"execute() outermost except at line {handler.lineno} "
                                    f"must call log.warning()"
                                )

    def test_staleness_except_calls_log_warning(self):
        """_build_staleness_warnings() except should call log.warning."""
        source = EXT_FILE.read_text()
        tree = ast.parse(source)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "_build_staleness_warnings":
                for child in ast.walk(node):
                    if isinstance(child, ast.ExceptHandler):
                        body = child.body
                        has_log = any(
                            isinstance(stmt, ast.Expr)
                            and isinstance(stmt.value, ast.Call)
                            and isinstance(stmt.value.func, ast.Attribute)
                            and stmt.value.func.attr == "warning"
                            for stmt in body
                        )
                        self.assertTrue(
                            has_log,
                            f"_build_staleness_warnings() except at line {child.lineno} "
                            f"must call log.warning()"
                        )


if __name__ == "__main__":
    unittest.main()
