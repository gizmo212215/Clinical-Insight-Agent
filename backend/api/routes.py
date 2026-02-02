from fastapi import APIRouter, HTTPException
from backend.api.schemas import ChatRequest, ChatResponse
from backend.services.agent.graph import app_graph
from langchain_core.messages import HumanMessage
from backend.core.logger import get_logger


router = APIRouter()
logger = get_logger("api_routes")


@router.get("/")
async def health_check():
    logger.debug("Health check request received.")
    return {"status": "active", "module": "Clinical Agent API"}


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    logger.info(f"📩 New Question Received: {request.question}")
    try:
        inputs = {"messages": [HumanMessage(content=request.question)]}
        logger.info("🤖 Starting Agent Workflow (Reasoning & Tool Use)...")
        final_state = app_graph.invoke(inputs, config={"recursion_limit": 10})
        last_message = final_state["messages"][-1]
        content = last_message.content
        logger.debug(f"🧩 Raw Agent Response Type: {type(content)}")

        final_answer = ""
        if isinstance(content, list):
            logger.info("ℹ️ Response is a list, parsing text blocks...")
            for block in content:
                if isinstance(block, dict) and "text" in block:
                    final_answer += block["text"]
                elif isinstance(block, str):
                    final_answer += block
        else:
            final_answer = str(content)

        if not final_answer:
            logger.warning("⚠️ Agent returned an empty response!")
        else:
            logger.info(
                f"✅ Answer generated successfully ({len(final_answer)} chars)."
            )

        return ChatResponse(answer=final_answer)

    except Exception as e:
        logger.error(f"❌ Chat Endpoint Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
