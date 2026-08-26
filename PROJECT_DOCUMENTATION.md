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

## 🏗️ System Architecture & Technology Stack

```
                                +---------------------------+
                                |      User Query / CLI     |
                                +-------------+-------------+
                                              |
                                              v
                                +---------------------------+
                                |  SubscriptionAgent (LLM)  |
                                |  (LLaMA 3.1 8B Instruct)  |
                                +-------------+-------------+
                                              |
                     +------------------------+------------------------+
                     | Tool Call Request                               | Tool Result Response
                     v                                                 v
        +--------------------------+                      +--------------------------+
        |   tools.add_subscription |                      |  tools.get_monthly_total |
        +------------+-------------+                      +------------+-------------+
                     |                                                 |
                     +------------------------+------------------------+
                                              |
                                              v
                                +---------------------------+
                                |     Persistent Memory     |
                                |      dict {name, cost}    |
                                +---------------------------+
```

| Component | Specification |
| :--- | :--- |
| **Language Model** | `meta/llama-3.1-8b-instruct` |
| **API Provider** | NVIDIA NIM API (`https://integrate.api.nvidia.com/v1`) |
| **Programming Language** | Python 3.11 |
| **Client Library** | `openai` Python SDK (with `httpx` & `truststore`) |
| **Version Control** | Git & GitHub |

---

## 🛠️ Step-by-Step Setup & Development Journey

1. **Archive Extraction & Workspace Setup**:
   - Extracted `subscription_manager.rar` using `UnRAR` binary into `C:\Users\HP\.gemini\antigravity\scratch\subscription_manager`.

2. **Environment & Dependency Resolution**:
   - Installed core libraries (`openai`, `requests`).
   - Configured SSL certificate handling for Windows network environments.

3. **Single Tool-Call Adaptation**:
   - Solved NVIDIA NIM template constraint (`single tool-call per assistant turn`) by enforcing single function execution per turn in `agent.py`.

4. **Version Control & GitHub Publishing**:
   - Initialized Git repository, created `.gitignore` (excluding `.venv`, cache, binaries), committed files, and published to GitHub:
   - **Repository URL**: `https://github.com/NagaChaitanya5143/subscription_manager`

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

## 🚀 How to Run the Project

### 1. Automated Execution
Run the full test suite in terminal or VS Code:
```powershell
python main.py
```

### 2. Live Interactive Mode
Start a real-time conversation with the agent:
```powershell
python interactive.py
```

### 3. Jupyter Notebook Demo
Open [`demo.ipynb`](file:///C:/Users/HP/.gemini/antigravity/scratch/subscription_manager/demo.ipynb) in VS Code or Jupyter Lab and execute all cells.

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
├── PROJECT_DOCUMENTATION.md # Complete project documentation (This file)
├── README.md                # Overview & design decisions
└── .gitignore               # Git ignored files (.venv, cache, binaries)
```
