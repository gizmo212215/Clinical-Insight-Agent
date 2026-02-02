import os
import operator
from typing import TypedDict, Annotated, Sequence
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from backend.services.agent.tools import search_clinical_documents, query_clinical_sql
from backend.core.logger import get_logger

logger = get_logger("agent_core")

load_dotenv()

SYSTEM_PROMPT = """
You are an expert Clinical Trial Assistant. Your goal is to provide accurate insights to researchers and doctors.
- For statistical questions (counts, phases, dates), YOU MUST USE 'query_clinical_sql'.
- For medical details (criteria, drug info), YOU MUST USE 'search_clinical_documents'.
- If you cannot find the info, admit it. Do not hallucinate.
- Always answer in Turkish language professionally.
"""


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]


tools = [search_clinical_documents, query_clinical_sql]
try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-latest",
        temperature=0,
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        convert_system_message_to_human=True,
    )
    llm_with_tools = llm.bind_tools(tools)
    logger.info("✅ Gemini Model initialized and tools bound.")
except Exception as e:
    logger.critical(f"❌ Failed to initialize LLM: {e}", exc_info=True)
    raise e


def call_model(state):
    messages = state["messages"]
    if not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + list(messages)
    logger.info(f"🧠 Agent is reasoning on {len(messages)} messages...")
    try:
        response = llm_with_tools.invoke(messages)
        logger.debug(
            f"🗣️ Model Response generated. Tool Calls: {len(response.tool_calls)}"
        )
        return {"messages": [response]}
    except Exception as e:
        logger.error(f"❌ Error during model invocation: {e}", exc_info=True)
        raise e


def should_continue(state):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        tool_names = [t["name"] for t in last_message.tool_calls]
        logger.info(f"🛠️ Agent decided to use tool(s): {tool_names}")
        return "tools"
    logger.info("🛑 Agent has finished reasoning (Final Answer).")
    return END


try:
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", ToolNode(tools))
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges(
        "agent", should_continue, {"tools": "tools", END: END}
    )
    workflow.add_edge("tools", "agent")
    app_graph = workflow.compile()
    logger.info("🏗️ Agent Graph compiled successfully.")

except Exception as e:
    logger.critical(f"❌ Failed to build agent graph: {e}", exc_info=True)
    raise e
