import streamlit as st
import asyncio
from google.adk.agents import Agent
from google.adk.tools import google_search
from google.genai import types
from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LoopAgent, LlmAgent
from google.adk.runners import InMemoryRunner
from google.adk.tools import AgentTool, FunctionTool, google_search
from google.genai import types
from PyPDF2 import PdfReader
from typing import Dict, List

from google.adk.apps.app import App, EventsCompactionConfig
from google.adk.models.google_llm import Gemini
from google.adk.sessions import DatabaseSessionService
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.tools.tool_context import ToolContext
from agent_with_abm import *


if 'runner' not in st.session_state:
    st.session_state.runner = InMemoryRunner(agent=root2_agent)
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": f"Hello! Ask me about Interest Rates, Credit Spread, Forex, and Inflation based on {all_docs} documents."})

# --- Streamlit UI Components ---

st.title("📈 Multi-Agent Bond Market Simulator")
st.markdown("Powered by your specialized `Gemini 2.5 Flash Lite`.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about your JPM markets documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Running your simulation..."):
            agent_response_list = asyncio.run(st.session_state.runner.run_debug(prompt))
    
        # Initialize tracking variables - MUST be inside the chat_message context
        agent_outputs = []  # Explicitly initialize as empty list
        total_tokens = 0
        
        # Process all events to extract agent outputs
        for event in agent_response_list:
            
            # Sum all tokens
            if hasattr(event, 'usage_metadata') and event.usage_metadata:
                total_tokens += event.usage_metadata.total_token_count
            
            # Extract agent name and text output
            if (hasattr(event, 'content') and 
                event.content and 
                hasattr(event.content, 'parts') and 
                event.content.parts):
                
                extracted_text = event.content.parts[0].text
                
                # Only capture non-empty text
                if extracted_text and extracted_text.strip():
                    # Try to get agent name from the event
                    agent_name = "Agent"
                    if hasattr(event, 'agent_name') and event.agent_name:
                        agent_name = event.agent_name
                    elif hasattr(event, 'name') and event.name:
                        agent_name = event.name
                    
                    agent_outputs.append({
                        'agent': agent_name,
                        'content': extracted_text.strip()
                    })
        
        # Display all agent outputs with expandable sections
        if agent_outputs:
            # Show final output prominently at the top
            st.markdown("### 🎯 Final Output")
            st.markdown(agent_outputs[-1]['content'])
            
            # Show intermediate agent outputs in expandable sections
            if len(agent_outputs) > 1:
                st.markdown("---")
                st.markdown("### 🔍 Agent Activity Log")
                
                for idx, output in enumerate(agent_outputs[:-1]):  # Exclude the last one (already shown)
                    with st.expander(f"**{output['agent']}** (Step {idx + 1})"):
                        st.markdown(output['content'])
            
            # Append the final response to chat history
            st.session_state.messages.append({
                "role": "assistant", 
                "content": agent_outputs[-1]['content']
            })
        else:
            # Fallback if no outputs were found
            error_msg = "Error: Agent finished but no text responses were found in the sequence."
            st.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
        
        st.caption(f"Total Process Tokens: {total_tokens}")