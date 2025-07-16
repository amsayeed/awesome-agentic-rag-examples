"""
CrewAI Agentic PDF Processing Pipeline

Agentic RAG pipeline using CrewAI for processing
PDF documents with multiple specialized agents working in coordination.

"""

import os
import logging
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from pathlib import Path

# Core CrewAI imports
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain.chains import RetrievalQA

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class PipelineConfig:
    """Configuration class for the CrewAI PDF processing pipeline."""
    
    pdf_path: str
    openai_api_key: str
    chunk_size: int = 800
    chunk_overlap: int = 100
    max_tokens: int = 2000
    temperature: float = 0.1
    vector_store_path: Optional[str] = None


class PDFRetrievalTool(BaseTool):
    """
    Custom tool for retrieving relevant content from PDF documents.
    
    This tool uses vector similarity search to find the most relevant 
    document chunks for a given query.
    """
    
    name: str = "pdf_retrieval"
    description: str = "Search for information in PDF documents. Input should be a search query string."
    retrieval_chain: Any = None
    
    def __init__(self, retrieval_chain: RetrievalQA):
        """Initialize the PDF retrieval tool with a retrieval chain."""
        super().__init__()
        self.retrieval_chain = retrieval_chain
    
    def _run(self, query: str) -> str:
        """
        Execute the retrieval tool to find relevant content.
        
        Args:
            query (str): The search query for document retrieval
            
        Returns:
            str: Retrieved content from the PDF document
        """
        try:
            result = self.retrieval_chain.run(query)
            logger.info(f"Successfully retrieved content for query: {query[:50]}...")
            return result
        except Exception as e:
            logger.error(f"Error during retrieval: {str(e)}")
            return f"Error retrieving content: {str(e)}"


