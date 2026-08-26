"""
Tools and Memory for Subscription Manager.
Two tools: add_subscription(name, cost) and get_monthly_total()
Includes Group of 3 add-ons: renewal-date reminders and yearly-cost view.
"""

# Memory: Remembers all active subscriptions across turns
memory = {}

def add_subscription(name: str, cost: any, renewal_date: str = "1st of next month") -> str:
    """Tool 1: Add or update a subscription with its monthly cost and renewal date."""
    # Clean cost if model passes "$15" or string
    cleaned_cost = float(str(cost).replace("$", "").strip())
    memory[name.strip()] = {
        "cost": cleaned_cost,
        "renewal_date": str(renewal_date)
    }
    return f"Added '{name}' at ${cleaned_cost:.2f}/month (Renewal Date: {renewal_date})."

def get_monthly_total() -> str:
    """Tool 2: Return all active subscriptions, monthly total, and yearly-cost view."""
    monthly_total = sum(item["cost"] for item in memory.values())
    yearly_total = monthly_total * 12
    return (
        f"Active Subscriptions: {memory} | "
        f"Monthly Total: ${monthly_total:.2f} | "
        f"Yearly Total: ${yearly_total:.2f}"
    )
