import json
from fastapi import FastAPI
from pydantic import BaseModel
from logic.ai_response_generator import get_claude_response, SYSTEM_PROMPT, STR_TOOL_OUTPUT_SP

app = FastAPI()

class Message(BaseModel):
    message: str

class ToolFormatPayload(BaseModel):
    tool_executed: str
    result: dict
    original_message: str | None = None

# 1) Tool-calling agent endpoint (HTTP Request #1 hits this)
@app.post("/chat")
async def chat_endpoint(data: Message):
    return get_claude_response(data.message, SYSTEM_PROMPT)

# 2) Tool-output formatter endpoint (HTTP Request #2 hits this)
@app.post("/format_tool_output")
async def format_tool_output_endpoint(data: ToolFormatPayload):
    # Build a single input string for the formatter model
    formatter_input = {
        "tool_executed": data.tool_executed,
        "tool_result": data.result,
        "original_message": data.original_message or ""
    }
    return get_claude_response(json.dumps(formatter_input), STR_TOOL_OUTPUT_SP)




