# metrics_dashboard.py
"""
Visual Metrics Dashboard for OpenLLMetry
Creates interactive charts and visualizations for LLM observability metrics.
"""

import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


def create_quality_errors_chart(metrics: Dict) -> go.Figure:
    """Create Quality & Errors chart - Finish Reason Distribution."""
    fig = go.Figure()
    
    # Finish Reason Distribution
    total_requests = metrics.get('total_requests', 0)
    error_count = metrics.get('error_count', 0)
    success_count = total_requests - error_count
    
    if total_requests > 0:
        fig.add_trace(go.Pie(
            labels=['Success', 'Error'],
            values=[success_count, error_count],
            marker=dict(colors=['#2ecc71', '#e74c3c']),
            hole=0.3
        ))
        
        fig.update_layout(
            title="Finish Reason Distribution",
            height=400,
            showlegend=True
        )
    else:
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    return fig


def create_token_cost_chart(metrics: Dict) -> go.Figure:
    """Create Token Usage & Cost chart."""
    fig = go.Figure()
    
    total_input = metrics.get('total_input_tokens', 0)
    total_output = metrics.get('total_output_tokens', 0)
    
    if total_input > 0 or total_output > 0:
        fig.add_trace(go.Bar(
            x=['Input Tokens', 'Output Tokens'],
            y=[total_input, total_output],
            marker_color=['#3498db', '#9b59b6'],
            text=[f'{total_input:,}', f'{total_output:,}'],
            textposition='auto'
        ))
        
        fig.update_layout(
            title="Token Usage",
            yaxis_title="Tokens",
            height=400,
            showlegend=False
        )
    else:
        fig.add_annotation(
            text="No token data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    return fig


def create_latency_chart(metrics: Dict) -> go.Figure:
    """Create Latency chart - Percentiles."""
    fig = go.Figure()
    
    latencies = {
        'Min': metrics.get('min_latency', 0),
        'P50': metrics.get('p50_latency', 0),
        'P95': metrics.get('p95_latency', 0),
        'P99': metrics.get('p99_latency', 0),
        'Max': metrics.get('max_latency', 0)
    }
    
    if any(v > 0 for v in latencies.values()):
        fig.add_trace(go.Bar(
            x=list(latencies.keys()),
            y=list(latencies.values()),
            marker_color='#e67e22',
            text=[f'{v:.2f}ms' for v in latencies.values()],
            textposition='auto'
        ))
        
        fig.update_layout(
            title="Latency Percentiles",
            yaxis_title="Latency (ms)",
            height=400,
            showlegend=False
        )
    else:
        fig.add_annotation(
            text="No latency data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    return fig


def create_health_overview_chart(metrics: Dict) -> go.Figure:
    """Create Health Overview chart - Model Usage."""
    fig = go.Figure()
    
    models_used = metrics.get('models_used', {})
    
    if models_used:
        fig.add_trace(go.Pie(
            labels=list(models_used.keys()),
            values=list(models_used.values()),
            hole=0.3
        ))
        
        fig.update_layout(
            title="Model Usage Distribution",
            height=400,
            showlegend=True
        )
    else:
        fig.add_annotation(
            text="No model usage data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    return fig


def create_full_dashboard(metrics: Dict) -> Tuple[go.Figure, go.Figure, go.Figure, go.Figure]:
    """
    Create all dashboard charts.
    
    Args:
        metrics: Metrics dictionary from MetricsCollector
        
    Returns:
        Tuple of 4 Plotly figures (Quality, Tokens, Latency, Health)
    """
    try:
        logger.info(f"Creating dashboard with metrics: total_requests={metrics.get('total_requests', 0)}")
        
        quality_fig = create_quality_errors_chart(metrics)
        token_fig = create_token_cost_chart(metrics)
        latency_fig = create_latency_chart(metrics)
        health_fig = create_health_overview_chart(metrics)
        
        return (quality_fig, token_fig, latency_fig, health_fig)
        
    except Exception as e:
        logger.error(f"Error creating dashboard: {e}", exc_info=True)
        # Return empty figures on error
        empty_fig = go.Figure()
        empty_fig.add_annotation(
            text=f"Error creating chart: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return (empty_fig, empty_fig, empty_fig, empty_fig)


def get_empty_dashboard_message() -> str:
    """Return message for when metrics are not available."""
    return """
## 🔍 Visual Metrics Dashboard

⚠️ **No Metrics Available**

To see the visual dashboard:

1. **Initialize RAG Engine** with tracing enabled
2. **Perform some operations**:
   - Parse and index documents
   - Ask questions in chat
3. **Refresh this page** to see charts

### What You'll See

Once metrics are collected, this dashboard will display:

**Quality & Errors:**
- Finish reason distribution (success vs errors)

**Token Usage & Cost:**
- Input vs output tokens comparison

**Latency:**
- Latency percentiles (Min, P50, P95, P99, Max)

**Health Overview:**
- Model usage distribution
"""

# Made with Bob
