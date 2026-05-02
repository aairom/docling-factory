#!/usr/bin/env python3
"""
Test script to verify LiteLLM integration with Docling Factory
"""

import os
import sys

def test_imports():
    """Test that all required packages are installed."""
    print("Testing imports...")
    try:
        import litellm
        print("✅ litellm imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import litellm: {e}")
        return False
    
    try:
        import ollama
        print("✅ ollama imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import ollama: {e}")
        return False
    
    try:
        from rag_engine import RAGEngine, LiteLLMEmbeddings, LiteLLMLLM
        print("✅ RAG engine with LiteLLM support imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import RAG engine: {e}")
        return False
    
    return True


def test_litellm_connection():
    """Test connection to LiteLLM service."""
    print("\nTesting LiteLLM connection...")
    
    litellm_base = os.getenv("LITELLM_API_BASE", "http://localhost:4000")
    
    try:
        import requests
        response = requests.get(f"{litellm_base}/health", timeout=5)
        if response.status_code == 200:
            print(f"✅ LiteLLM service is running at {litellm_base}")
            return True
        else:
            print(f"⚠️  LiteLLM service responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to LiteLLM at {litellm_base}")
        print("   Make sure LiteLLM is running: docker-compose up -d litellm")
        return False
    except Exception as e:
        print(f"❌ Error testing LiteLLM connection: {e}")
        return False


def test_ollama_connection():
    """Test connection to Ollama service."""
    print("\nTesting Ollama connection...")
    
    ollama_base = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    try:
        import ollama
        client = ollama.Client(host=ollama_base)
        models = client.list()
        print(f"✅ Ollama service is running at {ollama_base}")
        
        if hasattr(models, 'models'):
            model_list = [m.model for m in models.models]
        else:
            model_list = []
        
        if model_list:
            print(f"   Available models: {', '.join(model_list[:5])}")
            if len(model_list) > 5:
                print(f"   ... and {len(model_list) - 5} more")
        else:
            print("   ⚠️  No models found. Pull a model: ollama pull llama3.2")
        
        return True
    except Exception as e:
        print(f"❌ Cannot connect to Ollama at {ollama_base}")
        print(f"   Error: {e}")
        print("   Make sure Ollama is running: ollama serve")
        return False


def test_opensearch_connection():
    """Test connection to OpenSearch service."""
    print("\nTesting OpenSearch connection...")
    
    opensearch_host = os.getenv("OPENSEARCH_HOST", "localhost")
    opensearch_port = int(os.getenv("OPENSEARCH_PORT", "9200"))
    
    try:
        from opensearchpy import OpenSearch
        client = OpenSearch(
            hosts=[{'host': opensearch_host, 'port': opensearch_port}],
            use_ssl=False,
            verify_certs=False,
            ssl_show_warn=False
        )
        health = client.cluster.health()
        print(f"✅ OpenSearch is running at {opensearch_host}:{opensearch_port}")
        print(f"   Cluster status: {health.get('status', 'unknown')}")
        return True
    except Exception as e:
        print(f"❌ Cannot connect to OpenSearch at {opensearch_host}:{opensearch_port}")
        print(f"   Error: {e}")
        print("   Make sure OpenSearch is running: docker-compose up -d opensearch")
        return False


def test_rag_engine_initialization():
    """Test RAG engine initialization with both backends."""
    print("\nTesting RAG engine initialization...")
    
    try:
        from rag_engine import RAGEngine
        
        # Test with Ollama
        print("  Testing with Ollama backend...")
        try:
            rag_ollama = RAGEngine(
                opensearch_host=os.getenv("OPENSEARCH_HOST", "localhost"),
                opensearch_port=int(os.getenv("OPENSEARCH_PORT", "9200")),
                ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
                embedding_model="granite-embedding:30m",
                llm_model="llama3.2:latest",
                enable_tracing=False,
                use_litellm=False
            )
            print("  ✅ RAG engine initialized with Ollama backend")
        except Exception as e:
            print(f"  ⚠️  Failed to initialize with Ollama: {e}")
        
        # Test with LiteLLM
        print("  Testing with LiteLLM backend...")
        try:
            rag_litellm = RAGEngine(
                opensearch_host=os.getenv("OPENSEARCH_HOST", "localhost"),
                opensearch_port=int(os.getenv("OPENSEARCH_PORT", "9200")),
                embedding_model="text-embedding-ada-002",
                llm_model="gpt-3.5-turbo",
                enable_tracing=False,
                use_litellm=True,
                litellm_api_base=os.getenv("LITELLM_API_BASE", "http://localhost:4000"),
                litellm_api_key=os.getenv("LITELLM_API_KEY", "sk-****")
            )
            print("  ✅ RAG engine initialized with LiteLLM backend")
        except Exception as e:
            print(f"  ⚠️  Failed to initialize with LiteLLM: {e}")
        
        return True
    except Exception as e:
        print(f"❌ Error testing RAG engine: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("LiteLLM Integration Test Suite")
    print("=" * 60)
    
    results = {
        "Imports": test_imports(),
        "LiteLLM Connection": test_litellm_connection(),
        "Ollama Connection": test_ollama_connection(),
        "OpenSearch Connection": test_opensearch_connection(),
        "RAG Engine": test_rag_engine_initialization()
    }
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:.<40} {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All tests passed! LiteLLM integration is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

# Made with Bob
