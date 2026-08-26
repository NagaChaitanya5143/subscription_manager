"""
Demo runner executing SubscriptionAgent across 3 multi-turn scenarios.
Demonstrates:
- 2 tools: add_subscription(name, cost) and get_monthly_total()
- Memory retention across turns
- Agentic cancellation suggestions when over budget
- Group of 3 add-on: renewal-date reminders and yearly-cost view
"""

from agent import SubscriptionAgent
import tools

def main():
    tools.memory.clear()
    agent = SubscriptionAgent()

    # Scenario 1: Initial subscriptions within budget + renewal dates + yearly cost view
    agent.run("Add Netflix for $15 renewing on the 5th, and Spotify for $10 renewing on the 20th. My monthly budget is $40.")

    # Scenario 2: Budget overflow -> Agent calls tools, detects overage, and suggests what to cancel
    agent.run("Add Gym Membership for $50 renewing on the 1st. My budget is $50. Check if I'm over budget and suggest what to cancel to get back under.")

    # Scenario 3: Multi-turn memory test -> Recalls memory, adds Disney+, shows renewal reminders, yearly cost, and cancellation strategy
    agent.run("Also add Disney+ for $14 renewing on the 12th. Show my total, yearly cost, renewal reminders, and best cancellation plan for my $50 budget.")

if __name__ == "__main__":
    main()
