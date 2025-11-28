# 🌿 Plant Recognition with Q&A System

A comprehensive AI-powered system for identifying Vietnamese medicinal plants and answering questions about them. This project combines Computer Vision for image classification with RAG (Retrieval-Augmented Generation) and OG-RAG (Ontology-Grounded RAG) for accurate, context-aware question answering.

## 🏗️ System Architecture

This project is organized as a monorepo containing two main components:

- **[Frontend](./frontend)**: A modern web interface built with Next.js 15, TypeScript, and Tailwind CSS.
- **[Backend](./backend)**: A robust FastAPI server handling AI logic, vector database interactions (Supabase), and LLM integration.

## ✨ Key Features

The system operates through three distinct flows:

### 🌸 Flow 1: Plant Identification
- **Input**: Image (Upload or URL).
- **Output**: Top-5 plant predictions with confidence scores and brief summaries.
- **Tech**: Computer Vision classification model.

### 🖼️ Flow 2: Visual Q&A
- **Input**: Image + User Question.
- **Process**: First identifies the plant in the image, then uses that identity to retrieve specific knowledge for answering the question.
- **Tech**: CV Model + RAG/OG-RAG.

### 💬 Flow 3: Knowledge Chat
- **Input**: Text Question.
- **Process**: Pure RAG-based chat interface to query the system's comprehensive knowledge base of Vietnamese medicinal plants.
- **Tech**: Vector Search (Supabase pgvector) + LLM (Qwen via MegaLLM).

## 🚀 Getting Started

### 1. Clone the Repository

Since this project uses git submodules, clone it recursively:

```bash
git clone --recurse-submodules https://github.com/guzzle17/Plant-Recognition-with-Q-A-System.git
cd Plant-Recognition-with-Q-A-System
```

If you have already cloned it without submodules, run:

```bash
git submodule update --init --recursive
```

### 2. Setup Components

Please follow the detailed setup instructions in each directory:

- **Backend Setup**: Go to [backend/README.md](./backend/README.md) to set up the Python environment, environment variables, and database.
- **Frontend Setup**: Go to [frontend/README.md](./frontend/README.md) to install Node.js dependencies and start the web server.

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS v4
- **UI Components**: Radix UI, Lucide React
- **Tooling**: Biome, Turbopack

### Backend
- **Framework**: FastAPI
- **Database**: Supabase (PostgreSQL + pgvector)
- **AI/ML**:
  - **LLM**: MegaLLM API (Qwen/Qwen3)
  - **Embeddings**: Vietnamese-Embedding (1024-dim)
  - **Architecture**: OG-RAG (Ontology-Grounded RAG)

## 📄 License

This project is licensed under the MIT License.