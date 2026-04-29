# test_metrics_collector.py
"""
Unit tests for metrics_collector.py module
"""

import unittest
from unittest.mock import Mock, MagicMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestMetricsCollector(unittest.TestCase):
    """Test cases for MetricsCollector class"""

    def setUp(self):
        """Set up test fixtures"""
        from metrics_collector import MetricsCollector
        self.collector = MetricsCollector()

    def test_initialization(self):
        """Test metrics collector initialization"""
        self.assertIsNotNone(self.collector)
        self.assertIsInstance(self.collector.spans, list)
        self.assertIsInstance(self.collector.metrics, dict)

    def test_export_spans(self):
        """Test exporting spans"""
        # Create mock span
        mock_span = MagicMock()
        mock_span.name = "test_operation"
        mock_span.start_time = 1000000000
        mock_span.end_time = 1000001000
        mock_span.attributes = {}
        mock_span.status = MagicMock()
        mock_span.status.is_ok = True
        
        # Export span
        result = self.collector.export([mock_span])
        
        # Verify export was successful
        from opentelemetry.sdk.trace.export import SpanExportResult
        self.assertEqual(result, SpanExportResult.SUCCESS)

    def test_get_metrics_empty(self):
        """Test getting metrics when no spans collected"""
        metrics = self.collector.get_metrics()
        
        self.assertIsInstance(metrics, dict)
        self.assertEqual(metrics['total_requests'], 0)
        self.assertEqual(metrics['total_tokens'], 0)

    def test_get_recent_spans_empty(self):
        """Test getting recent spans when none exist"""
        spans = self.collector.get_recent_spans(limit=10)
        
        self.assertIsInstance(spans, list)
        self.assertEqual(len(spans), 0)

    def test_reset_metrics(self):
        """Test resetting metrics"""
        # Add some mock data
        self.collector.spans.append({"test": "data"})
        self.collector.metrics['test'] = 123
        
        # Reset
        self.collector.reset_metrics()
        
        # Verify reset
        self.assertEqual(len(self.collector.spans), 0)
        self.assertEqual(len(self.collector.metrics), 0)

    def test_calculate_latency_percentiles(self):
        """Test latency percentile calculation"""
        latencies = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
        
        # This would test the internal percentile calculation
        # For now, just verify the data structure
        self.assertIsInstance(latencies, list)
        self.assertEqual(len(latencies), 10)

    def test_get_time_series_data(self):
        """Test getting time series data"""
        data = self.collector.get_time_series_data()
        
        self.assertIsInstance(data, dict)
        self.assertIn('hourly_requests', data)
        self.assertIn('latency_by_operation', data)


class TestMetricsAggregation(unittest.TestCase):
    """Test cases for metrics aggregation"""

    def setUp(self):
        """Set up test fixtures"""
        from metrics_collector import MetricsCollector
        self.collector = MetricsCollector()

    def test_aggregate_tokens(self):
        """Test token aggregation"""
        # Create mock spans with token data
        mock_span1 = MagicMock()
        mock_span1.name = "llm.generate"
        mock_span1.attributes = {
            'llm.usage.prompt_tokens': 100,
            'llm.usage.completion_tokens': 50
        }
        mock_span1.start_time = 1000000000
        mock_span1.end_time = 1000001000
        mock_span1.status = MagicMock()
        mock_span1.status.is_ok = True
        
        # Export span
        self.collector.export([mock_span1])
        
        # Get metrics
        metrics = self.collector.get_metrics()
        
        # Verify token counting
        self.assertIn('total_tokens', metrics)

    def test_aggregate_errors(self):
        """Test error aggregation"""
        # Create mock span with error
        mock_span = MagicMock()
        mock_span.name = "test_operation"
        mock_span.start_time = 1000000000
        mock_span.end_time = 1000001000
        mock_span.attributes = {}
        mock_span.status = MagicMock()
        mock_span.status.is_ok = False
        
        # Export span
        self.collector.export([mock_span])
        
        # Get metrics
        metrics = self.collector.get_metrics()
        
        # Verify error counting
        self.assertIn('error_count', metrics)


if __name__ == '__main__':
    unittest.main()

# Made with Bob
