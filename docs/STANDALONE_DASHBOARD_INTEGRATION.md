# Standalone Dashboard Integration

## Overview

The Visual Metrics Dashboard now includes an **"Open Standalone Dashboard"** button that launches the interactive charts in a separate browser window. This provides a workaround for Gradio rendering limitations while maintaining full functionality.

## Features

### 🎯 What It Does

When you click the "Open Standalone Dashboard" button:

1. **Collects Current Metrics** - Retrieves all metrics from the OpenLLMetry collector
2. **Transforms Data** - Processes metrics for visualization (latency percentiles, token counts, etc.)
3. **Generates Charts** - Creates 4 interactive Plotly charts in a 2x2 layout:
   - **Quality & Errors** (Pie chart) - Success vs error distribution
   - **Token Usage & Cost** (Bar chart) - Input vs output tokens
   - **Latency Percentiles** (Bar chart) - Min, P50, P95, P99, Max
   - **Health Overview** (Pie chart) - Model usage distribution
4. **Opens in Browser** - Launches the dashboard in your default web browser
5. **Provides Feedback** - Shows success message with metrics summary

### 📊 Dashboard Layout

```
┌─────────────────────────────────────────────────────────┐
│  OpenLLMetry Dashboard - X Requests                     │
├──────────────────────────┬──────────────────────────────┤
│  Quality & Errors        │  Token Usage & Cost          │
│  (Pie Chart)             │  (Bar Chart)                 │
│  • Success: XX%          │  • Input: XXX tokens         │
│  • Error: XX%            │  • Output: XXX tokens        │
├──────────────────────────┼──────────────────────────────┤
│  Latency Percentiles     │  Health Overview             │
│  (Bar Chart)             │  (Pie Chart)                 │
│  • Min, P50, P95, P99    │  • Model distribution        │
│  • Max latency           │  • Usage by model            │
└──────────────────────────┴──────────────────────────────┘
│  Metrics Summary: Requests, Tokens, Latency, Errors     │
└─────────────────────────────────────────────────────────┘
```

## Usage

### Step 1: Initialize RAG with Tracing

```python
# In the RAG Setup tab:
1. Select your LLM model (e.g., llama3.2:3b)
2. Select your embedding model (e.g., nomic-embed-text)
3. ✅ Enable "Enable OpenLLMetry Tracing"
4. Click "Initialize RAG Engine"
```

### Step 2: Generate Metrics

Perform operations to collect metrics:

**Option A: Parse and Index Documents**
```python
# In the Document Parser tab:
1. Upload PDF files
2. ✅ Enable "Index for RAG"
3. Click "Parse Document"
```

**Option B: Chat with Documents**
```python
# In the RAG Chat tab:
1. Enter a question
2. Click "Send"
3. Repeat for multiple queries
```

### Step 3: Open Standalone Dashboard

```python
# In the OpenLLMetry tab > Visual Dashboard sub-tab:
1. Click "🚀 Open Standalone Dashboard"
2. Dashboard opens in new browser window
3. View interactive charts with full metrics
```

## Technical Implementation

### Function: `open_standalone_dashboard()`

Located in `app_enhanced.py` (lines 692-806):

```python
def open_standalone_dashboard():
    """Open the standalone dashboard in a new browser window."""
    import subprocess
    import webbrowser
    import tempfile
    from plotly.subplots import make_subplots
    
    # 1. Validate RAG engine and metrics availability
    if not rag_engine or not hasattr(rag_engine, 'metrics_collector'):
        return "⚠️ RAG Engine not initialized"
    
    # 2. Get and transform metrics
    metrics = rag_engine.metrics_collector.get_metrics()
    dashboard_metrics = transform_metrics(metrics)
    
    # 3. Create 4 charts using metrics_dashboard.py
    fig1, fig2, fig3, fig4 = create_full_dashboard(dashboard_metrics)
    
    # 4. Combine into 2x2 subplot layout
    fig = make_subplots(rows=2, cols=2, ...)
    
    # 5. Save to temporary HTML file
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False)
    fig.write_html(temp_path, include_plotlyjs='cdn')
    
    # 6. Open in default browser
    webbrowser.open('file://' + temp_path)
    
    return "✅ Dashboard opened in new browser window!"
```

### Dependencies

```python
# Required imports (already in app_enhanced.py)
from metrics_dashboard import create_full_dashboard
from plotly.subplots import make_subplots
import webbrowser
import tempfile
```

### UI Integration

```python
# In Gradio UI (app_enhanced.py, lines 1000-1010)
with gr.Tab("📊 Visual Dashboard"):
    gr.Markdown("## 🎨 Interactive Metrics Dashboard")
    
    with gr.Row():
        refresh_visual_btn = gr.Button("🔄 Refresh Dashboard")
        open_standalone_btn = gr.Button("🚀 Open Standalone Dashboard")
        reset_metrics_btn = gr.Button("🗑️ Reset Metrics")
    
    dashboard_html = gr.HTML()
    reset_status = gr.Textbox(label="Status", visible=False)
    standalone_status = gr.Textbox(label="Standalone Status")
    
    # Event handlers
    refresh_visual_btn.click(fn=get_visual_dashboard_html, outputs=dashboard_html)
    open_standalone_btn.click(fn=open_standalone_dashboard, outputs=standalone_status)
    reset_metrics_btn.click(fn=reset_metrics, outputs=reset_status)
```

