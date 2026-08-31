"""
Subscription Manager Agent built with LangChain.
Utilizes ChatOpenAI, tool binding, and typed messages for a minimal agent loop.
"""

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from tools import add_subscription, get_monthly_total

TOOL_MAP = {t.name: t for t in [add_subscription, get_monthly_total]}

llm = ChatOpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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",
    model="openai/gpt-oss-20b",
    temperature=0.0,
    max_tokens=160
).bind_tools(list(TOOL_MAP.values()))

SYSTEM_PROMPT = (
    "You are a Subscription Manager Agent. "
    "Use `add_subscription` for new subscriptions, then `get_monthly_total` to inspect totals. "
    "If over budget, suggest what to cancel. "
    "Always give a short, concise response with monthly total, yearly total, and renewal reminders."
)

class SubscriptionAgent:
    def __init__(self):
        self.messages = [SystemMessage(content=SYSTEM_PROMPT)]

    def run(self, user_goal: str):
        print(f"\n{'='*65}\n[USER]: {user_goal}\n{'='*65}")
        self.messages.append(HumanMessage(content=user_goal))

        while True:
            msg = llm.invoke(self.messages)
            self.messages.append(msg)

            if not msg.tool_calls:
                safe_text = msg.content.encode("ascii", "ignore").decode("ascii") if msg.content else ""
                print(f"\n[AGENT RESPONSE]:\n{safe_text}\n")
                return msg.content

            for tc in msg.tool_calls:
                clean_name = tc["name"].split("<|")[0].split("(")[0].strip()
                tool_func = TOOL_MAP.get(clean_name)
                if tool_func:
                    result = tool_func.invoke(tc["args"])
                else:
                    result = f"Error: Tool '{clean_name}' not found."
                print(f" -> [TOOL CALL] {clean_name}({tc['args']}) => {result}")
                self.messages.append(ToolMessage(tool_call_id=tc["id"], content=str(result)))
