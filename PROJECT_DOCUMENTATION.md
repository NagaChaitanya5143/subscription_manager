# Project Report & Technical Documentation
## T4: Subscription Manager Agent

---

### 👨‍💻 Team Information

| Student Name | Registration Number | Roll Number | Role |
| :--- | :--- | :--- | :--- |
| **K. Naga Chaitanya** | `12308076` | `9` | Team Lead / Lead Developer |
| **V. Sai Tanmai** | `12319651` | `60` | Co-Developer / Documentation & Testing |

🔗 **GitHub Repository Link**: [https://github.com/NagaChaitanya5143/subscription_manager](https://github.com/NagaChaitanya5143/subscription_manager)

---

## 📑 Executive Summary

The **Subscription Manager Agent** is an autonomous financial assistant designed to solve common personal finance challenges such as subscription creep, forgotten renewal dates, and budget overruns. Built on an agentic architecture powered by **LLaMA 3.1 8B Instruct** via the **NVIDIA NIM API**, the system tracks active recurring services, computes real-time monthly and annual financial metrics, maintains persistent memory across multi-turn user interactions, and autonomously recommends optimal cancellation strategies whenever budget thresholds are exceeded.

---

## ⚙️ System Architecture & Workflow Diagram

```
+-----------------------------------------------------------------------------------+
|                            USER INPUT / GOAL PROMPT                               |
+----------------------------------------+------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|               SubscriptionAgent Engine (LLaMA 3.1 8B Instruct)                     |
+----------------------------------------+------------------------------------------+
                                         |
         +-------------------------------+-------------------------------+
         | Tool Call Execution                                           | Tool Call Execution
         v                                                               v
+------------------------------------+                         +--------------------+
| add_subscription(name, cost, date) |                         | get_monthly_total()|
+------------------+-----------------+                         +---------+----------+
                   |                                                     |
                   +-------------------------------+---------------------+
                                                   |
                                                   v
+-----------------------------------------------------------------------------------+
|                       PERSISTENT STATE MEMORY (dict)                              |
+----------------------------------------+------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                     AUTONOMOUS BUDGET EVALUATION ENGINE                           |
+----------------------------------------+------------------------------------------+
                                         |
              +--------------------------+--------------------------+
              | Spend <= Budget                                     | Spend > Budget
              v                                                     v
+------------------------------------+             +--------------------------------+
|       Report Monthly & Yearly      |             | Generate Optimal Cancellation  |
|             Totals                 |             |          Strategy              |
+-----------------+------------------+             +----------------+---------------+
                  |                                                 |
                  +--------------------------+----------------------+
                                             |
                                             v
+-----------------------------------------------------------------------------------+
|                        FORMATTED AGENT RESPONSE TO USER                           |
+-----------------------------------------------------------------------------------+
```

---

## 💡 Problem Statement & Solution

### The Challenge
Modern consumers subscribe to numerous digital services (streaming, software, gyms, cloud storage). Managing individual renewal dates and total expenditure manually leads to:
1. **Unnoticed Over-budget Spending**: Adding a new service without calculating cumulative monthly costs.
2. **Mental Math Hallucination**: Stateless chatbots attempting to sum multi-item expenses manually often produce inaccurate totals.
3. **Lack of Renewal Visibility**: Missing upcoming billing dates.

### The Agentic Solution
Rather than operating as a simple stateless chat interface, the **Subscription Manager Agent** uses a structured **Plan-Act-Observe Loop**:
- **Deterministic Memory**: Stores all active subscriptions in a persistent dictionary memory.
- **Tool-Backed Accuracy**: Never guesses sums; relies strictly on tool outputs (`add_subscription` and `get_monthly_total`).
- **Autonomous Overage Resolution**: Detects budget violations and determines the optimal combination of non-essential services to cancel to restore financial balance.

---

## ⭐ Core Features & Capabilities

### 1. Dual Python Tool Integration
- `add_subscription(name, cost, renewal_date)`: Sanitizes cost input (handling numeric or string formats like `"$15"`), registers the subscription, and records the renewal schedule.
- `get_monthly_total()`: Calculates exact monthly totals, computes annual commitments ($12 \times \text{monthly}$), and formats active state reminders.

### 2. Multi-Turn Persistent State Memory
- Maintains memory state across multi-turn conversations so users can incrementally add subscriptions, update budget constraints, and request financial audits without losing previous inputs.

### 3. Renewal Date Reminders & Yearly Cost View (Group Add-on)
- Provides a comprehensive breakdown including renewal dates for each service alongside the projected 12-month total cost.

### 4. Smart Budget Overage & Cancellation Optimization
- When total monthly spend exceeds the user's defined budget, the agent analyzes active subscriptions and calculates the minimal or highest-cost non-essential cancellation plan to bring spending back under budget.

---

## 🛠️ Implementation Workflow & System Development

1. **Project Architecture & Modular Design**:
   - Designed a modular agentic framework separating LLM prompt logic (`agent.py`), tool execution & state memory (`tools.py`), automated verification (`main.py`), and interactive CLI (`interactive.py`).

2. **Environment & Dependency Resolution**:
   - Configured Python 3.11 runtime environment and integrated core libraries (`openai` Python SDK and `httpx` truststore) for secure API transport.

3. **LLM Tool-Calling Optimization**:
   - Adapted function calling mechanics for LLaMA 3.1 8B on NVIDIA NIM API to ensure precise turn-by-turn tool execution and response parsing.

4. **Version Control & Collaboration**:
   - Managed codebase using Git and deployed to GitHub for collaborative development.

---

## 🧪 Demonstration & Test Scenarios

The agent was verified across 3 multi-turn scenarios in `main.py`:

### Scenario 1: Initial Subscriptions Within Budget
- **User Prompt**: *"Add Netflix for $15 renewing on the 5th, and Spotify for $10 renewing on the 20th. My monthly budget is $40."*
- **Tool Executions**:
  - `add_subscription(name='Netflix', cost=15.0, renewal_date='5th')`
  - `add_subscription(name='Spotify', cost=10.0, renewal_date='20th')`
  - `get_monthly_total()`
- **Result**: Monthly Total: **$25.00** | Yearly Total: **$300.00** | Budget: **$40.00** (Within budget).

### Scenario 2: Budget Overflow & Cancellation Suggestion
- **User Prompt**: *"Add Gym Membership for $50 renewing on the 1st. My budget is $50. Check if I'm over budget and suggest what to cancel to get back under."*
- **Tool Executions**:
  - `add_subscription(name='Gym Membership', cost=50.0, renewal_date='1st')`
  - `get_monthly_total()`
- **Result**: Monthly Total: **$75.00** (Exceeds $50 budget by $25.00).
- **Agent Action**: Automatically identifies *Gym Membership ($50)* as over budget and suggests canceling it to bring monthly spending back to $25.00.

### Scenario 3: Multi-Turn Memory & Multi-Subscription Optimization
- **User Prompt**: *"Also add Disney+ for $14 renewing on the 12th. Show my total, yearly cost, renewal reminders, and best cancellation plan for my $50 budget."*
- **Tool Executions**:
  - `add_subscription(name='Disney+', cost=14.0, renewal_date='12th')`
  - `get_monthly_total()`
- **Result**: Recalled all 4 subscriptions from persistent memory. Total monthly spend: **$89.00** (Yearly Total: **$1,068.00**).
- **Agent Action**: Devised optimal plan: Cancel *Gym Membership ($50)* and *Netflix ($15)* to bring total down to **$24.00/month**, safely below the $50 budget.

---

## 🚀 How to Run & Verify Project

### 1. Clone Repository & Navigate
```bash
git clone https://github.com/NagaChaitanya5143/subscription_manager.git
cd subscription_manager
```

### 2. Automated Execution
Run the full test suite:
```bash
python main.py
```

### 3. Live Interactive Mode
Start a real-time conversation with the agent:
```bash
python interactive.py
```

---

### 📂 File Structure Overview

```text
subscription_manager/
├── agent.py                 # Core SubscriptionAgent class & LLM loop
├── tools.py                 # Tool functions & memory state dictionary
├── main.py                  # Multi-scenario automated test runner
├── interactive.py           # Real-time CLI interactive mode
├── benchmark.py             # Model latency benchmarking tool
├── demo.ipynb               # Jupyter notebook demonstration
├── PROJECT_DOCUMENTATION.md # Complete project documentation
├── README.md                # Overview & design decisions
└── .gitignore               # Git ignored files
```
