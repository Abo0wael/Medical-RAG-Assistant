from typing import Annotated, List, Optional
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    user_input: str
    messages: Annotated[List,add_messages]
    content: Optional[List[str]]
    response: Optional[str]
    rewritten_query: Optional[str]
    system_prompt: Optional[str]
    user_prompt_template: Optional[str]
    selected_model: Optional[str]