class CrewAIPDFPipeline:
    """
    Main pipeline class for processing PDF documents using CrewAI agents.
    
    This pipeline coordinates multiple specialized agents to analyze,
    extract insights, and generate comprehensive reports from PDF documents.
    """
    
    def __init__(self, config: PipelineConfig):
        """
        Initialize the CrewAI PDF processing pipeline.
        
        Args:
            config (PipelineConfig): Configuration object containing pipeline settings
        """
        self.config = config
        self.retrieval_chain = None
        self.pdf_tool = None
        self.crew = None
        
        # Set OpenAI API key
        os.environ["OPENAI_API_KEY"] = config.openai_api_key
        
        logger.info("CrewAI PDF Pipeline initialized")
    
    def setup_document_retrieval(self) -> None:
        """
        Set up the document retrieval system using vector embeddings.
        
        This method loads the PDF, splits it into chunks, creates embeddings,
        and sets up the retrieval chain for similarity search.
        """
        try:
            # Validate PDF path exists
            pdf_path = Path(self.config.pdf_path)
            if not pdf_path.exists():
                raise FileNotFoundError(f"PDF file not found: {self.config.pdf_path}")
            
            # Load PDF document
            logger.info(f"Loading PDF from: {self.config.pdf_path}")
            loader = PyPDFLoader(self.config.pdf_path)
            documents = loader.load()
            
            # Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.config.chunk_size,
                chunk_overlap=self.config.chunk_overlap
            )
            texts = text_splitter.split_documents(documents)
            logger.info(f"Split document into {len(texts)} chunks")
            
            # Create embeddings and vector store
            embeddings = OpenAIEmbeddings()
            vectorstore = FAISS.from_documents(texts, embeddings)
            
            # Save vector store if path provided
            if self.config.vector_store_path:
                vectorstore.save_local(self.config.vector_store_path)
                logger.info(f"Vector store saved to: {self.config.vector_store_path}")
            
            # Create retrieval chain
            llm = OpenAI(
                model="gpt-3.5-turbo-instruct",
                temperature=self.config.temperature,
                max_tokens=2000  # Reduced to avoid token limit issues
            )
            self.retrieval_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=vectorstore.as_retriever()
            )
            
            # Create PDF retrieval tool
            self.pdf_tool = PDFRetrievalTool(self.retrieval_chain)
            
            logger.info("Document retrieval system setup complete")
            
        except Exception as e:
            logger.error(f"Error setting up document retrieval: {str(e)}")
            raise
    
    def create_agents(self) -> Dict[str, Agent]:
        """
        Create specialized agents for different aspects of PDF analysis.
        
        Returns:
            Dict[str, Agent]: Dictionary of created agents
        """
        # Document Analyst Agent
        document_analyst = Agent(
            role="Document Analyst",
            goal="Analyze PDF documents and extract key information, structure, and themes",
            backstory="""You are an expert document analyst with years of experience in 
            analyzing complex documents. You excel at identifying key themes, important 
            information, and document structure. You have a keen eye for detail and can 
            quickly understand the main points of any document.""",
            tools=[self.pdf_tool],
            verbose=True,
            allow_delegation=False
        )
        
        # Content Summarizer Agent
        content_summarizer = Agent(
            role="Content Summarizer",
            goal="Create comprehensive and concise summaries of document content",
            backstory="""You are a skilled content summarizer who can distill complex 
            information into clear, concise summaries. You understand how to maintain 
            the essential meaning while making content accessible to different audiences. 
            Your summaries are both comprehensive and easy to understand.""",
            tools=[self.pdf_tool],
            verbose=True,
            allow_delegation=False
        )
        
        # Quality Assurance Agent
        qa_agent = Agent(
            role="Quality Assurance Specialist",
            goal="Verify accuracy and completeness of analysis and summaries",
            backstory="""You are a meticulous quality assurance specialist with expertise 
            in document analysis validation. You ensure that all extracted information 
            is accurate, complete, and properly referenced. You have a systematic approach 
            to verification and quality control.""",
            tools=[self.pdf_tool],
            verbose=True,
            allow_delegation=False
        )
        
        # Insight Generator Agent
        insight_generator = Agent(
            role="Insight Generator",
            goal="Generate actionable insights and recommendations from document analysis",
            backstory="""You are a strategic analyst who excels at identifying patterns, 
            implications, and actionable insights from complex information. You can see 
            the bigger picture and provide valuable recommendations based on document 
            analysis. Your insights help decision-makers understand the practical 
            implications of the information.""",
            tools=[self.pdf_tool],
            verbose=True,
            allow_delegation=False
        )
        
        agents = {
            "analyst": document_analyst,
            "summarizer": content_summarizer,
            "qa": qa_agent,
            "insight_generator": insight_generator
        }
        
        logger.info(f"Created {len(agents)} specialized agents")
        return agents
    
    def create_tasks(self, agents: Dict[str, Agent]) -> List[Task]:
        """
        Create tasks for the agents to execute in sequence.
        
        Args:
            agents (Dict[str, Agent]): Dictionary of available agents
            
        Returns:
            List[Task]: List of tasks to be executed
        """
        # Document Analysis Task
        analysis_task = Task(
            description="""Analyze the PDF document comprehensively. Extract and identify:
            1. Document structure and organization
            2. Key themes and topics
            3. Important facts and data points
            4. Main arguments and conclusions
            5. Any tables, figures, or special content
            
            Provide a detailed analysis report with specific page references where possible.""",
            agent=agents["analyst"],
            expected_output="A comprehensive document analysis report with key findings and structure overview"
        )
        
        # Content Summarization Task
        summarization_task = Task(
            description="""Based on the document analysis, create multiple types of summaries:
            1. Executive summary (2-3 paragraphs)
            2. Detailed summary (1-2 pages)
            3. Key points bullet list
            4. Main takeaways for different stakeholder groups
            
            Ensure summaries are accurate, complete, and well-structured.""",
            agent=agents["summarizer"],
            expected_output="Multiple summary formats catering to different audience needs",
            context=[analysis_task]
        )
        
        # Quality Assurance Task
        qa_task = Task(
            description="""Review and validate the document analysis and summaries for:
            1. Accuracy of extracted information
            2. Completeness of coverage
            3. Consistency across different outputs
            4. Proper citation and referencing
            5. Clarity and readability
            
            Provide a quality assessment report with any recommended corrections.""",
            agent=agents["qa"],
            expected_output="Quality assurance report with validation results and recommendations",
            context=[analysis_task, summarization_task]
        )
        
        # Insight Generation Task
        insight_task = Task(
            description="""Generate strategic insights and actionable recommendations based on:
            1. Document content and themes
            2. Implications for stakeholders
            3. Potential applications and use cases
            4. Recommended next steps
            5. Areas requiring further investigation
            
            Focus on practical, actionable insights that add value beyond basic summarization.""",
            agent=agents["insight_generator"],
            expected_output="Strategic insights report with actionable recommendations",
            context=[analysis_task, summarization_task, qa_task]
        )
        
        tasks = [analysis_task, summarization_task, qa_task, insight_task]
        logger.info(f"Created {len(tasks)} tasks for execution")
        return tasks
    
    def setup_crew(self) -> None:
        """Set up the CrewAI crew with agents and tasks."""
        try:
            agents = self.create_agents()
            tasks = self.create_tasks(agents)
            
            self.crew = Crew(
                agents=list(agents.values()),
                tasks=tasks,
                process=Process.sequential,
                verbose=True
            )
            
            logger.info("CrewAI crew setup complete")
            
        except Exception as e:
            logger.error(f"Error setting up crew: {str(e)}")
            raise
    
    def execute_pipeline(self) -> Dict[str, Any]:
        """
        Execute the complete PDF processing pipeline.
        
        Returns:
            Dict[str, Any]: Results from the pipeline execution
        """
        try:
            logger.info("Starting CrewAI PDF processing pipeline")
            
            # Setup components
            self.setup_document_retrieval()
            self.setup_crew()
            
            # Execute the crew
            logger.info("Executing CrewAI crew")
            result = self.crew.kickoff()
            
            logger.info("Pipeline execution completed successfully")
            
            return {
                "status": "success",
                "result": result,
                "pipeline_config": self.config
            }
            
        except Exception as e:
            logger.error(f"Pipeline execution failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "pipeline_config": self.config
            }


