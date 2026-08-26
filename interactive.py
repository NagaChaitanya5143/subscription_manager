"""
Interactive CLI for testing Subscription Manager Agent.
Run this script to talk to your Subscription Agent live.
"""

from agent import SubscriptionAgent
import tools

def interactive():
    print("=" * 60)
    print(" Subscription Manager Agent - Interactive Mode")
    print(" Type 'exit' or 'quit' to stop.")
    print(" Type 'reset' to clear memory.")
    print("=" * 60)

    tools.memory.clear()
    agent = SubscriptionAgent()

    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                print("Exiting. Goodbye!")
                break
            if user_input.lower() == "reset":
                tools.memory.clear()
                agent = SubscriptionAgent()
                print("Memory reset.")
                continue

            agent.run(user_input)
        except (KeyboardInterrupt, EOFError):
            print("\nExiting. Goodbye!")
            break

if __name__ == "__main__":
    interactive()
