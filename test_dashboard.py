#!/usr/bin/env python3
"""
Test script to verify the visual dashboard works correctly.
"""

from metrics_dashboard import create_full_dashboard

# Sample metrics data matching what metrics_collector returns
test_metrics = {
    "total_requests": 13,
    "total_tokens": 1500,
    "total_input_tokens": 800,
    "total_output_tokens": 700,
    "avg_latency_ms": 250.5,
    "error_count": 0,
    "error_rate": 0.0,
    "operations": {
        "llm_generate": 8,
        "generate_embedding": 5
    },
    "models_used": {
        "llama3.2:latest": 8,
        "granite-embedding:30m": 5
    },
    "latency_stats": {
        "llm_generate": {
            "min": 200.0,
            "max": 350.0,
            "avg": 275.0,
            "p50": 250.0,
            "p95": 340.0,
            "p99": 348.0
        },
        "generate_embedding": {
            "min": 50.0,
            "max": 100.0,
            "avg": 75.0,
            "p50": 70.0,
            "p95": 95.0,
            "p99": 98.0
        }
    },
    "hourly_requests": {
        "2024-01-15 10:00": 5,
        "2024-01-15 11:00": 8
    }
}

# Transform metrics for dashboard (same as in app_enhanced.py)
dashboard_metrics = dict(test_metrics)
latency_stats = test_metrics.get('latency_stats', {})

# Calculate overall latency percentiles from all operations
all_latencies = []
for op_stats in latency_stats.values():
    if 'min' in op_stats:
        all_latencies.append(op_stats['min'])
    if 'max' in op_stats:
        all_latencies.append(op_stats['max'])

if all_latencies:
    sorted_latencies = sorted(all_latencies)
    dashboard_metrics['min_latency'] = min(all_latencies)
    dashboard_metrics['max_latency'] = max(all_latencies)
    dashboard_metrics['p50_latency'] = sorted_latencies[len(sorted_latencies) // 2]
    dashboard_metrics['p95_latency'] = sorted_latencies[int(len(sorted_latencies) * 0.95)] if len(sorted_latencies) > 1 else sorted_latencies[0]
    dashboard_metrics['p99_latency'] = sorted_latencies[int(len(sorted_latencies) * 0.99)] if len(sorted_latencies) > 1 else sorted_latencies[0]
else:
    dashboard_metrics['min_latency'] = 0
    dashboard_metrics['max_latency'] = 0
    dashboard_metrics['p50_latency'] = 0
    dashboard_metrics['p95_latency'] = 0
    dashboard_metrics['p99_latency'] = 0

print("Testing dashboard with metrics:")
print(f"  Total Requests: {dashboard_metrics['total_requests']}")
print(f"  Total Tokens: {dashboard_metrics['total_tokens']}")
print(f"  Input Tokens: {dashboard_metrics['total_input_tokens']}")
print(f"  Output Tokens: {dashboard_metrics['total_output_tokens']}")
print(f"  Min Latency: {dashboard_metrics['min_latency']}")
print(f"  Max Latency: {dashboard_metrics['max_latency']}")
print(f"  Models Used: {dashboard_metrics['models_used']}")
print()

try:
    # Create dashboard
    fig1, fig2, fig3, fig4 = create_full_dashboard(dashboard_metrics)
    
    print("✅ Dashboard created successfully!")
    print(f"  Chart 1 (Quality & Errors): {len(fig1.data)} traces")
    print(f"  Chart 2 (Token Usage): {len(fig2.data)} traces")
    print(f"  Chart 3 (Latency): {len(fig3.data)} traces")
    print(f"  Chart 4 (Health Overview): {len(fig4.data)} traces")
    print()
    print("Dashboard is ready to display!")
    
except Exception as e:
    print(f"❌ Error creating dashboard: {e}")
    import traceback
    traceback.print_exc()

# Made with Bob
