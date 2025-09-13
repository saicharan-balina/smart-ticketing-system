README.md
# Intelligent Support Ticket Assignment System - PyCon25 Hackathon

Welcome to the Intelligent Support Ticket Assignment System, a robust and scalable solution built for the PyCon25 Hackathon. This project provides an API-driven service to optimally route support tickets to the best-suited agents, balancing workload and prioritizing critical issues.

## 📋 Project Overview

This system addresses the challenge of efficiently assigning support tickets in a helpdesk environment. It processes a list of agents (with their skills and current workload) and a queue of tickets, then generates an optimal assignment plan.

Our solution is built as a scalable web service that can be easily integrated into a larger helpdesk ecosystem.

## ✨ Key Features & Technical Highlights

Our implementation stands out by focusing on a realistic and robust system design:

**1. Multi-Factor Scoring Algorithm:** We don't just match keywords. Each assignment is a calculated decision based on a weighted score that considers:
    *   **🎯 Skill Match Score:** A comprehensive mapping of keywords within the ticket's title and description to the agent's specific skills and their proficiency level.
    *   **⚖️ Dynamic Load Balancing:** The system heavily favors agents with a lower current workload. The agent's load is updated *in-memory* after each assignment, ensuring fair distribution across the entire batch.
    *   **🔥 Urgency-Based Prioritization:** Before assignment, tickets are pre-sorted based on urgency keywords (e.g., "outage," "critical," "down"). This ensures that business-critical issues are always handled first.
    *   ** Tie-Breaker:** An agent's experience level is used as a final tie-breaker for otherwise equal scores.

**2. Stateful & Persistent Service:** Unlike a simple script, our service maintains the state of agent workloads between API calls.
    *   We use a lightweight file-based persistence (`agent_state.json`) to store the latest workload of each agent after a batch of assignments is processed.
    *   This simulates a real-world scenario where agent availability is continuous, making our load balancing far more effective over time.

**3. Scalable API-First Design:**
    *   The entire logic is wrapped in a high-performance **FastAPI** web server.
    *   This API-first approach means our assignment logic can be easily called by other services, a front-end UI, or an event-driven system (e.g., when a new ticket is created).
    *   FastAPI also provides **auto-generating, interactive documentation** (`/docs`), making our service incredibly easy to test and demonstrate.

## 🛠️ Tech Stack

*   **Language:** Python 3
*   **API Framework:** FastAPI
*   **Data Handling:** Pandas
*   **Server:** Uvicorn

## 🚀 How to Run the Project

Follow these steps to get the service running locally.

**1. Clone the Repository:**
```bash
git clone [your-repo-url]
cd [your-repo-folder]