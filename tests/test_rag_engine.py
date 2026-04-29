# test_rag_engine.py
"""
Unit tests for rag_engine.py module
"""

import unittest
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestRAGEngine(unittest.TestCase):
    """Test cases for RAGEngine class"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    @patch('rag_engine.OpenSearch')
    @patch('rag_engine.ollama')
    def test_initialization(self, mock_ollama, mock_opensearch):
        """Test RAG engine initialization"""
        from rag_engine import RAGEngine
        
        rag = RAGEngine(
            opensearch_host="localhost",
            opensearch_port=9200,
            embedding_model="test-embedding",
            llm_model="test-llm",
            enable_tracing=False
        )
        
        self.assertIsNotNone(rag)
        self.assertEqual(rag.embedding_model, "test-embedding")
        self.assertEqual(rag.llm_model, "test-llm")

    @patch('rag_engine.OpenSearch')
    @patch('rag_engine.ollama')
    def test_health_check(self, mock_ollama, mock_opensearch):
        """Test health check functionality"""
        from rag_engine import RAGEngine
        
        # Mock OpenSearch client
        mock_client = MagicMock()
        mock_client.ping.return_value = True
        mock_opensearch.return_value = mock_client
        
        # Mock Ollama client
        mock_ollama_client = MagicMock()
        mock_response = MagicMock()
        mock_response.models = []
        mock_ollama_client.list.return_value = mock_response
        mock_ollama.Client.return_value = mock_ollama_client
        
        rag = RAGEngine(enable_tracing=False)
        health = rag.health_check()
        
        self.assertIsInstance(health, dict)
        self.assertIn('opensearch', health)

    @patch('rag_engine.OpenSearch')
    @patch('rag_engine.ollama')
    def test_index_document(self, mock_ollama, mock_opensearch):
        """Test document indexing"""
        from rag_engine import RAGEngine
        
        # Mock OpenSearch
        mock_client = MagicMock()
        mock_client.indices.exists.return_value = True
        mock_opensearch.return_value = mock_client
        
        # Mock Ollama embeddings
        mock_ollama.embeddings.return_value = {
            'embedding': [0.1] * 384
        }
        
        rag = RAGEngine(enable_tracing=False)
        
        result = rag.index_document(
            file_path="test.pdf",
            content="Test content for indexing",
            metadata={"source": "test"}
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn('chunks_indexed', result)

    @patch('rag_engine.OpenSearch')
    @patch('rag_engine.ollama')
    def test_search(self, mock_ollama, mock_opensearch):
        """Test semantic search"""
        from rag_engine import RAGEngine
        
        # Mock OpenSearch search response
        mock_client = MagicMock()
        mock_client.search.return_value = {
            'hits': {
                'hits': [
                    {
                        '_source': {
                            'content': 'Test result',
                            'file_path': 'test.pdf'
                        },
                        '_score': 0.9
                    }
                ]
            }
        }
        mock_opensearch.return_value = mock_client
        
        # Mock Ollama embeddings
        mock_ollama.embeddings.return_value = {
            'embedding': [0.1] * 384
        }
        
        rag = RAGEngine(enable_tracing=False)
        results = rag.search("test query", top_k=5)
        
        self.assertIsInstance(results, list)

    @patch('rag_engine.OpenSearch')
    @patch('rag_engine.ollama')
    def test_get_stats(self, mock_ollama, mock_opensearch):
        """Test getting index statistics"""
        from rag_engine import RAGEngine
        
        # Mock OpenSearch stats
        mock_client = MagicMock()
        mock_client.count.return_value = {'count': 100}
        mock_client.indices.stats.return_value = {
            'indices': {
                'documents': {
                    'primaries': {
                        'store': {'size_in_bytes': 1024000}
                    }
                }
            }
        }
        mock_opensearch.return_value = mock_client
        
        rag = RAGEngine(enable_tracing=False)
        stats = rag.get_stats()
        
        self.assertIsInstance(stats, dict)
        self.assertIn('total_chunks', stats)


class TestOllamaEmbeddings(unittest.TestCase):
    """Test cases for OllamaEmbeddings class"""

    @patch('rag_engine.ollama')
    def test_embed_documents(self, mock_ollama):
        """Test embedding multiple documents"""
        from rag_engine import OllamaEmbeddings
        
        mock_ollama.embeddings.return_value = {
            'embedding': [0.1] * 384
        }
        
        embedder = OllamaEmbeddings(model="test-model")
        texts = ["text1", "text2", "text3"]
        embeddings = embedder.embed_documents(texts)
        
        self.assertIsInstance(embeddings, list)
        self.assertEqual(len(embeddings), 3)

    @patch('rag_engine.ollama')
    def test_embed_query(self, mock_ollama):
        """Test embedding a single query"""
        from rag_engine import OllamaEmbeddings
        
        mock_ollama.embeddings.return_value = {
            'embedding': [0.1] * 384
        }
        
        embedder = OllamaEmbeddings(model="test-model")
        embedding = embedder.embed_query("test query")
        
        self.assertIsInstance(embedding, list)
        self.assertEqual(len(embedding), 384)


class TestOllamaLLM(unittest.TestCase):
    """Test cases for OllamaLLM class"""

    @patch('rag_engine.ollama')
    def test_generate(self, mock_ollama):
        """Test LLM text generation"""
        from rag_engine import OllamaLLM
        
        mock_ollama.generate.return_value = {
            'response': 'Generated response'
        }
        
        llm = OllamaLLM(model="test-model")
        response = llm.generate("test prompt")
        
        self.assertIsInstance(response, str)
        self.assertEqual(response, 'Generated response')

    @patch('rag_engine.ollama')
    def test_generate_with_temperature(self, mock_ollama):
        """Test LLM generation with temperature parameter"""
        from rag_engine import OllamaLLM
        
        mock_ollama.generate.return_value = {
            'response': 'Generated response'
        }
        
        llm = OllamaLLM(model="test-model", temperature=0.7)
        response = llm.generate("test prompt")
        
        self.assertIsInstance(response, str)


if __name__ == '__main__':
    unittest.main()

# Made with Bob
