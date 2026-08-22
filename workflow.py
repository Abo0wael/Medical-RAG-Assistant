from langgraph import graph

from agents import *
from models import State
from langgraph.graph import START, END, StateGraph


class Workflow:
    def __init__(self):
        self.rewrite_query = rewitten_query_agent
        self.response_agent = response_agent
        self.retriever_agent = retriever_agent

    def build_graph(self):
        graph = StateGraph(State)

        # build nodes
        graph.add_node("rewritten_query_agent", self.rewrite_query)
        graph.add_node("response_agent", self.response_agent)
        graph.add_node("retriever_agent", self.retriever_agent)

        # connection between nodes
        graph.add_edge(START, "rewritten_query_agent")
        graph.add_edge("rewritten_query_agent", "retriever_agent")
        graph.add_edge("retriever_agent", "response_agent")
        graph.add_edge("response_agent", END)

        return graph.compile()

    def run(self, initial_state: State) -> State:
        graph = self.build_graph()
        result = graph.invoke(initial_state)
        return result