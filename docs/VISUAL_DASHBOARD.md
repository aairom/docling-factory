# Visual Metrics Dashboard

## Overview

The Docling Factory application includes a visual metrics dashboard powered by Plotly that provides real-time insights into your LLM operations through OpenLLMetry observability.

## Features

The dashboard displays four columns of interactive charts:

### 1. Quality & Errors
- **Finish Reason Distribution**: Pie chart showing completion types (stop, length, error)
- **Error Breakdown**: Bar chart of error types and frequencies
- **Rate Limits**: Timeline of rate limit occurrences

### 2. Token Usage & Cost
- **Input vs Output Tokens**: Comparison of token consumption
- **Cost Over Time**: Timeline of cumulative costs
- **Token Throughput**: Tokens processed per minute

### 3. Latency
- **Latency Percentiles**: P50, P95, P99 response times
- **Time to First Token**: Distribution of initial response times
- **Latency by Model**: Performance comparison across models

### 4. Health Overview
- **Request Rate**: Requests per minute over time
- **Error Rate**: Error percentage timeline
- **Active Models**: Current model usage distribution

## Installation

The visual dashboard requires Plotly:

```bash
pip install plotly>=5.18.0
```

Or install all dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. **Start the Application**:
   ```bash
   python app_enhanced.py
   ```

2. **Navigate to OpenLLMetry Tab**:
   - Click on the "🔍 OpenLLMetry" tab
   - Select the "📊 Metrics" sub-tab

3. **View Dashboard**:
   - The dashboard displays automatically with 4 columns of charts
   - Click "🔄 Refresh Metrics" to update the visualizations

4. **Interact with Charts**:
   - Hover over data points for detailed information
   - Zoom in/out on specific time ranges
   - Pan across timelines
   - Click legend items to show/hide series

## Fallback Mode

If Plotly is not installed, the application will:
- Display a warning message with installation instructions
- Continue to work normally with text-based metrics
- Show a fallback message in the dashboard area

## Technical Details

### Chart Types
- **Pie Charts**: For categorical distributions (finish reasons, models)
- **Bar Charts**: For error breakdowns and comparisons
- **Line Charts**: For time-series data (costs, rates, latency)
- **Scatter Plots**: For latency distributions

### Data Sources
All metrics are collected via OpenLLMetry integration:
- OpenTelemetry spans for trace data
- Custom metrics collector for aggregations
- Real-time updates on refresh

### Performance
- Charts are generated on-demand (not auto-refreshing)
- Efficient data aggregation using pandas
- Responsive design adapts to screen size

## Troubleshooting

### Dashboard Not Showing
1. Verify Plotly is installed:
   ```bash
   pip list | grep plotly
   ```

2. Check application logs for import errors

3. Restart the application after installing Plotly

### Empty Charts
- Ensure RAG engine is initialized
- Perform some operations to generate metrics
- Click "🔄 Refresh Metrics" to update

### Performance Issues
- Large datasets may take time to render
- Consider resetting metrics periodically
- Use the "🗑️ Reset Metrics" button to clear old data

## Related Documentation

- [Getting Started Guide](GETTING_STARTED.md)
- [Comprehensive Guide](COMPREHENSIVE_GUIDE.md)
- [Troubleshooting](TROUBLESHOOTING.md)