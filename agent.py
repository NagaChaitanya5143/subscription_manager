"""
Subscription Manager Agent powered by LLaMA 3.1 8B on NVIDIA NIM API.
"""

import json
from openai import OpenAI
import tools

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)
MODEL = "meta/llama-3.1-8b-instruct"

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_subscription",
            "description": "Add a subscription with name, monthly cost, and optional renewal date.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "cost": {"type": "number"},
                    "renewal_date": {"type": "string"}
                },
                "required": ["name", "cost"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_monthly_total",
            "description": "Get all active subscriptions, monthly total, and yearly total.",
            "parameters": {"type": "object", "properties": {}}
        }
    }
]

TOOL_MAP = {
    "add_subscription": tools.add_subscription,
    "get_monthly_total": tools.get_monthly_total
}

class SubscriptionAgent:
    def __init__(self):
        self.messages = [
            {
                "role": "system",
                "content": (
                    "You are a Subscription Manager Agent. "
                    "You MUST call only ONE tool at a time. "
                    "Use add_subscription for new subscriptions, then get_monthly_total to check totals. "
                    "If total exceeds the budget, suggest which subscription(s) to cancel. "
                    "Always include monthly total, yearly total, and renewal dates in your reply."
                )
            }
        ]

    def run(self, user_goal: str):
        print(f"\n{'='*65}\n[USER]: {user_goal}\n{'='*65}")
        self.messages.append({"role": "user", "content": user_goal})

        while True:
            response = client.chat.completions.create(
                model=MODEL,
                messages=self.messages,
                tools=TOOLS,
                temperature=0.0,
                max_tokens=300,
                parallel_tool_calls=False
            )
            msg = response.choices[0].message

            if msg.tool_calls:
                # Restrict to single tool call to satisfy NVIDIA NIM template constraints
                tool_call = msg.tool_calls[0]
                msg.tool_calls = [tool_call]
                self.messages.append(msg)

                fn_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments) if tool_call.function.arguments else {}

                # Sanitize cost in case model passes a string like "$15"
                if fn_name == "add_subscription" and "cost" in args:
                    args["cost"] = float(str(args["cost"]).replace("$", "").strip())

                result = TOOL_MAP[fn_name](**args)
                print(f" -> [TOOL CALL] {fn_name}({args}) => {result}")

                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })
            else:
                self.messages.append(msg)
                print(f"\n[AGENT RESPONSE]:\n{msg.content}\n")
                return msg.content
