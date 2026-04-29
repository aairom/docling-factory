#!/usr/bin/env python3
"""
Standalone Visual Metrics Dashboard
Opens a browser window with Plotly charts showing current metrics.
"""

import sys
sys.path.insert(0, '.')

from metrics_dashboard import create_full_dashboard
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import webbrowser
import tempfile
import os

def create_standalone_dashboard():
    """Create a standalone HTML dashboard with all charts."""
    
    # Try to get metrics from running app
    try:
        from rag_engine import RAGEngine
        from metrics_collector import get_metrics_collector
        
        collector = get_metrics_collector()
        if collector:
            metrics = collector.get_metrics()
            print(f"✅ Found metrics collector with {metrics['total_requests']} requests")
        else:
            print("⚠️ No metrics collector found, using sample data")
            metrics = get_sample_metrics()
    except Exception as e:
        print(f"⚠️ Could not access metrics collector: {e}")
        print("Using sample data instead")
        metrics = get_sample_metrics()
    
    # Transform metrics for dashboard
    dashboard_metrics = dict(metrics)
    latency_stats = metrics.get('latency_stats', {})
    
    # Calculate overall latency percentiles
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
    
    # Create the 4 charts
    fig1, fig2, fig3, fig4 = create_full_dashboard(dashboard_metrics)
    
    # Create a 2x2 subplot layout
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Quality & Errors", "Token Usage & Cost", 
                       "Latency Percentiles", "Health Overview"),
        specs=[[{"type": "pie"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "pie"}]],
        vertical_spacing=0.15,
        horizontal_spacing=0.1
    )
    
    # Add traces from each figure
    for trace in fig1.data:
        fig.add_trace(trace, row=1, col=1)
    
    for trace in fig2.data:
        fig.add_trace(trace, row=1, col=2)
    
    for trace in fig3.data:
        fig.add_trace(trace, row=2, col=1)
    
    for trace in fig4.data:
        fig.add_trace(trace, row=2, col=2)
    
    # Update layout
    fig.update_layout(
        title_text=f"OpenLLMetry Visual Dashboard - {metrics['total_requests']} Requests",
        showlegend=True,
        height=800,
        template="plotly_dark"
    )
    
    # Add metrics summary as annotation
    summary = f"""
    <b>Metrics Summary:</b><br>
    Total Requests: {metrics['total_requests']}<br>
    Total Tokens: {metrics['total_tokens']:,}<br>
    Input Tokens: {metrics.get('total_input_tokens', 0):,}<br>
    Output Tokens: {metrics.get('total_output_tokens', 0):,}<br>
    Avg Latency: {metrics['avg_latency_ms']:.2f}ms<br>
    Error Rate: {metrics['error_rate']:.2f}%<br>
    Models: {len(metrics.get('models_used', {}))}
    """
    
    fig.add_annotation(
        text=summary,
        xref="paper", yref="paper",
        x=0.5, y=-0.1,
        showarrow=False,
        font=dict(size=12),
        align="left",
        bgcolor="rgba(0,0,0,0.5)",
        bordercolor="white",
        borderwidth=1
    )
    
    return fig, metrics


def get_sample_metrics():
    """Get sample metrics for testing."""
    return {
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


if __name__ == "__main__":
    print("="*60)
    print("OpenLLMetry Standalone Dashboard")
    print("="*60)
    print()
    
    # Create dashboard
    fig, metrics = create_standalone_dashboard()
    
    # Save to temporary HTML file
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False)
    temp_path = temp_file.name
    temp_file.close()
    
    fig.write_html(temp_path, include_plotlyjs='cdn')
    
    print(f"✅ Dashboard created successfully!")
    print(f"📊 Metrics: {metrics['total_requests']} requests, {metrics['total_tokens']} tokens")
    print(f"📁 Saved to: {temp_path}")
    print(f"🌐 Opening in browser...")
    print()
    
    # Open in browser
    webbrowser.open('file://' + os.path.abspath(temp_path))
    
    print("✨ Dashboard opened in your default browser!")
    print("   Press Ctrl+C to exit (the HTML file will remain)")
    print()
    
    try:
        input("Press Enter to close and delete the temporary file...")
        os.unlink(temp_path)
        print("🗑️  Temporary file deleted")
    except KeyboardInterrupt:
        print("\n🗑️  Temporary file deleted")
        os.unlink(temp_path)

# Made with Bob
