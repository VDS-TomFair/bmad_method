"""
Unit tests for langfuse_memory_trace.py helper (Story 004)
ACs covered: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, AC-010
"""
import sys
import os
import unittest
from unittest.mock import MagicMock, patch, call

# Add lib to path
sys.path.insert(0, '/a0/usr/plugins/langfuse-observability/extensions/python/lib')
# Add plugin helpers to path
sys.path.insert(0, '/a0/usr/plugins/langfuse-observability')


class TestRecordMemoryTrace(unittest.TestCase):

    def _make_mock_client(self):
        client = MagicMock()
        trace = MagicMock()
        generation = MagicMock()
        trace.generation.return_value = generation
        client.trace.return_value = trace
        return client, trace, generation

    def _make_mock_agent(self, profile='bmad-master', agent_number=0):
        agent = MagicMock()
        agent.number = agent_number
        agent.config.profile = profile
        agent.config.utility_model.name = 'gpt-4o-mini'
        return agent

    @patch('langfuse_memory_trace.get_langfuse_client')
    @patch('langfuse_memory_trace.approximate_tokens', return_value=42)
    def test_ac001_fragment_trace_name(self, mock_tokens, mock_client_fn):
        """AC-001: trace named bmad-memory-fragments is created"""
        client, trace, _ = self._make_mock_client()
        mock_client_fn.return_value = client
        from langfuse_memory_trace import record_memory_trace
        record_memory_trace(
            trace_name='bmad-memory-fragments',
            session_id='sess-001',
            user_id='Vanja',
            agent_profile='bmad-master',
            input_text='input',
            output_text='["frag1"]',
            item_count=1,
            item_key='fragment',
        )
        client.trace.assert_called_once()
        call_kwargs = client.trace.call_args[1]
        self.assertEqual(call_kwargs['name'], 'bmad-memory-fragments')

    @patch('langfuse_memory_trace.get_langfuse_client')
    @patch('langfuse_memory_trace.approximate_tokens', return_value=42)
    def test_ac002_solutions_trace_name(self, mock_tokens, mock_client_fn):
        """AC-002: trace named bmad-memory-solutions is created"""
        client, trace, _ = self._make_mock_client()
        mock_client_fn.return_value = client
        from langfuse_memory_trace import record_memory_trace
        record_memory_trace(
            trace_name='bmad-memory-solutions',
            session_id='sess-001',
            user_id='Vanja',
            agent_profile='bmad-dev',
            input_text='input',
            output_text='[{"problem":"p","solution":"s"}]',
            item_count=1,
            item_key='solution',
        )
        call_kwargs = client.trace.call_args[1]
        self.assertEqual(call_kwargs['name'], 'bmad-memory-solutions')

    @patch('langfuse_memory_trace.get_langfuse_client')
    @patch('langfuse_memory_trace.approximate_tokens', return_value=10)
    def test_ac003_identity_and_session_linkage(self, mock_tokens, mock_client_fn):
        """AC-003: userId, tags include bmad/bmad-memory/session:id, metadata.agent_profile"""
        client, trace, _ = self._make_mock_client()
        mock_client_fn.return_value = client
        from langfuse_memory_trace import record_memory_trace
        record_memory_trace(
            trace_name='bmad-memory-fragments',
            session_id='sess-abc',
            user_id='Vanja',
            agent_profile='bmad-dev',
            input_text='in',
            output_text='out',
            item_count=0,
            item_key='fragment',
        )
        kw = client.trace.call_args[1]
        self.assertEqual(kw['user_id'], 'Vanja')
        self.assertEqual(kw['session_id'], 'sess-abc')
        self.assertIn('bmad', kw['tags'])
        self.assertIn('bmad-memory', kw['tags'])
        self.assertIn('session:sess-abc', kw['tags'])
        self.assertEqual(kw['metadata']['agent_profile'], 'bmad-dev')

    @patch('langfuse_memory_trace.get_langfuse_client')
    @patch('langfuse_memory_trace.approximate_tokens', side_effect=[50, 30])
    def test_ac004_utility_llm_generation_span(self, mock_tokens, mock_client_fn):
        """AC-004: utility-llm generation child span is created with token data"""
        client, trace, generation = self._make_mock_client()
        mock_client_fn.return_value = client
        from langfuse_memory_trace import record_memory_trace
        record_memory_trace(
            trace_name='bmad-memory-fragments',
            session_id='s1',
            user_id='Vanja',
            agent_profile='bmad-master',
            input_text='prompt text',
            output_text='response text',
            item_count=2,
            item_key='fragment',
            model_name='gpt-4o-mini',
        )
        trace.generation.assert_called_once()
        gen_kw = trace.generation.call_args[1]
        self.assertEqual(gen_kw['name'], 'utility-llm')
        self.assertEqual(gen_kw['model'], 'gpt-4o-mini')
        self.assertIn('input', gen_kw['usage'])
        self.assertIn('output', gen_kw['usage'])
        self.assertIn('total', gen_kw['usage'])
        generation.end.assert_called_once()

    @patch('langfuse_memory_trace.get_langfuse_client')
    @patch('langfuse_memory_trace.approximate_tokens', return_value=5)
    def test_ac005_fragment_count_metadata(self, mock_tokens, mock_client_fn):
        """AC-005: fragment_count in trace metadata"""
        client, trace, _ = self._make_mock_client()
        mock_client_fn.return_value = client
        from langfuse_memory_trace import record_memory_trace
        record_memory_trace(
            trace_name='bmad-memory-fragments',
            session_id='s1', user_id='u', agent_profile='bmad-master',
            input_text='i', output_text='o', item_count=3, item_key='fragment',
        )
        kw = client.trace.call_args[1]
        self.assertEqual(kw['metadata']['fragment_count'], 3)

    @patch('langfuse_memory_trace.get_langfuse_client')
    @patch('langfuse_memory_trace.approximate_tokens', return_value=5)
    def test_ac006_solution_count_metadata(self, mock_tokens, mock_client_fn):
        """AC-006: solution_count in trace metadata"""
        client, trace, _ = self._make_mock_client()
        mock_client_fn.return_value = client
        from langfuse_memory_trace import record_memory_trace
        record_memory_trace(
            trace_name='bmad-memory-solutions',
            session_id='s1', user_id='u', agent_profile='bmad-sm',
            input_text='i', output_text='o', item_count=5, item_key='solution',
        )
        kw = client.trace.call_args[1]
        self.assertEqual(kw['metadata']['solution_count'], 5)

    @patch('langfuse_memory_trace.get_langfuse_client')
    @patch('langfuse_memory_trace.approximate_tokens', return_value=5)
    def test_ac001_zero_items_still_traces(self, mock_tokens, mock_client_fn):
        """AC-001/002: trace created even when item_count=0"""
        client, trace, _ = self._make_mock_client()
        mock_client_fn.return_value = client
        from langfuse_memory_trace import record_memory_trace
        record_memory_trace(
            trace_name='bmad-memory-fragments',
            session_id='s1', user_id='u', agent_profile='bmad-master',
            input_text='i', output_text='o', item_count=0, item_key='fragment',
        )
        client.trace.assert_called_once()

    @patch('langfuse_memory_trace.get_langfuse_client')
    def test_no_client_returns_silently(self, mock_client_fn):
        """If Langfuse disabled, function returns without error"""
        mock_client_fn.return_value = None
        from langfuse_memory_trace import record_memory_trace
        # Should not raise
        record_memory_trace(
            trace_name='bmad-memory-fragments',
            session_id='s', user_id='u', agent_profile='p',
            item_count=0, item_key='fragment',
        )

    @patch('langfuse_memory_trace.get_langfuse_client')
    @patch('langfuse_memory_trace.approximate_tokens', return_value=5)
    def test_exception_in_client_does_not_raise(self, mock_tokens, mock_client_fn):
        """Langfuse failure must NEVER propagate into caller"""
        client = MagicMock()
        client.trace.side_effect = RuntimeError('network error')
        mock_client_fn.return_value = client
        from langfuse_memory_trace import record_memory_trace
        # Must not raise
        record_memory_trace(
            trace_name='bmad-memory-fragments',
            session_id='s', user_id='u', agent_profile='p',
            item_count=0, item_key='fragment', input_text='x', output_text='y',
        )

    @patch('langfuse_memory_trace.get_langfuse_client')
    @patch('langfuse_memory_trace.approximate_tokens', return_value=5)
    def test_flush_called_after_trace(self, mock_tokens, mock_client_fn):
        """client.flush() must be called after trace creation"""
        client, trace, _ = self._make_mock_client()
        mock_client_fn.return_value = client
        from langfuse_memory_trace import record_memory_trace
        record_memory_trace(
            trace_name='bmad-memory-fragments',
            session_id='s', user_id='u', agent_profile='p',
            input_text='i', output_text='o', item_count=1, item_key='fragment',
        )
        client.flush.assert_called_once()

    @patch('langfuse_memory_trace.get_langfuse_client')
    @patch('langfuse_memory_trace.approximate_tokens', return_value=5)
    def test_ac010_specialist_agent_profile(self, mock_tokens, mock_client_fn):
        """AC-010: specialist agent profile correctly set"""
        client, trace, _ = self._make_mock_client()
        mock_client_fn.return_value = client
        from langfuse_memory_trace import record_memory_trace
        for profile in ['bmad-dev', 'bmad-sm', 'bmad-architect', 'bmad-pm']:
            client.reset_mock()
            trace.reset_mock()
            client.trace.return_value = trace
            record_memory_trace(
                trace_name='bmad-memory-fragments',
                session_id='s', user_id='u', agent_profile=profile,
                input_text='i', output_text='o', item_count=0, item_key='fragment',
            )
            kw = client.trace.call_args[1]
            self.assertEqual(kw['metadata']['agent_profile'], profile)
            self.assertIn(f'agent:{profile}', kw['tags'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
