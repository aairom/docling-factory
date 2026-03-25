"""
OpenLLMetry Metrics Collector
Collects and aggregates metrics from OpenTelemetry traces for dashboard display.
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import threading
import time

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider, ReadableSpan
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult
from opentelemetry.sdk.resources import Resource

logger = logging.getLogger(__name__)


class MetricsCollector(SpanExporter):
    """
    Custom span exporter that collects metrics from OpenTelemetry spans.
    Stores metrics in memory for dashboard display.
    """
    
    def __init__(self, max_history: int = 1000):
        """
        Initialize metrics collector.
        
        Args:
            max_history: Maximum number of spans to keep in history
        """
        self.max_history = max_history
        self.spans: List[Dict] = []
        self.metrics: Dict = {
            "total_requests": 0,
            "total_tokens": 0,
            "total_latency_ms": 0,
            "error_count": 0,
            "operations": defaultdict(int),
            "models_used": defaultdict(int),
            "hourly_requests": defaultdict(int),
            "latency_by_operation": defaultdict(list),
        }
        self.lock = threading.Lock()
        logger.info("MetricsCollector initialized")
    
    def export(self, spans: List[ReadableSpan]) -> SpanExportResult:
        """Export spans and collect metrics."""
        with self.lock:
            for span in spans:
                self._process_span(span)
        return SpanExportResult.SUCCESS
    
    def _process_span(self, span: ReadableSpan):
        """Process a single span and extract metrics."""
        try:
            # Extract span data
            span_data = {
                "name": span.name,
                "start_time": span.start_time,
                "end_time": span.end_time,
                "duration_ms": (span.end_time - span.start_time) / 1_000_000,  # Convert to ms
                "status": span.status.status_code.name,
                "attributes": dict(span.attributes) if span.attributes else {},
                "timestamp": datetime.fromtimestamp(span.start_time / 1_000_000_000)
            }
            
            # Add to history
            self.spans.append(span_data)
            if len(self.spans) > self.max_history:
                self.spans.pop(0)
            
            # Update metrics
            self.metrics["total_requests"] += 1
            self.metrics["operations"][span.name] += 1
            self.metrics["total_latency_ms"] += span_data["duration_ms"]
            
            # Track errors
            if span.status.status_code.name == "ERROR":
                self.metrics["error_count"] += 1
            
            # Extract tokens from attributes
            if span.attributes:
                attrs = dict(span.attributes)
                
                # Track model usage
                if "gen_ai.request.model" in attrs:
                    model = attrs["gen_ai.request.model"]
                    self.metrics["models_used"][model] += 1
                
                # Track tokens
                prompt_tokens = attrs.get("gen_ai.usage.prompt_tokens", 0)
                completion_tokens = attrs.get("gen_ai.usage.completion_tokens", 0)
                total_tokens = prompt_tokens + completion_tokens
                
                if total_tokens > 0:
                    self.metrics["total_tokens"] += total_tokens
                    span_data["tokens"] = {
                        "prompt": prompt_tokens,
                        "completion": completion_tokens,
                        "total": total_tokens
                    }
            
            # Track hourly requests
            hour_key = span_data["timestamp"].strftime("%Y-%m-%d %H:00")
            self.metrics["hourly_requests"][hour_key] += 1
            
            # Track latency by operation
            self.metrics["latency_by_operation"][span.name].append(span_data["duration_ms"])
            
        except Exception as e:
            logger.error(f"Error processing span: {e}")
    
    def get_metrics(self) -> Dict:
        """Get current metrics summary."""
        with self.lock:
            # Calculate averages
            avg_latency = (
                self.metrics["total_latency_ms"] / self.metrics["total_requests"]
                if self.metrics["total_requests"] > 0
                else 0
            )
            
            # Calculate latency percentiles by operation
            latency_stats = {}
            for op, latencies in self.metrics["latency_by_operation"].items():
                if latencies:
                    sorted_latencies = sorted(latencies)
                    latency_stats[op] = {
                        "min": min(latencies),
                        "max": max(latencies),
                        "avg": sum(latencies) / len(latencies),
                        "p50": sorted_latencies[len(sorted_latencies) // 2],
                        "p95": sorted_latencies[int(len(sorted_latencies) * 0.95)],
                        "p99": sorted_latencies[int(len(sorted_latencies) * 0.99)],
                    }
            
            return {
                "total_requests": self.metrics["total_requests"],
                "total_tokens": self.metrics["total_tokens"],
                "avg_latency_ms": round(avg_latency, 2),
                "error_count": self.metrics["error_count"],
                "error_rate": (
                    round(self.metrics["error_count"] / self.metrics["total_requests"] * 100, 2)
                    if self.metrics["total_requests"] > 0
                    else 0
                ),
                "operations": dict(self.metrics["operations"]),
                "models_used": dict(self.metrics["models_used"]),
                "latency_stats": latency_stats,
                "hourly_requests": dict(sorted(self.metrics["hourly_requests"].items())),
            }
    
    def get_recent_spans(self, limit: int = 50) -> List[Dict]:
        """Get recent spans for detailed view."""
        with self.lock:
            return self.spans[-limit:][::-1]  # Return most recent first
    
    def get_time_series_data(self, hours: int = 24) -> Dict:
        """Get time series data for charts."""
        with self.lock:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            # Filter spans within time window
            recent_spans = [
                s for s in self.spans
                if s["timestamp"] >= cutoff_time
            ]
            
            # Group by hour
            hourly_data = defaultdict(lambda: {
                "requests": 0,
                "tokens": 0,
                "latency_sum": 0,
                "errors": 0
            })
            
            for span in recent_spans:
                hour_key = span["timestamp"].strftime("%Y-%m-%d %H:00")
                hourly_data[hour_key]["requests"] += 1
                hourly_data[hour_key]["latency_sum"] += span["duration_ms"]
                
                if span["status"] == "ERROR":
                    hourly_data[hour_key]["errors"] += 1
                
                if "tokens" in span:
                    hourly_data[hour_key]["tokens"] += span["tokens"]["total"]
            
            # Calculate averages
            for hour_data in hourly_data.values():
                if hour_data["requests"] > 0:
                    hour_data["avg_latency"] = hour_data["latency_sum"] / hour_data["requests"]
            
            return dict(sorted(hourly_data.items()))
    
    def reset_metrics(self):
        """Reset all metrics."""
        with self.lock:
            self.spans.clear()
            self.metrics = {
                "total_requests": 0,
                "total_tokens": 0,
                "total_latency_ms": 0,
                "error_count": 0,
                "operations": defaultdict(int),
                "models_used": defaultdict(int),
                "hourly_requests": defaultdict(int),
                "latency_by_operation": defaultdict(list),
            }
            logger.info("Metrics reset")
    
    def shutdown(self):
        """Shutdown the exporter."""
        pass
    
    def force_flush(self, timeout_millis: int = 30000) -> bool:
        """Force flush any buffered spans."""
        return True


# Global metrics collector instance
_metrics_collector: Optional[MetricsCollector] = None


def get_metrics_collector() -> Optional[MetricsCollector]:
    """Get the global metrics collector instance."""
    return _metrics_collector


def set_metrics_collector(collector: MetricsCollector):
    """Set the global metrics collector instance."""
    global _metrics_collector
    _metrics_collector = collector
    logger.info("Global metrics collector set")


def initialize_metrics_collector(max_history: int = 1000) -> MetricsCollector:
    """
    Initialize and configure the metrics collector.
    
    Args:
        max_history: Maximum number of spans to keep in history
        
    Returns:
        MetricsCollector instance
    """
    collector = MetricsCollector(max_history=max_history)
    set_metrics_collector(collector)
    return collector


# Made with Bob