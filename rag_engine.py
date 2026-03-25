"""
RAG Engine Module
Implements Retrieval-Augmented Generation using OpenSearch and Ollama.
Supports document indexing, semantic search, and chat with documents.
"""

import os
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import json
from datetime import datetime

# OpenSearch
from opensearchpy import OpenSearch, helpers
from opensearchpy.exceptions import NotFoundError

# Ollama
import ollama

# LangChain for RAG orchestration
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# OpenLLMetry for observability
from traceloop.sdk import Traceloop
from traceloop.sdk.decorators import workflow, task

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OllamaEmbeddings:
    """Ollama embeddings wrapper."""
    
    def __init__(self, model: str = "granite-embedding:30m", base_url: str = "http://localhost:11434"):
        """
        Initialize Ollama embeddings.
        
        Args:
            model: Ollama embedding model name
            base_url: Ollama server URL
        """
        self.model = model
        self.base_url = base_url
        self.client = ollama.Client(host=base_url)
        logger.info(f"Initialized Ollama embeddings with model: {model}")
    
    @task(name="generate_embedding")
    def embed_query(self, text: str) -> List[float]:
        """Generate embedding for a query text."""
        try:
            response = self.client.embeddings(model=self.model, prompt=text)
            return response['embedding']
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
    
    @task(name="generate_embeddings_batch")
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple documents."""
        embeddings = []
        for text in texts:
            embeddings.append(self.embed_query(text))
        return embeddings


class OllamaLLM:
    """Ollama LLM wrapper for chat."""
    
    def __init__(self, model: str = "llama3.2:latest", base_url: str = "http://localhost:11434"):
        """
        Initialize Ollama LLM.
        
        Args:
            model: Ollama model name
            base_url: Ollama server URL
        """
        self.model = model
        self.base_url = base_url
        self.client = ollama.Client(host=base_url)
        logger.info(f"Initialized Ollama LLM with model: {model}")
    
    @task(name="llm_generate")
    def generate(self, prompt: str, context: str = "", temperature: float = 0.7) -> str:
        """
        Generate response using Ollama.
        
        Args:
            prompt: User query
            context: Retrieved context from documents
            temperature: Generation temperature
            
        Returns:
            Generated response
        """
        try:
            full_prompt = f"""Context information:
{context}

Question: {prompt}

Please answer the question based on the context provided above. If the context doesn't contain relevant information, say so."""

            response = self.client.generate(
                model=self.model,
                prompt=full_prompt,
                options={"temperature": temperature}
            )
            return response['response']
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise
    
    @task(name="llm_chat")
    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """
        Chat with Ollama using message history.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Generation temperature
            
        Returns:
            Generated response
        """
        try:
            response = self.client.chat(
                model=self.model,
                messages=messages,
                options={"temperature": temperature}
            )
            return response['message']['content']
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            raise


