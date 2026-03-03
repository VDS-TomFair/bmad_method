"""
Unit tests for _90_langfuse_tool_end.py (Story 004)
ACs covered: AC-007 (status flag), AC-008 (memory_load result count)
"""
import sys
import os
import types
import unittest
from unittest.mock import MagicMock, AsyncMock

# ── Pre-stub heavy A0 dependencies before any imports ──────────────────────
# This prevents litellm/models/agent import chain from running in test env.
for mod_name in [
    'litellm', 'simpleeval', 'regex',
    'models',
    'agent',
    'python', 'python.helpers', 'python.helpers.extension',
    'python.helpers.tool', 'python.helpers.extract_tools',
    'python.helpers.files', 'python.helpers.tokens',
    'python.helpers.errors', 'python.helpers.log',
    'python.helpers.defer', 'python.helpers.dirty_json',
    'python.helpers.plugins',
]:
    if mod_name not in sys.modules:
        sys.modules[mod_name] = MagicMock()

# Stub Extension base class
class _FakeExtension:
    def __init__(self): pass
sys.modules['python.helpers.extension'].Extension = _FakeExtension

# Stub Response class
class _FakeResponse:
    def __init__(self, message): self.message = message
sys.modules['python.helpers.tool'].Response = _FakeResponse

# Ensure /a0 paths are available
for _p in ['/a0', '/a0/usr/plugins/langfuse-observability/extensions/python/tool_execute_after']:
    if _p not in sys.path:
        sys.path.insert(0, _p)

# Now safe to import
from _90_langfuse_tool_end import _parse_memory_load_count, LangfuseToolSpanEnd  # noqa: E402


# ── Tests for _parse_memory_load_count ─────────────────────────────────────

class TestParseMemoryLoadCount(unittest.TestCase):
    """AC-008: _parse_memory_load_count correctness"""

    def test_json_list_returns_length(self):
        out = '[{"id":1},{"id":2},{"id":3}]'
        self.assertEqual(_parse_memory_load_count(out), 3)

    def test_empty_json_list_returns_zero(self):
        self.assertEqual(_parse_memory_load_count('[]'), 0)

    def test_json_dict_with_count_key(self):
        out = '{"count": 5, "results": []}'
        self.assertEqual(_parse_memory_load_count(out), 5)

    def test_json_dict_with_results_list(self):
        out = '{"results": [{"a":1},{"a":2}]}'
        self.assertEqual(_parse_memory_load_count(out), 2)

    def test_json_dict_with_documents_list(self):
        out = '{"documents": ["x","y","z"]}'
        self.assertEqual(_parse_memory_load_count(out), 3)

    def test_json_dict_with_memories_list(self):
        out = '{"memories": ["a","b"]}'
        self.assertEqual(_parse_memory_load_count(out), 2)

    def test_malformed_json_returns_minus_one(self):
        self.assertEqual(_parse_memory_load_count('{not valid json'), -1)

    def test_empty_string_returns_minus_one(self):
        self.assertEqual(_parse_memory_load_count(''), -1)

    def test_plain_text_does_not_raise(self):
        result = _parse_memory_load_count('some plain text output')
        self.assertIsInstance(result, int)

    def test_whitespace_only_returns_minus_one(self):
        self.assertEqual(_parse_memory_load_count('   '), -1)


# ── Tests for LangfuseToolSpanEnd.execute ──────────────────────────────────

class TestLangfuseToolSpanEnd(unittest.IsolatedAsyncioTestCase):
    """AC-007: status flag on tool spans"""

    def _make_ext(self, tool_name='code_execution_tool', sampled=True):
        ext = object.__new__(LangfuseToolSpanEnd)
        ext.agent = MagicMock()
        loop_data = MagicMock()
        loop_data.params_persistent.get.side_effect = (
            lambda k, d=None: sampled if k == 'lf_sampled' else d
        )
        span = MagicMock()
        loop_data.params_temporary.get.return_value = span
        ext.agent.loop_data = loop_data
        return ext, span

    async def test_ac007_success_status_in_metadata(self):
        """AC-007: metadata.status = 'success' on normal execution"""
        ext, span = self._make_ext()
        resp = _FakeResponse('tool output text')
        await ext.execute(response=resp, tool_name='code_execution_tool')
        span.update.assert_called_once()
        kw = span.update.call_args[1]
        self.assertEqual(kw['metadata']['status'], 'success')
        span.end.assert_called_once()

    async def test_ac007_tool_name_in_metadata(self):
        """AC-007: metadata.tool_name set correctly"""
        ext, span = self._make_ext()
        resp = _FakeResponse('output')
        await ext.execute(response=resp, tool_name='search_engine')
        kw = span.update.call_args[1]
        self.assertEqual(kw['metadata']['tool_name'], 'search_engine')

    async def test_ac007_none_response_success_status(self):
        """AC-007: None response — status still success"""
        ext, span = self._make_ext()
        await ext.execute(response=None, tool_name='memory_save')
        span.update.assert_called_once()
        kw = span.update.call_args[1]
        self.assertEqual(kw['metadata']['status'], 'success')

    async def test_ac007_span_update_exception_sets_error_status(self):
        """AC-007: span.update() exception triggers error status retry"""
        ext, span = self._make_ext()
        span.update.side_effect = [RuntimeError('sdk error'), None]
        span.end.return_value = None
        resp = _FakeResponse('out')
        await ext.execute(response=resp, tool_name='response')
        self.assertEqual(span.update.call_count, 2)
        second_kw = span.update.call_args_list[1][1]
        self.assertEqual(second_kw['metadata']['status'], 'error')
        self.assertIn('error_message', second_kw['metadata'])

    async def test_ac008_memory_load_adds_returned_field(self):
        """AC-008: memory_load output includes returned count"""
        ext, span = self._make_ext()
        resp = _FakeResponse('[{"id":1},{"id":2}]')
        await ext.execute(response=resp, tool_name='memory_load')
        kw = span.update.call_args[1]
        output = kw['output']
        self.assertIsInstance(output, dict)
        self.assertIn('returned', output)
        self.assertEqual(output['returned'], 2)

    async def test_ac008_memory_load_bad_output_returns_minus_one(self):
        """AC-008: unparseable output → returned=-1, no raise"""
        ext, span = self._make_ext()
        resp = _FakeResponse('not parseable')
        await ext.execute(response=resp, tool_name='memory_load')
        kw = span.update.call_args[1]
        output = kw['output']
        self.assertIsInstance(output, dict)
        self.assertEqual(output['returned'], -1)

    async def test_ac009_non_memory_load_no_returned_field(self):
        """AC-009 regression: non-memory_load tools don't get 'returned'"""
        ext, span = self._make_ext()
        resp = _FakeResponse('some output')
        await ext.execute(response=resp, tool_name='search_engine')
        kw = span.update.call_args[1]
        output = kw['output']
        # For non-memory_load, output is plain string
        self.assertNotIsInstance(output, dict)

    async def test_no_span_returns_silently(self):
        """No span in loop_data → returns without error"""
        ext = object.__new__(LangfuseToolSpanEnd)
        ext.agent = MagicMock()
        loop_data = MagicMock()
        loop_data.params_persistent.get.return_value = True
        loop_data.params_temporary.get.return_value = None
        ext.agent.loop_data = loop_data
        await ext.execute(response=None, tool_name='memory_load')

    async def test_not_sampled_skips_span(self):
        """lf_sampled=False → skip without touching span"""
        ext, span = self._make_ext(sampled=False)
        await ext.execute(response=None, tool_name='memory_load')
        span.update.assert_not_called()


if __name__ == '__main__':
    unittest.main(verbosity=2)
