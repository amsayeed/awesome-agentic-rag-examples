# 🤖 LlamaIndex Advanced Agentic RAG Demo

Welcome to the most fun way to learn about Agentic RAG systems! This demo combines the power of LlamaIndex, intelligent agents, and RAG (Retrieval-Augmented Generation) into an interactive experience.

## 🌟 What You'll Learn

- How to build an AI agent that can reason and use tools
- Implementing RAG for accurate, grounded responses
- Creating custom tools for your agents
- Building interactive AI applications with Streamlit
- Advanced techniques like memory management and tool chaining

## 🎯 Features

Our demo agent can:
- 🔍 **Search Knowledge**: Query an AI knowledge base about agents, RAG, and more
- 🧮 **Calculate**: Perform mathematical operations
- 😄 **Tell Jokes**: Lighten the mood with AI and programming jokes
- 📝 **Summarize**: Create concise summaries of complex topics
- 💾 **Remember**: Maintain conversation context with built-in memory

## 🚀 Quick Start

### 1. Clone and Navigate
```bash
cd llamaindex-rag
```

### 2. Set Up Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Key
```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your_actual_api_key_here
```

### 4. Run the Demo

**Option A: Command Line Interface**
```bash
python agentic_rag_demo.py
```

**Option B: Streamlit Web App** (Recommended!)
```bash
streamlit run streamlit_app.py
```

## 📚 Understanding the Code

### Core Components

1. **AgenticRAGSystem** (`agentic_rag_demo.py`)
   - The brain of our operation
   - Manages knowledge base, tools, and agent creation

2. **Knowledge Base**
   - Pre-loaded with fun documents about AI, agents, and RAG
   - Stored as vector embeddings for semantic search

3. **ReAct Agent**
   - Uses reasoning + acting pattern
   - Decides which tools to use based on the query

4. **Custom Tools**
   - Calculator: For math operations
   - Joke Teller: For entertainment
   - Knowledge Search: RAG-powered search
   - Summarizer: Creates concise summaries

### How It Works

```python
# 1. Initialize the system
rag_system = AgenticRAGSystem()

# 2. Create the agent with tools
agent = rag_system.create_agent()

# 3. Chat with the agent
response = rag_system.chat("What is RAG and why is it important?")
```

The agent will:
1. Analyze your question
2. Decide to use the knowledge search tool
3. Retrieve relevant information
4. Generate a comprehensive response
5. Remember the conversation for context

## 🎮 Try These Examples

### Basic Queries
- "What is RAG and how does it work?"
- "Explain the history of AI agents"
- "How do I build my first agent?"

### Tool Usage
- "Calculate 42 * 17 + 89"
- "Tell me a joke about programming"
- "Summarize advanced agent techniques"

### Complex Reasoning
- "Compare RAG with traditional LLMs and calculate the percentage improvement in accuracy"
- "What are the key milestones in AI history and when did they occur?"

## 🔧 Customization

### Add Your Own Documents

```python
# In agentic_rag_demo.py
new_docs = [
    Document(
        text="Your custom content here",
        metadata={"source": "custom.txt", "topic": "Your Topic"}
    )
]
rag_system.create_knowledge_base(documents=new_docs)
```

### Create New Tools

```python
def custom_tool(parameter: str) -> str:
    """Your tool description"""
    # Tool logic here
    return result

# Add to agent
new_tool = FunctionTool.from_defaults(
    fn=custom_tool,
    name="tool_name",
    description="What this tool does"
)
```

## 📊 Architecture

```
┌─────────────────┐
│   User Query    │
└────────┬────────┘
         │
┌────────▼────────┐
│  ReAct Agent    │◄──── Reasoning Engine
└────────┬────────┘
         │
┌────────▼────────┐
│  Tool Selection │
└────────┬────────┘
         │
    ┌────┴────┬──────┬──────┐
    │         │      │      │
┌───▼──┐ ┌───▼──┐ ┌─▼──┐ ┌─▼──┐
│ RAG  │ │ Calc │ │Joke│ │Sum │
│Search│ │ Tool │ │Tool│ │Tool│
└───┬──┘ └───┬──┘ └─┬──┘ └─┬──┘
    │         │      │      │
    └────┬────┴──────┴──────┘
         │
┌────────▼────────┐
│    Response     │
└─────────────────┘
```

## 🎯 Advanced Features

### 1. Memory Management
The agent remembers your conversation history, allowing for contextual follow-ups:
```python
# First query
"What is RAG?"
# Follow-up
"Can you give me an example of how to implement it?"
```

### 2. Tool Chaining
The agent can use multiple tools in sequence:
```python
"Search for information about AI agents and then calculate how many years have passed since the Turing Test"
```

### 3. Self-Reflection
The agent evaluates its responses and can correct itself if needed.

## 🐛 Troubleshooting

### Common Issues

1. **"API Key not found"**
   - Make sure your `.env` file contains: `OPENAI_API_KEY=your_key_here`

2. **"Module not found"**
   - Ensure you've activated your virtual environment
   - Run `pip install -r requirements.txt` again

3. **"Storage directory error"**
   - The system will create necessary directories automatically
   - Ensure you have write permissions in the current directory

## 🚀 Next Steps

1. **Experiment with Different Models**
   - Try GPT-3.5 for faster responses
   - Use GPT-4 for complex reasoning

2. **Add More Tools**
   - Web search integration
   - Database queries
   - API calls

3. **Enhance the Knowledge Base**
   - Add your own documents
   - Implement dynamic document loading
   - Try different embedding models

4. **Build Production Features**
   - User authentication
   - Conversation persistence
   - Analytics and monitoring

## 📖 Resources

- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [ReAct Paper](https://arxiv.org/abs/2210.03629)
- [RAG Survey](https://arxiv.org/abs/2312.10997)
- [Original Google Cloud Example](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/gemini/sample-apps/llamaindex-rag)