class RAGEngine:
    """
    RAG Engine using OpenSearch for vector storage and Ollama for LLM/embeddings.
    """
    
    def __init__(
        self,
        opensearch_host: str = "localhost",
        opensearch_port: int = 9200,
        opensearch_user: str = "admin",
        opensearch_password: str = "admin",
        ollama_base_url: str = "http://localhost:11434",
        embedding_model: str = "granite-embedding:30m",
        llm_model: str = "llama3.2:latest",
        index_name: str = "docling_documents",
        enable_tracing: bool = True
    ):
        """
        Initialize RAG Engine.
        
        Args:
            opensearch_host: OpenSearch host
            opensearch_port: OpenSearch port
            opensearch_user: OpenSearch username
            opensearch_password: OpenSearch password
            ollama_base_url: Ollama server URL
            embedding_model: Ollama embedding model
            llm_model: Ollama LLM model
            index_name: OpenSearch index name
            enable_tracing: Enable OpenLLMetry tracing
        """
        # Initialize OpenLLMetry tracing
        if enable_tracing:
            Traceloop.init(app_name="docling-rag", disable_batch=True)
            logger.info("OpenLLMetry tracing enabled")
        
        # Initialize OpenSearch client
        self.opensearch_client = OpenSearch(
            hosts=[{'host': opensearch_host, 'port': opensearch_port}],
            http_auth=(opensearch_user, opensearch_password),
            use_ssl=False,
            verify_certs=False,
            ssl_show_warn=False
        )
        
        self.index_name = index_name
        
        # Initialize Ollama components
        self.embeddings = OllamaEmbeddings(model=embedding_model, base_url=ollama_base_url)
        self.llm = OllamaLLM(model=llm_model, base_url=ollama_base_url)
        
        # Text splitter for chunking
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        # Create index if it doesn't exist
        self._create_index_if_not_exists()
        
        logger.info(f"RAG Engine initialized with index: {index_name}")
    
    def _create_index_if_not_exists(self):
        """Create OpenSearch index with vector field if it doesn't exist."""
        if not self.opensearch_client.indices.exists(index=self.index_name):
            index_body = {
                "settings": {
                    "index": {
                        "knn": True,
                        "knn.algo_param.ef_search": 100
                    }
                },
                "mappings": {
                    "properties": {
                        "content": {"type": "text"},
                        "embedding": {
                            "type": "knn_vector",
                            "dimension": 384,  # granite-embedding:30m dimension
                            "method": {
                                "name": "hnsw",
                                "space_type": "cosinesimil",
                                "engine": "lucene"  # Changed from nmslib to lucene for OpenSearch 3.0+
                            }
                        },
                        "metadata": {"type": "object"},
                        "source": {"type": "keyword"},
                        "timestamp": {"type": "date"}
                    }
                }
            }
            
            self.opensearch_client.indices.create(index=self.index_name, body=index_body)
            logger.info(f"Created index: {self.index_name}")
    
    @workflow(name="index_document")
    def index_document(self, file_path: str, content: str, metadata: Optional[Dict] = None) -> Dict:
        """
        Index a document into OpenSearch.
        
        Args:
            file_path: Path to the source document
            content: Document content
            metadata: Additional metadata
            
        Returns:
            Indexing result
        """
        try:
            # Split content into chunks
            chunks = self.text_splitter.split_text(content)
            logger.info(f"Split document into {len(chunks)} chunks")
            
            # Generate embeddings for chunks
            embeddings = self.embeddings.embed_documents(chunks)
            
            # Prepare documents for bulk indexing
            actions = []
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                doc = {
                    "_index": self.index_name,
                    "_source": {
                        "content": chunk,
                        "embedding": embedding,
                        "source": file_path,
                        "chunk_id": i,
                        "metadata": metadata or {},
                        "timestamp": datetime.utcnow().isoformat()
                    }
                }
                actions.append(doc)
            
            # Bulk index
            success, failed = helpers.bulk(self.opensearch_client, actions, raise_on_error=False)
            
            logger.info(f"Indexed {success} chunks from {file_path}")
            
            return {
                "status": "success",
                "file_path": file_path,
                "chunks_indexed": success,
                "chunks_failed": len(failed) if failed else 0
            }
            
        except Exception as e:
            logger.error(f"Error indexing document: {e}")
            return {
                "status": "error",
                "file_path": file_path,
                "error": str(e)
            }
    
    @workflow(name="search_documents")
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search for relevant documents using semantic search.
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of relevant document chunks
        """
        try:
            # Generate query embedding
            query_embedding = self.embeddings.embed_query(query)
            
            # KNN search
            search_body = {
                "size": top_k,
                "query": {
                    "knn": {
                        "embedding": {
                            "vector": query_embedding,
                            "k": top_k
                        }
                    }
                }
            }
            
            response = self.opensearch_client.search(
                index=self.index_name,
                body=search_body
            )
            
            results = []
            for hit in response['hits']['hits']:
                results.append({
                    "content": hit['_source']['content'],
                    "source": hit['_source']['source'],
                    "score": hit['_score'],
                    "metadata": hit['_source'].get('metadata', {})
                })
            
            logger.info(f"Found {len(results)} relevant chunks for query")
            return results
            
        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            return []
    
    @workflow(name="chat_with_documents")
    def chat(self, query: str, top_k: int = 5, temperature: float = 0.7) -> Dict:
        """
        Chat with documents using RAG.
        
        Args:
            query: User question
            top_k: Number of context chunks to retrieve
            temperature: LLM temperature
            
        Returns:
            Response with answer and sources
        """
        try:
            # Retrieve relevant context
            search_results = self.search(query, top_k=top_k)
            
            if not search_results:
                return {
                    "answer": "I couldn't find any relevant information in the indexed documents.",
                    "sources": [],
                    "context_used": False
                }
            
            # Build context from search results
            context = "\n\n".join([
                f"[Source: {r['source']}]\n{r['content']}"
                for r in search_results
            ])
            
            # Generate response
            answer = self.llm.generate(query, context=context, temperature=temperature)
            
            # Extract unique sources
            sources = list(set([r['source'] for r in search_results]))
            
            return {
                "answer": answer,
                "sources": sources,
                "context_used": True,
                "num_chunks": len(search_results)
            }
            
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return {
                "answer": f"Error: {str(e)}",
                "sources": [],
                "context_used": False
            }
    
    def list_indexed_documents(self) -> List[str]:
        """List all indexed document sources."""
        try:
            search_body = {
                "size": 0,
                "aggs": {
                    "unique_sources": {
                        "terms": {
                            "field": "source",
                            "size": 1000
                        }
                    }
                }
            }
            
            response = self.opensearch_client.search(
                index=self.index_name,
                body=search_body
            )
            
            sources = [
                bucket['key']
                for bucket in response['aggregations']['unique_sources']['buckets']
            ]
            
            return sources
            
        except Exception as e:
            logger.error(f"Error listing documents: {e}")
            return []
    
    def delete_document(self, file_path: str) -> Dict:
        """Delete all chunks of a document from the index."""
        try:
            delete_query = {
                "query": {
                    "term": {
                        "source": file_path
                    }
                }
            }
            
            response = self.opensearch_client.delete_by_query(
                index=self.index_name,
                body=delete_query
            )
            
            deleted = response.get('deleted', 0)
            logger.info(f"Deleted {deleted} chunks from {file_path}")
            
            return {
                "status": "success",
                "deleted_chunks": deleted
            }
            
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def get_stats(self) -> Dict:
        """Get index statistics."""
        try:
            stats = self.opensearch_client.indices.stats(index=self.index_name)
            count_response = self.opensearch_client.count(index=self.index_name)
            
            return {
                "total_chunks": count_response['count'],
                "index_size": stats['indices'][self.index_name]['total']['store']['size_in_bytes'],
                "unique_documents": len(self.list_indexed_documents())
            }
            
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {}
    
    def health_check(self) -> Dict:
        """Check health of OpenSearch and Ollama."""
        health = {
            "opensearch": False,
            "ollama": False,
            "embedding_model": False,
            "llm_model": False
        }
        
        # Check OpenSearch
        try:
            self.opensearch_client.cluster.health()
            health["opensearch"] = True
        except Exception as e:
            logger.error(f"OpenSearch health check failed: {e}")
        
        # Check Ollama and models
        try:
            models = ollama.list()
            model_names = [m['name'] for m in models.get('models', [])]
            
            health["ollama"] = True
            health["embedding_model"] = self.embeddings.model in model_names
            health["llm_model"] = self.llm.model in model_names
            
        except Exception as e:
            logger.error(f"Ollama health check failed: {e}")
        
        return health


# Made with Bob