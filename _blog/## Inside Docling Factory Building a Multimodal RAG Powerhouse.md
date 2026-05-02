## ## Inside Docling Factory: Building a Multimodal RAG Powerhouse

**Posted on October 24, 2023 • By Your AI Engineer**

We’ve all been there: staring at a pile of messy PDFs, complex XBRL financial reports, and scattered CSVs, wondering how to turn that "dark data" into something an LLM can actually understand. Today, I’m pulling back the curtain on **Docling Factory**, a project I've been refining to solve exactly that.  

+1



It's more than just a parser; it's a full-stack document intelligence pipeline that bridges the gap between raw files and meaningful conversation.  

+1



------

### ### The Core Engine: Docling & Layout Awareness

At the heart of the system is the `DoclingParser`. Unlike traditional parsers that treat a page as a flat bag of words, this engine is **layout-aware**. It identifies headers, tables, and even those tricky images. Using the `docling` library, we can convert a complex PDF into clean Markdown while keeping the structure intact.  

+1



I've baked in support for **RapidOCR**, **EasyOCR**, and even **macOS Vision**. Whether you have a digital-native DOCX or a grainy scan of a 1990s invoice, the parser adapts. It even handles **XBRL** and **CSV** files natively, transforming structured data into LLM-friendly formats.  

+1



> **Why Multimodal Matters:** Documents aren't just text. They have charts, figures, and diagrams. Docling Factory detects `PictureItem` elements and extracts them as separate PNGs, or embeds them directly into the Markdown. This means your RAG system doesn't just "read"—it "sees."  

------

### ### The RAG Stack: Local Privacy meets Cloud Power

How do we chat with these documents? I built the `RAGEngine` to be as flexible as possible. It uses **OpenSearch** with k-NN (k-Nearest Neighbors) search for lightning-fast vector retrieval.  

+1



The real magic is the **Dual Backend Support**. You can run everything locally using **Ollama** (perfect for privacy-sensitive data) or flip a switch to **LiteLLM**. LiteLLM acts as a gateway to over 100 providers, letting you use GPT-4, Claude, or Gemini without changing a single line of business logic.  

+1



------

### ### Observability: Seeing the Unseen

"Black box" AI is a no-go for production. That’s why I integrated **OpenLLMetry**. Through our `MetricsCollector`, we track everything: P95 latency, token usage, and even cost estimation. If a model starts acting up or a prompt is getting too expensive, you’ll see it on the Plotly-powered dashboard before it becomes a problem.  

+2



------

### ### Final Thoughts

Docling Factory represents a shift from "simple RAG" to "Production Document AI." By combining containerized services like **PostgreSQL**, **OpenSearch**, and **Gradio**, we’ve created a workspace that is both powerful for developers and intuitive for users.  

+1



Check out the full architecture in the README, and let's get those documents talking!