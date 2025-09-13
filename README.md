# Intelligent Support Ticket Assignment System - PyCon25 Hackathon

![Status](https://img.shields.io/badge/Status-Complete-brightgreen)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Framework](https://img.shields.io/badge/Framework-FastAPI-blueviolet)

An API-driven solution to intelligently assign support tickets by prioritizing critical issues, matching agent skills, and dynamically balancing workloads. This project is built to be a robust, stateful, and scalable microservice.

---

## 🏛️ System Architecture

Our solution is designed as a clean, stateless API service that relies on a simple file-based persistence layer to maintain agent state between requests. This makes the service scalable and easy to deploy.

```mermaid
graph LR
    subgraph "User / Client"
        A[Test Script / UI]
    end

    subgraph "Ticket Assignment Service"
        B[FastAPI Server]
        C{Assignment Logic}
    end

    subgraph "Persistence"
        D[(agent_state.json)]
    end

    A -- POST /v1/ticket-assignment with dataset.json --> B
    B -- triggers --> C
    C -- 1. Reads last known loads --> D
    C -- 2. Calculates optimal assignments --> C
    C -- 3. Saves new loads --> D
    B -- returns assignments (JSON) --> A

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