def main():
    """
    Main function to demonstrate the CrewAI PDF processing pipeline.
    
    This function shows how to configure and run the pipeline with
    a sample PDF document.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="CrewAI PDF Processing Pipeline")
    parser.add_argument("--pdf", required=True, help="Path to PDF file")
    parser.add_argument("--api-key", help="OpenAI API key (or set OPENAI_API_KEY env var)")
    parser.add_argument("--vector-store", default="./vector_store", help="Path to save vector store")
    parser.add_argument("--chunk-size", type=int, default=800, help="Text chunk size (default: 800)")
    parser.add_argument("--chunk-overlap", type=int, default=100, help="Text chunk overlap (default: 100)")
    
    args = parser.parse_args()
    
    # Get API key
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OpenAI API key required (--api-key or OPENAI_API_KEY env var)")
        return 1
    
    # Configure pipeline
    config = PipelineConfig(
        pdf_path=args.pdf,
        openai_api_key=api_key,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
        max_tokens=2000,
        temperature=0.1,
        vector_store_path=args.vector_store
    )
    
    # Initialize and run pipeline
    pipeline = CrewAIPDFPipeline(config)
    results = pipeline.execute_pipeline()
    
    # Display results
    if results["status"] == "success":
        print("\n✅ Pipeline executed successfully!")
        print("\n" + "="*80)
        print("RESULTS")
        print("="*80)
        print(results["result"])
        print("\n" + "="*80)
    else:
        print(f"\n❌ Pipeline execution failed: {results['error']}")
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
