import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.services.agent.graph import app_graph
from langchain_core.messages import HumanMessage
from backend.core.logger import get_logger

logger = get_logger("script_cli_chat")


def chat_loop():
    print("\n💬 CLI CHAT MODE (Type 'exit' or 'q' to quit)")
    print("---------------------------------------------")

    while True:
        try:
            user_input = input("\n👤 You: ")
            if user_input.lower() in ["exit", "quit", "q"]:
                print("👋 Exiting...")
                break

            logger.info(f"Testing Question: {user_input}")
            inputs = {"messages": [HumanMessage(content=user_input)]}
            final_state = app_graph.invoke(inputs, config={"recursion_limit": 10})
            answer = final_state["messages"][-1].content
            print(f"🤖 Agent: {answer}")

        except Exception as e:
            logger.error(f"❌ Error: {e}", exc_info=True)
            print("❌ An error occurred. Check logs.")


if __name__ == "__main__":
    chat_loop()
