'''
This file defines the agent's brain: its prompt, memory, and the executor that runs its reasoning loop.

The agent is a React Agent, which means it can use tools to get information and reason about it.

The agent is also a memory-aware agent, which means it can use the conversation history to reason about the user's question.

The agent is also a tool-aware agent, which means it can use the tools to get information and reason about it.
'''
import os
import logging
from typing import Dict
from dotenv import load_dotenv

from langchain.agents import AgentExecutor, create_react_agent
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

from .tools import available_tools

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

# --- Agent Prompt Template ---
agent_prompt_template = """
You are a friendly and encouraging Fitbit AI assistant. Your name is Aura.
Your goal is to help users understand their health data and motivate them.

You have access to the following tools to answer user questions. You must use these tools to get the most up-to-date information.
The current user's ID is '{user_id}'. Always use this ID when calling tools.

TOOLS:
------
{tool_names}

TOOL DESCRIPTIONS:
----------------
{tools}

HOW TO USE THE TOOLS:
---------------------
When you need to use a tool, use the following format:

Thought: Do I need to use a tool? Yes. I should use a tool to answer the user's question.
Action: The name of the tool to use
Action Input: {{"user_id": "{user_id}"}}
Observation: [The result of the tool will be inserted here]

When you have a response to say to the user, or if you don't need to use a tool, you MUST use the format:

Thought: Do I need to use a tool? No. I have enough information to respond.
Final Answer: [Your response to the user here]

CONVERSATION:
-------------
History:
{chat_history}

User Question: {input}

YOUR RESPONSE:
--------------
Thought:
{agent_scratchpad}
"""

prompt = PromptTemplate.from_template(agent_prompt_template)

# --- LLM and Memory Initialization ---
try:
    llm = ChatAnthropic(model='claude-3-5-sonnet-20240620', temperature=0)
except Exception as e:
    logger.error("Failed to initialize Anthropic client. Make sure ANTHROPIC_API_KEY is set in your .env file.")
    llm = None

# In-memory store for conversations. In production, this would be Redis or a database.
conversation_memory_store: Dict[str, ConversationBufferMemory] = {}

def get_memory_for_session(session_id: str) -> ConversationBufferMemory:
    """Retrieves or creates memory for a conversation session."""
    if session_id not in conversation_memory_store:
        conversation_memory_store[session_id] = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
    return conversation_memory_store[session_id]

# --- Agent Creation ---
agent = create_react_agent(llm, available_tools, prompt) if llm else None

def get_agent_executor(session_id: str, user_id: str) -> AgentExecutor:
    """Creates an AgentExecutor with session-specific memory and user context."""
    if not agent:
        raise ValueError("Agent is not initialized. Check LLM configuration.")
        
    memory = get_memory_for_session(session_id)
    
    # Create a custom prompt with the user_id
    custom_prompt = PromptTemplate.from_template(agent_prompt_template).partial(user_id=user_id)
    
    # Create a new agent instance with the custom prompt
    custom_agent = create_react_agent(llm, available_tools, custom_prompt)
    
    return AgentExecutor(
        agent=custom_agent,
        tools=available_tools,
        verbose=True,
        memory=memory,
        handle_parsing_errors=True
    )
