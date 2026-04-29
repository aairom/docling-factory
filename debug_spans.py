#!/usr/bin/env python3
"""
Debug script to check what OpenTelemetry span attributes are being captured.
Run this after performing some operations in the app.
"""

import sys
sys.path.insert(0, '.')

from rag_engine import RAGEngine
import time

# Initialize RAG with tracing
print("Initializing RAG engine with tracing...")
rag = RAGEngine(
    opensearch_host="localhost",
    opensearch_port=9200,
    ollama_base_url="http://localhost:11434",
    embedding_model="granite-embedding:30m",
    llm_model="llama3.2:latest",
    enable_tracing=True
)

print("Waiting for initialization...")
time.sleep(2)

# Perform a simple operation
print("\nPerforming test operation...")
try:
    result = rag.chat("What is 2+2?", top_k=1, temperature=0.7)
    print(f"Chat result: {result['answer'][:100]}...")
except Exception as e:
    print(f"Error in chat: {e}")

print("\nWaiting for spans to be processed...")
time.sleep(2)

# Check metrics
if rag.metrics_collector:
    metrics = rag.metrics_collector.get_metrics()
    print("\n" + "="*60)
    print("METRICS SUMMARY")
    print("="*60)
    print(f"Total Requests: {metrics['total_requests']}")
    print(f"Total Tokens: {metrics['total_tokens']}")
    print(f"Input Tokens: {metrics['total_input_tokens']}")
    print(f"Output Tokens: {metrics['total_output_tokens']}")
    print(f"Models Used: {metrics['models_used']}")
    print(f"Operations: {metrics['operations']}")
    
    # Check recent spans
    spans = rag.metrics_collector.get_recent_spans(limit=5)
    print("\n" + "="*60)
    print("RECENT SPANS")
    print("="*60)
    for i, span in enumerate(spans, 1):
        print(f"\nSpan {i}: {span['name']}")
        print(f"  Duration: {span['duration_ms']:.2f}ms")
        print(f"  Status: {span['status']}")
        if span['attributes']:
            print(f"  Attributes ({len(span['attributes'])} keys):")
            for key in sorted(span['attributes'].keys()):
                value = span['attributes'][key]
                if isinstance(value, str) and len(value) > 50:
                    value = value[:50] + "..."
                print(f"    - {key}: {value}")
        if 'tokens' in span:
            print(f"  Tokens: {span['tokens']}")
        else:
            print(f"  Tokens: NOT CAPTURED")
else:
    print("ERROR: Metrics collector not available!")

# Made with Bob
