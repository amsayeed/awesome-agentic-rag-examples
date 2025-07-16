# CrewAI PDF Processing Pipeline

A complete, production-ready example of using CrewAI agents to analyze and extract insights from PDF documents using multiple specialized agents working in coordination.

## 🚀 Quick Start

### 1. Activate Virtual Environment

```bash
cd crewai_examples
source venv/bin/activate  # Virtual environment already created
```

### 2. Set OpenAI API Key

```bash
export OPENAI_API_KEY="your-api-key-here"
```

### 3. Run the Pipeline

```bash
python agentic_pdf_walkthrough.py --pdf "your_document.pdf"
```

## 📋 Features

- **Multi-Agent System**: 4 specialized agents working together
  - **Document Analyst**: Extracts structure and key information
  - **Content Summarizer**: Creates comprehensive summaries
  - **Quality Assurance**: Validates accuracy and completeness
  - **Insight Generator**: Provides actionable recommendations

- **Vector-Based Retrieval**: Uses FAISS for efficient similarity search
- **Configurable Processing**: Adjustable chunk sizes and overlap
- **Persistent Vector Store**: Save and reuse document embeddings
- **Command-Line Interface**: Easy to use with various options

## 🛠️ Command Line Options

```bash
python agentic_pdf_walkthrough.py --help

Options:
  --pdf PDF             Path to PDF file (required)
  --api-key API_KEY     OpenAI API key (optional if set as env var)
  --vector-store PATH   Path to save vector store (default: ./vector_store)
  --chunk-size SIZE     Text chunk size (default: 800)
  --chunk-overlap SIZE  Text chunk overlap (default: 100)
```

## 📝 Example Usage

```bash
# Basic usage
python agentic_pdf_walkthrough.py --pdf "report.pdf"

# With custom settings
python agentic_pdf_walkthrough.py \
  --pdf "technical_document.pdf" \
  --chunk-size 800 \
  --chunk-overlap 100 \
  --vector-store "./embeddings/tech_docs"

# For files with spaces in the name
python agentic_pdf_walkthrough.py --pdf "My Document Name.pdf"
```

## 🔧 Pipeline Architecture

```
PDF Document
    ↓
Document Loader (PyPDF)
    ↓
Text Splitter (Chunks)
    ↓
Embeddings (OpenAI)
    ↓
Vector Store (FAISS)
    ↓
CrewAI Agents
    ├── Document Analyst
    ├── Content Summarizer
    ├── Quality Assurance
    └── Insight Generator
    ↓
Final Report
```

## 📊 Output Structure

The pipeline provides comprehensive analysis including:

### 1. Document Analysis
- Document structure and organization
- Key themes and topics
- Important facts and data points
- Main arguments and conclusions

### 2. Content Summaries
- Executive summary (2-3 paragraphs)
- Detailed summary (1-2 pages)
- Key points bullet list
- Stakeholder-specific summaries

### 3. Quality Assessment
- Accuracy verification
- Completeness check
- Consistency validation
- Quality recommendations

### 4. Strategic Insights
- Actionable recommendations
- Pattern identification
- Next steps
- Areas for further investigation

## 🧠 Agent Details

### Document Analyst
```python
role="Document Analyst"
goal="Analyze PDF documents and extract key information, structure, and themes"
```

### Content Summarizer
```python
role="Content Summarizer"
goal="Create comprehensive and concise summaries of document content"
```

### Quality Assurance Specialist
```python
role="Quality Assurance Specialist"
goal="Verify accuracy and completeness of analysis and summaries"
```

### Insight Generator
```python
role="Insight Generator"
goal="Generate actionable insights and recommendations from document analysis"
```

## ⚙️ Technical Details

### Dependencies
All required packages are in `requirements.txt`:
```
crewai>=0.1.0
langchain>=0.1.0
langchain-community>=0.0.10
langchain-openai>=0.0.5
faiss-cpu>=1.7.4
pypdf>=3.17.0
openai>=1.0.0
python-dotenv>=1.0.0
```

### Configuration Options

```python
PipelineConfig(
    pdf_path: str           # Path to PDF file
    openai_api_key: str     # OpenAI API key
    chunk_size: int = 800   # Size of text chunks
    chunk_overlap: int = 100 # Overlap between chunks
    max_tokens: int = 2000  # Max tokens for responses
    temperature: float = 0.1 # LLM temperature
    vector_store_path: str  # Path to save vectors
)
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Make sure virtual environment is activated
   source venv/bin/activate
   ```

2. **API Key Issues**
   ```bash
   # Verify your OpenAI API key
   echo $OPENAI_API_KEY
   ```

3. **PDF Processing Errors**
   - Ensure the PDF file exists and is readable
   - Try reducing chunk size for large documents
   - Check that the PDF contains text (not just images)

4. **Memory Issues**
   - Reduce chunk_size for large documents
   - Process documents in smaller batches
   - Increase system memory allocation

### Performance Tips

- **Academic Papers**: Use chunk_size=1200-1500 for better context
- **Technical Documents**: Use chunk_size=600-1000 for precision
- **General Documents**: Default chunk_size=800 works well
- **Lower temperature** (0.0-0.2) for factual analysis
- **Higher temperature** (0.3-0.5) for creative insights

### Token Limit Issues

If you encounter errors like "maximum context length is 4097 tokens":
- The default settings are optimized to avoid this
- For larger documents, reduce `--chunk-size` to 600
- The pipeline uses `gpt-3.5-turbo-instruct` model with 2000 max tokens
- Consider processing very large PDFs in sections


## 🤝 Contributing

Feel free to submit issues or pull requests to improve this example!