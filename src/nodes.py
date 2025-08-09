from langgraph.graph import START, END, StateGraph, MessagesState
from chains import responder_chain, revisor_chain
from schemas import AnswerQuestionSchema, RevisionSchema, OverAllState
from langchain_community.tools.tavily_search import TavilySearchResults


def responder(state:AnswerQuestionSchema):
    response = responder_chain.invoke({"messages": state["messages"]})
    return response


def search_web(state: OverAllState):
    
    """ Retrieve docs from web search """

    # Search
    tavily_search = TavilySearchResults(max_results=3)
    
    # Search
    search_docs = tavily_search.invoke(state["search_queries"])

     # Format
    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
            for doc in search_docs
        ]
    )

    return {"context": [formatted_search_docs]} 


def revisor(state: OverAllState):
    pass