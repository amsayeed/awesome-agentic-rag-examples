"""
🎨 LlamaIndex Agentic RAG - Interactive Streamlit App
"""

import streamlit as st
import os
from dotenv import load_dotenv
from agentic_rag_demo import AgenticRAGSystem
import time

load_dotenv()

# Page config
st.set_page_config(
    page_title="Agentic RAG Demo",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'rag_system' not in st.session_state:
    st.session_state.rag_system = None
    st.session_state.messages = []
    st.session_state.agent_thoughts = []

# Title and description
st.title("🤖 LlamaIndex Advanced Agentic RAG Demo")
st.markdown("""
Welcome to the interactive Agentic RAG demo! This system combines:
- 📚 **RAG (Retrieval-Augmented Generation)** for accurate, sourced responses
- 🧠 **ReAct Agent** for reasoning and tool usage
- 🛠️ **Multiple Tools** including search, calculator, and more
- 💾 **Memory** for contextual conversations
""")

# Sidebar
with st.sidebar:
    st.header("🎮 Control Panel")
    
    # API Key check
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("⚠️ Please set your OPENAI_API_KEY in the .env file")
        st.stop()
    else:
        st.success("✅ API Key loaded")
    
    # Initialize button
    if st.button("🚀 Initialize Agent", type="primary"):
        with st.spinner("Initializing agent and knowledge base..."):
            st.session_state.rag_system = AgenticRAGSystem()
            st.session_state.rag_system.create_agent()
            st.success("🎉 Agent ready to chat!")
    
    # Example queries
    st.header("💡 Example Queries")
    example_queries = [
        "What is RAG and how does it work?",
        "Calculate 42 * 17 + 89",
        "Tell me a joke about AI",
        "Summarize the evolution of AI agents",
        "How do I build my first agent?",
        "What are advanced agent techniques?"
    ]
    
    for query in example_queries:
        if st.button(f"📝 {query}", key=f"example_{query}"):
            st.session_state.messages.append({"role": "user", "content": query})
    
    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.agent_thoughts = []
        st.rerun()

# Main chat interface
col1, col2 = st.columns([2, 1])

with col1:
    st.header("💬 Chat")
    
    # Check if agent is initialized
    if st.session_state.rag_system is None:
        st.info("👈 Please initialize the agent using the button in the sidebar")
    else:
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask me anything about AI, agents, or RAG..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get agent response
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                # Show thinking animation
                with st.spinner("🤔 Agent thinking..."):
                    # Clear previous thoughts
                    st.session_state.agent_thoughts = []
                    
                    # Get response
                    response = st.session_state.rag_system.chat(prompt)
                    full_response = str(response)
                
                # Display response with typing effect
                displayed_text = ""
                for char in full_response:
                    displayed_text += char
                    message_placeholder.markdown(displayed_text + "▌")
                    time.sleep(0.01)
                
                message_placeholder.markdown(full_response)
            
            # Add assistant message
            st.session_state.messages.append({"role": "assistant", "content": full_response})

with col2:
    st.header("🧠 Agent Tools")
    
    if st.session_state.rag_system and st.session_state.rag_system.agent:
        st.subheader("Available Tools:")
        tools_info = {
            "🔍 Knowledge Search": "Search AI knowledge base",
            "🧮 Calculator": "Perform calculations",
            "😄 Joke Teller": "Tell AI/programming jokes",
            "📝 Summarizer": "Summarize topics"
        }
        
        for tool, desc in tools_info.items():
            st.info(f"**{tool}**\n{desc}")
        
        # Memory status
        st.subheader("💾 Memory Status")
        if st.session_state.rag_system.agent.memory:
            chat_history = st.session_state.rag_system.agent.memory.get_all()
            st.metric("Messages in memory", len(chat_history))
    
    # Fun facts
    st.subheader("🎯 Fun Facts")
    facts = [
        "Agents can reason step-by-step using ReAct pattern",
        "RAG reduces hallucinations by grounding responses in data",
        "This agent has persistent memory across conversations",
        "The agent decides which tools to use autonomously"
    ]
    for fact in facts:
        st.success(f"💡 {fact}")

# Footer
st.markdown("---")
