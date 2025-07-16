"""
🤖 LlamaIndex Advanced Agentic RAG Demo
A fun implementation showcasing agents with RAG capabilities!
"""

import os
from typing import List, Optional
from dotenv import load_dotenv

from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
    Settings,
    Document
)
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool, QueryEngineTool, ToolMetadata
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.composability import QASummaryQueryEngineBuilder
import json

load_dotenv()


class AgenticRAGSystem:
    """
    🎯 Our Agentic RAG System that combines:
    - Document indexing and retrieval
    - Agent-based reasoning
    - Tool usage for enhanced capabilities
    - Memory for context retention
    """
    
    def __init__(self):
        self.setup_llm()
        self.indices = {}
        self.agent = None
        
    def setup_llm(self):
        """Configure LLM and embedding models"""
        Settings.llm = OpenAI(model="gpt-4", temperature=0.7)
        Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
        
    def create_sample_documents(self) -> List[Document]:
        """Create fun sample documents about AI and programming"""
        sample_docs = [
            Document(
                text="""
                🚀 The History of AI Agents
                
                AI agents have evolved from simple rule-based systems to sophisticated 
                entities capable of reasoning, planning, and learning. The journey began 
                in the 1950s with the Turing Test and has accelerated with modern LLMs.
                
                Key milestones:
                - 1950s: Turing Test proposed
                - 1960s: ELIZA chatbot created
                - 1980s: Expert systems boom
                - 1990s: Intelligent agents in software
                - 2020s: LLM-powered autonomous agents
                
                Today's agents can use tools, access external knowledge, and even 
                collaborate with other agents to solve complex problems.
                """,
                metadata={"source": "ai_history.txt", "topic": "AI History"}
            ),
            Document(
                text="""
                🧰 RAG (Retrieval-Augmented Generation) Explained
                
                RAG is like giving an AI a library card! Instead of relying solely on 
                training data, RAG systems can:
                
                1. Search through documents (retrieval)
                2. Find relevant information (augmentation)
                3. Generate accurate responses (generation)
                
                Benefits of RAG:
                - Reduces hallucinations
                - Provides up-to-date information
                - Enables citing sources
                - Scales with your knowledge base
                
                Advanced RAG techniques include:
                - Hybrid search (keyword + semantic)
                - Reranking for relevance
                - Query expansion
                - Multi-hop reasoning
                """,
                metadata={"source": "rag_guide.txt", "topic": "RAG Technology"}
            ),
            Document(
                text="""
                🎮 Building Your First AI Agent
                
                Creating an AI agent is like teaching a robot to be your assistant!
                Here's a simple recipe:
                
                Ingredients:
                1. A language model (the brain)
                2. Tools (the hands)
                3. Memory (the notebook)
                4. Instructions (the guidebook)
                
                Step-by-step process:
                1. Define the agent's purpose
                2. Give it access to tools (search, calculate, etc.)
                3. Add memory for context
                4. Set up a feedback loop
                5. Test with real tasks!
                
                Pro tip: Start simple and add complexity gradually. Even a basic agent
                can be incredibly useful!
                """,
                metadata={"source": "agent_tutorial.txt", "topic": "Agent Building"}
            ),
            Document(
                text="""
                🔧 Advanced Agent Techniques
                
                Level up your agents with these advanced techniques:
                
                1. Multi-Agent Systems:
                   - Agents can collaborate
                   - Divide complex tasks
                   - Specialist agents for different domains
                
                2. Tool Creation:
                   - Agents can create their own tools
                   - Dynamic tool selection
                   - Tool chaining for complex workflows
                
                3. Self-Reflection:
                   - Agents evaluate their own responses
                   - Learn from mistakes
                   - Improve over time
                
                4. Hierarchical Planning:
                   - Break down complex goals
                   - Create sub-tasks
                   - Monitor progress
                
                Remember: The best agents are those that know their limitations and
                can ask for help when needed!
                """,
                metadata={"source": "advanced_agents.txt", "topic": "Advanced Techniques"}
            )
        ]
        return sample_docs
    
    def create_knowledge_base(self, documents: Optional[List[Document]] = None):
        """Create or load the vector index for our knowledge base"""
        index_path = "./storage/ai_knowledge"
        
        if documents is None:
            documents = self.create_sample_documents()
        
        if os.path.exists(index_path):
            print("📚 Loading existing knowledge base...")
            storage_context = StorageContext.from_defaults(persist_dir=index_path)
            index = load_index_from_storage(storage_context)
        else:
            print("🔨 Building new knowledge base...")
            parser = SimpleNodeParser.from_defaults(chunk_size=512, chunk_overlap=50)
            nodes = parser.get_nodes_from_documents(documents)
            index = VectorStoreIndex(nodes)
            index.storage_context.persist(persist_dir=index_path)
        
        self.indices["ai_knowledge"] = index
        return index
    
    def create_calculator_tool(self) -> FunctionTool:
        """Create a calculator tool for the agent"""
        def calculate(expression: str) -> str:
            """
            Calculate mathematical expressions.
            Args:
                expression: A mathematical expression to evaluate
            """
            try:
                result = eval(expression, {"__builtins__": {}}, {})
                return f"The result of {expression} is {result}"
            except Exception as e:
                return f"Error calculating {expression}: {str(e)}"
        
        return FunctionTool.from_defaults(
            fn=calculate,
            name="calculator",
            description="Useful for performing mathematical calculations"
        )
    
    def create_joke_tool(self) -> FunctionTool:
        """Create a fun joke generator tool"""
        def tell_joke(topic: str = "AI") -> str:
            """
            Tell a joke about the given topic.
            Args:
                topic: The topic for the joke
            """
            jokes = {
                "AI": "Why did the neural network go to therapy? It had too many deep issues!",
                "programming": "Why do programmers prefer dark mode? Because light attracts bugs!",
                "data": "Why did the data scientist break up with the statistician? They had too many outliers in their relationship!",
                "default": "Why don't scientists trust atoms? Because they make up everything!"
            }
            return jokes.get(topic.lower(), jokes["default"])
        
        return FunctionTool.from_defaults(
            fn=tell_joke,
            name="joke_teller",
            description="Tell jokes about AI, programming, or data science"
        )
    
    def create_summary_tool(self) -> FunctionTool:
        """Create a document summarization tool"""
        def summarize_knowledge(query: str) -> str:
            """
            Summarize knowledge from the AI knowledge base.
            Args:
                query: Topic to summarize
            """
            if "ai_knowledge" not in self.indices:
                return "Knowledge base not initialized!"
            
            query_engine = self.indices["ai_knowledge"].as_query_engine()
            response = query_engine.query(f"Provide a brief summary about: {query}")
            return str(response)
        
        return FunctionTool.from_defaults(
            fn=summarize_knowledge,
            name="knowledge_summarizer",
            description="Summarize information from the AI knowledge base"
        )
    
    def create_agent(self):
        """Create the main ReAct agent with tools and knowledge"""
        print("🤖 Initializing the AI Agent...")
        
        # Create knowledge base
        knowledge_index = self.create_knowledge_base()
        
        # Create query engine tool for RAG
        query_engine = knowledge_index.as_query_engine(similarity_top_k=3)
        rag_tool = QueryEngineTool(
            query_engine=query_engine,
            metadata=ToolMetadata(
                name="ai_knowledge_search",
                description="Search the AI knowledge base for information about agents, RAG, and AI techniques"
            )
        )
        
        # Create additional tools
        calculator_tool = self.create_calculator_tool()
        joke_tool = self.create_joke_tool()
        summary_tool = self.create_summary_tool()
        
        # Initialize memory
        memory = ChatMemoryBuffer.from_defaults(token_limit=3000)
        
        # Create the agent
        self.agent = ReActAgent.from_tools(
            tools=[rag_tool, calculator_tool, joke_tool, summary_tool],
            llm=Settings.llm,
            memory=memory,
            verbose=True,
            max_iterations=10
        )
        
        print("✅ Agent ready! It can search knowledge, calculate, tell jokes, and summarize!")
        return self.agent
    
    def chat(self, message: str):
        """Chat with the agent"""
        if not self.agent:
            self.create_agent()
        
        response = self.agent.chat(message)
        return response
    
    def save_conversation(self, filename: str = "conversation_history.json"):
        """Save the conversation history"""
        if not self.agent:
            return
        
        history = []
        for msg in self.agent.memory.get_all():
            history.append({
                "role": msg.role,
                "content": msg.content
            })
        
        with open(filename, 'w') as f:
            json.dump(history, f, indent=2)
        print(f"💾 Conversation saved to {filename}")


def main():
    """Run the interactive demo"""
    print("🌟 Welcome to the LlamaIndex Agentic RAG Demo! 🌟")
    print("=" * 50)
    
    # Initialize the system
    rag_system = AgenticRAGSystem()
    rag_system.create_agent()
    
    print("\n📝 Example queries you can try:")
    print("- What is RAG and how does it work?")
    print("- Calculate 42 * 17 + 89")
    print("- Tell me a joke about AI")
    print("- Summarize the evolution of AI agents")
    print("- How do I build my first agent?")
    print("- What are advanced agent techniques?")
    print("\nType 'exit' to quit, 'save' to save conversation\n")
    
    while True:
        user_input = input("\n🤔 You: ")
        
        if user_input.lower() == 'exit':
            print("👋 Thanks for chatting! Goodbye!")
            break
        elif user_input.lower() == 'save':
            rag_system.save_conversation()
            continue
        
        print("\n🤖 Agent thinking...\n")
        response = rag_system.chat(user_input)
        print(f"\n💬 Agent: {response}")


if __name__ == "__main__":
    main()