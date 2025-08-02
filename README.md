# Fitbit Conversational AI Framework 🏃‍♂️

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green.svg)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-latest-orange.svg)](https://python.langchain.com/)

A proof-of-concept conversational AI assistant for Fitbit that provides personalized health insights using FastAPI and LangChain.

## 📋 Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Testing](#testing)

## ✨ Features
- Conversational AI interface for Fitbit data
- Real-time health insights and recommendations
- Interactive command-line and Jupyter notebook interfaces
- Built with FastAPI for high-performance API endpoints
- Powered by LangChain for advanced AI capabilities

## 🗂 Project Structure
```
fitbit_conversational_ai/
├── src/
│   └── fitbit_agent/         # Core application logic
│       ├── agent.py          # LangChain agent implementation
│       ├── service.py        # FastAPI service and endpoints
│       └── tools.py          # Agent tools and data store
├── notebooks/                # Interactive examples
│   └── fitbit_poc_notebook.ipynb
├── tests/                    # Unit tests
├── debug_client.py           # CLI debugging tool
├── run_server.py            # Production server runner
└── requirements.txt         # Project dependencies
```

## 🚀 Installation

1. **Clone the Repository**
   ```bash
   git clone <your_repository_url>
   cd fitbit_conversational_ai
   ```

2. **Set Up Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

1. **Environment Setup**
   ```bash
   cp .env.example .env
   ```

2. **Configure API Key**
   
   Open `.env` and add your Anthropic API key:
   ```env
   ANTHROPIC_API_KEY="sk-ant-api03-..."
   ```

## 💻 Usage

### Starting the Server

#### Development Mode
```bash
uvicorn src.fitbit_agent.service:app --reload
```

#### Production Mode
```bash
python run_server.py
```

The server will be available at `http://localhost:8000`

### Interacting with the Agent

#### Option 1: Jupyter Notebook (Recommended)
1. Start Jupyter Lab:
   ```bash
   jupyter lab
   ```
2. Navigate to `notebooks/fitbit_poc_notebook.ipynb`
3. Follow the interactive examples

#### Option 2: Command Line Interface
```bash
python debug_client.py
```

> 💡 **Pro Tip**: Monitor the Uvicorn server logs to see detailed agent thoughts and actions for debugging.

## 🧪 Testing

Run the test suite:
```bash
python -m unittest discover tests
```

