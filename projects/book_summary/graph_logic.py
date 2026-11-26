# load main modules
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END
from typing import TypedDict
from langgraph.checkpoint.memory import MemorySaver

# load the prompts
from book_prompts import PLANNER_PROMPT, RESEARCHER_PROMPT, RESEARCH_SOURCES, WRITER_PROMPT, CRITIC_PROMPT

# load LLM
model_name = os.getenv('MODEL_NAME', 'gpt-6-luna')
llm = ChatOpenAI(model=model_name)


# Define the shared state that flows between agents 
class BookState(TypedDict):
    pages: list             # raw page documents
    book_text: str
    outline: str            # output from PLANNER
    research_notes: str     # output from RESEARCHER
    draft: str              # output from WRITER
    critique: str           # output from CRITIC
    revision_count: str     # keeps track of numbers of draft revisions


# create 'book_text' as its own preparatory node
def prep_node(state: BookState) -> dict:
    """Converts raw pages into a single formatted string."""
    book_text = "\n\n".join(
        [f"--- PAGE {i+1} ---\n{p.page_content}" for i, p in enumerate(state["pages"])]
    )
    return {"book_text": book_text}

# Wrap PLANNER logic as node function
def planner_node(state: BookState) -> dict:
    """Takes pages from state and produces an outline"""

    response = llm.invoke([
        SystemMessage(content=PLANNER_PROMPT),
        HumanMessage(content=state['book_text'])
    ])
    return {'outline': response.content}    # partial state update

# Wrap RESEARCHER logic as node function
def researcher_node(state: BookState) -> dict:
    """Takes the outline and the full book text. Extracts key insights from each section."""

    user_prompt = RESEARCH_SOURCES.format(
        outline=state['outline'],
        book_text=state['book_text']
    )

    response = llm.invoke([
        SystemMessage(content=RESEARCHER_PROMPT),
        HumanMessage(content=user_prompt)
    ])
    return {'research_notes': response.content}

def writer_node(state: BookState) -> dict:
    """Takes outline + research notes to generate a 1-page summary of the book."""
    sources_for_writer = [
        f"OUTLINE:\n{state['outline']}",
        f"RESEARCH NOTES:\n{state['research_notes']}"
    ]

    count = state.get('revision_count', 0)
    if state.get('critique'):
        sources_for_writer.append(f"PREVIOUS DRAFT:\n{state['draft']}")
        sources_for_writer.append(f"CRITIQUE:\n{state['critique']}")
        count += 1

    sources_all = "\n\n".join(sources_for_writer)

    notes_prompt = """Please use the following sources to write the summary: {materials}"""
    user_prompt = notes_prompt.format(materials=sources_all)

    response = llm.invoke([
        SystemMessage(content=WRITER_PROMPT),
        HumanMessage(content=user_prompt)
    ])

    return {'draft': response.content, 'revision_count': count}

def critic_node(state: BookState) -> dict:
    """Takes the draft from the writer and critiques it offering suggestions for improvement."""

    sources_for_critic = [
        f"RESEARCH NOTES\n{state['research_notes']}",
        f"DRAFT\n{state['draft']}"
    ]
    sources_all = "\n\n".join(sources_for_critic)

    sources_prompt = """Please use the following sources to generate your critique: {sources}"""
    user_prompt = sources_prompt.format(sources=sources_all)
    
    response = llm.invoke([
        SystemMessage(content=CRITIC_PROMPT),
        HumanMessage(content=user_prompt)
    ])
    return {'critique': response.content}

def should_revise(state: BookState) -> str:
    """DECISION BRANCH: send draft to CRITIC or END?"""
    if state.get('revision_count', 0) >= 1:
        return 'end'
    return 'critic'


# Set up the main canvas
workflow = StateGraph(BookState)

# draw the boxes
workflow.add_node('prep', prep_node)
workflow.add_node('planner', planner_node)
workflow.add_node('researcher', researcher_node)
workflow.add_node('writer', writer_node)
workflow.add_node('critic', critic_node)

# draw starting point and the arrows
workflow.set_entry_point('prep')
workflow.add_edge('prep', 'planner')
workflow.add_edge('planner', 'researcher')
workflow.add_edge('researcher', 'writer')
workflow.add_edge('critic', 'writer')

# conditional edge
workflow.add_conditional_edges(
    'writer',                           # source node
    should_revise,                      # function that decides to direct to
    {'critic': 'critic', 'end': END}    # one of 2 outgoing nodes
)

# compile the graph
memory = MemorySaver()
flowchart = workflow.compile(checkpointer=memory)


