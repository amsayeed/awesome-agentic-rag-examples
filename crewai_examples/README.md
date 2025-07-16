# CrewAI Examples 🤖👥

A comprehensive collection of CrewAI-powered agentic RAG examples demonstrating multi-agent coordination for document processing and analysis.

## 📋 Overview

This directory contains practical examples of using CrewAI framework to build sophisticated agentic RAG pipelines where multiple specialized AI agents work together to analyze, process, and extract insights from documents.

### What is CrewAI?

CrewAI is a cutting-edge framework for orchestrating role-playing, autonomous AI agents. By fostering collaborative intelligence, CrewAI empowers agents to work together seamlessly, tackling complex tasks through coordinated teamwork.

### Why Agentic RAG with CrewAI?

- **🎭 Role Specialization**: Each agent has a specific expertise (analysis, summarization, QA, etc.)
- **🔄 Collaborative Workflow**: Agents pass information and build upon each other's work
- **📊 Quality Assurance**: Built-in validation and quality control through dedicated QA agents
- **🎯 Targeted Outputs**: Different agents produce outputs tailored for specific use cases
- **🚀 Scalability**: Easy to add new agents or modify existing workflows

## 🚀 Getting Started

### Prerequisites

```bash
# Python 3.8+
python --version

# Required packages
pip install crewai
pip install langchain
pip install openai
pip install faiss-cpu
pip install pypdf
```

### Environment Setup

1. **Clone the repository** (if you haven't already):
```bash
git clone https://github.com/amsayeed/awesome-agentic-rag-examples.git
cd awesome-agentic-rag-examples/crewai_examples
```

2. **Set up environment variables**:
```bash
# Create a .env file or export directly
export OPENAI_API_KEY="your-openai-api-key-here"
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt  # From the root directory
```

## 📁 Examples in This Directory

### 1. Agentic PDF Walkthrough (`agentic_pdf_walkthrough.py`)

A comprehensive multi-agent pipeline for processing PDF documents with four specialized agents:

#### 🧠 Agent Roles:

- **📊 Document Analyst**: 
  - Analyzes document structure and organization
  - Extracts key themes, topics, and data points
  - Identifies main arguments and conclusions

- **📝 Content Summarizer**: 
  - Creates executive summaries (2-3 paragraphs)
  - Generates detailed summaries (1-2 pages)  
  - Produces key points and takeaways for different audiences

- **✅ Quality Assurance Specialist**: 
  - Validates accuracy of extracted information
  - Ensures completeness and consistency
  - Provides quality assessment reports

- **💡 Insight Generator**: 
  - Identifies patterns and implications
  - Generates actionable recommendations
  - Suggests next steps and areas for investigation

#### 🔧 Features:

- **Production-ready architecture** with proper error handling
- **Comprehensive logging** for debugging and monitoring  
- **Configurable parameters** for different document types
- **Vector store persistence** for reusability
- **Modular design** for easy customization

## 🛠️ Usage Instructions

### Basic Usage

```python
from agentic_pdf_walkthrough import CrewAIPDFPipeline, PipelineConfig

# Configure the pipeline
config = PipelineConfig(
    pdf_path="path/to/your/document.pdf",
    openai_api_key="your-openai-api-key",
    chunk_size=1000,
    chunk_overlap=200,
    max_tokens=4000,
    temperature=0.1,
    vector_store_path="./vector_store"
)

# Initialize and run the pipeline
pipeline = CrewAIPDFPipeline(config)
results = pipeline.execute_pipeline()

# Check results
if results["status"] == "success":
    print("Analysis completed successfully!")
    print("Results:", results["result"])
else:
    print("Error:", results["error"])
```

### Advanced Configuration

```python
# Custom configuration for specific use cases
config = PipelineConfig(
    pdf_path="research_paper.pdf",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    chunk_size=1500,          # Larger chunks for academic papers
    chunk_overlap=300,        # More overlap for better context
    max_tokens=6000,          # More tokens for detailed analysis
    temperature=0.05,         # Lower temperature for factual content
    vector_store_path="./research_vectors"
)
```

## 📊 Expected Outputs

The pipeline generates structured outputs from each agent:

### 1. Document Analysis Report
- Document structure and organization
- Key themes and topics identified
- Important facts and data points
- Main arguments and conclusions
- References to tables, figures, and special content

### 2. Multi-Format Summaries
- **Executive Summary**: 2-3 paragraph overview
- **Detailed Summary**: 1-2 page comprehensive summary  
- **Key Points**: Bullet-point format for quick reference
- **Stakeholder Summaries**: Tailored for different audiences

### 3. Quality Assessment
- Accuracy validation of extracted information
- Completeness assessment
- Consistency checks across outputs
- Recommendations for improvements

### 4. Strategic Insights
- Pattern identification and implications
- Actionable recommendations
- Suggested next steps
- Areas requiring further investigation

## 🔧 Customization Guide

### Adding New Agents

```python
# Example: Adding a Citation Agent
citation_agent = Agent(
    role="Citation Specialist",
    goal="Extract and format citations and references",
    backstory="""You are an expert in academic citations and 
    reference management. You excel at identifying and properly 
    formatting citations from academic and professional documents.""",
    tools=[self.pdf_tool],
    verbose=True,
    allow_delegation=False
)
```

### Modifying Agent Workflows

```python
# Example: Adding context between tasks
citation_task = Task(
    description="Extract all citations and create a bibliography",
    agent=citation_agent,
    expected_output="Formatted bibliography with all document citations",
    context=[analysis_task, summarization_task]  # Build on previous work
)
```

### Custom Tools

```python
# Example: Web search tool for fact-checking
class WebSearchTool(BaseTool):
    name = "web_search"
    description = "Search the web for fact-checking and additional context"
    
    def _run(self, query: str) -> str:
        # Implement web search logic
        return search_results
```

## 🐛 Troubleshooting

### Common Issues

1. **OpenAI API Key Error**
   ```bash
   Error: OpenAI API key not found
   Solution: Set OPENAI_API_KEY environment variable
   ```

2. **PDF Loading Issues**
   ```bash
   Error: Could not load PDF file
   Solution: Check file path and ensure PDF is not corrupted
   ```

3. **Memory Issues with Large Documents**
   ```bash
   Error: Out of memory
   Solution: Reduce chunk_size or process in smaller batches
   ```

4. **Vector Store Permission Errors**
   ```bash
   Error: Permission denied writing vector store
   Solution: Check write permissions for vector_store_path
   ```

### Performance Optimization

- **Chunk Size**: Larger chunks (1500-2000) for academic papers, smaller (500-1000) for general documents
- **Temperature**: Lower (0.0-0.2) for factual analysis, higher (0.3-0.7) for creative insights
- **Token Limits**: Adjust based on document complexity and desired detail level

### Ideas
- New agent types (e.g., Citation Agent, Fact-Checker Agent)
- Integration with other document formats (Word, PowerPoint, etc.)
- Advanced visualization of agent interactions
- Performance benchmarking tools
- Multi-language support