## Advantages

### ✅ Benefits

1. **Full Interactivity** - All Plotly features work (zoom, pan, hover, export)
2. **No Gradio Limitations** - Bypasses potential rendering issues
3. **Better Performance** - Native browser rendering is faster
4. **Larger View** - Full browser window for better visualization
5. **Independent Window** - Can keep dashboard open while using main app
6. **Easy Sharing** - HTML file can be saved and shared

### 🔄 Comparison with Embedded Dashboard

| Feature | Embedded (gr.HTML) | Standalone (Browser) |
|---------|-------------------|---------------------|
| Location | Inside Gradio tab | Separate browser window |
| Interactivity | Limited | Full Plotly features |
| Performance | May be slow | Fast native rendering |
| Size | Fixed in tab | Full browser window |
| Persistence | Refreshes with tab | Independent window |
| Sharing | Not easily | Save HTML file |

## Troubleshooting

### Issue: Button Does Nothing

**Symptoms:**
- Click "Open Standalone Dashboard" but nothing happens
- No browser window opens
- No error message

**Solutions:**

1. **Check RAG Initialization:**
   ```
   ⚠️ RAG Engine not initialized. Please initialize RAG first.
   ```
   → Go to RAG Setup tab and initialize RAG with tracing enabled

2. **Check Metrics Availability:**
   ```
   ⚠️ No metrics data available. Perform some operations first.
   ```
   → Parse documents or chat to generate metrics

3. **Check Browser Permissions:**
   - Ensure Python has permission to open browser
   - Check if popup blocker is preventing window

### Issue: Empty Charts in Standalone Dashboard

**Symptoms:**
- Dashboard opens but charts show "No data available"
- Metrics show 0 tokens despite operations

**Solutions:**

1. **Reset Metrics and Regenerate:**
   ```bash
   # Click "Reset Metrics" button
   # Perform new operations (parse/chat)
   # Open standalone dashboard again
   ```

2. **Check Token Capture:**
   ```bash
   # Run diagnostic script
   python3 debug_spans.py
   ```
   Should show token counts > 0

3. **Verify Ollama Attributes:**
   - Metrics collector checks multiple attribute patterns
   - Ollama uses `gen_ai.usage.input_tokens` / `output_tokens`
   - Standard uses `gen_ai.usage.prompt_tokens` / `completion_tokens`

### Issue: Browser Opens Wrong File

**Symptoms:**
- Old dashboard data appears
- Metrics don't match current state

**Solutions:**

1. **Clear Browser Cache:**
   ```
   Ctrl+Shift+Delete (Windows/Linux)
   Cmd+Shift+Delete (Mac)
   ```

2. **Force Refresh:**
   ```
   Ctrl+F5 (Windows/Linux)
   Cmd+Shift+R (Mac)
   ```

3. **Check Temp File:**
   - Dashboard saves to `/tmp/tmpXXXXXX.html`
   - Each click creates new file
   - Old files may accumulate

## Related Files

### Core Implementation
- `app_enhanced.py` - Main application with `open_standalone_dashboard()` function
- `metrics_dashboard.py` - Chart generation functions
- `metrics_collector.py` - OpenTelemetry span collection and metrics aggregation

### Documentation
- `docs/VISUAL_DASHBOARD_FIX_FINAL.md` - Complete dashboard fix documentation
- `DASHBOARD_SOLUTION.md` - Token attribute key mismatch explanation
- `docs/RAG_USAGE_GUIDE.md` - RAG setup and usage guide

### Diagnostic Tools
- `debug_spans.py` - Verify token capture is working
- `test_dashboard.py` - Test dashboard generation
- `standalone_dashboard.py` - Original standalone viewer (now integrated)

## Future Enhancements

### Potential Improvements

1. **Auto-Refresh** - Automatically update dashboard every N seconds
2. **Export Options** - Save dashboard as PNG, PDF, or static HTML
3. **Custom Layouts** - Allow users to choose chart arrangements
4. **More Metrics** - Add cost estimation, error details, trace timelines
5. **Comparison Mode** - Compare metrics across time periods
6. **Dark/Light Theme** - Toggle between themes
7. **Embedded Mode Fix** - Investigate and fix Gradio rendering issues

### Contributing

To enhance the standalone dashboard:

1. **Add New Charts** - Edit `metrics_dashboard.py`
2. **Modify Layout** - Update `open_standalone_dashboard()` subplot configuration
3. **Add Metrics** - Enhance `metrics_collector.py` to capture more data
4. **Improve UI** - Update button labels, add tooltips, improve feedback

## Conclusion

The standalone dashboard integration provides a robust solution for visualizing OpenLLMetry metrics when Gradio's embedded rendering has limitations. It maintains full interactivity, provides better performance, and offers a superior user experience for analyzing LLM observability data.

**Key Takeaway:** Click "🚀 Open Standalone Dashboard" to view your metrics in a full-featured, interactive browser window!

---

**Last Updated:** 2026-04-29  
**Version:** 1.0  
**Status:** ✅ Production Ready