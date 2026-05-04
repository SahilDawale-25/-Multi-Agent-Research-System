from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
from langchain_ollama import ChatOllama
from dotenv import load_dotenv

load_dotenv()

# =========================
# Model Setup
# =========================

llm = ChatOllama(model="llama3.1", temperature=0.3)

# =========================
# Search Agent
# =========================

def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
        system_prompt=(
            "You are a research search agent. "
            "Find relevant and recent information with URLs."
        )
    )

# =========================
# Reader Agent
# =========================

def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url],
        system_prompt=(
            "You are a reader agent. "
            "Open URLs and extract useful clean content."
        )
    )

# =========================
# Writer Chain
# =========================

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer."),
    ("human", """
Write a detailed research report.

Topic:
{topic}

Research:
{research}

Structure:
- Introduction
- Key Findings (min 3)
- Conclusion
- Sources
"""),
])

writer_chain = writer_prompt | llm | StrOutputParser()

# =========================
# Critic Chain
# =========================

critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a strict research critic."),
    ("human", """
Review the report:

{report}

Format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

Verdict:
...
"""),
])

critic_chain = critic_prompt | llm | StrOutputParser()