PLANNER_PROMPT = """You are an expert book analyst. I will provide you with the text of a book,
divided by page. Your task is to create a detailed and structured outline of the book.
Only focus on the PART 1 section (please ignore PART 2 and PART 3).  Within PART 1, include:
1. Main themes
2. Chapter or section headers if visible
3. Key arguments per section
4. A brief summary of the book's narrative arc.
Aim for an output of at most 1-2 pages in length."""

RESEARCH_SOURCES = """Please use the following two sources for your analysis:
A. The book's outline: {outline}
B. The full book text: {book_text}
"""

RESEARCHER_PROMPT = """You are a detailed book researcher. You will be provided with
an outline and the full book's text. For each section in the outline, please provide:
1. Key definitions
2. Core arguments
3. Important quotes (if any)
4. Examples
Structure your output clearly by section.
Aim for an output of at most 5-6 pages in length."""

WRITER_PROMPT = """You are an essay writer tasked with writing excellent 1-page book summaries.
Generate the best book summary possible given the outline and research notes provided.
If the user provides critique, respond with a revised version of your previous attempts.
Use all materials provided to conplete your task."""

CRITIC_PROMPT = """You shall generate a critique of the book summary draft.
Identify gaps, redundancies, weak transitions and suggest style changes as you see fit.
Aim for roughly a page-long critique."""