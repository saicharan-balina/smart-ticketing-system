# Intelligent Support Ticket Assignment System - PyCon25 Hackathon

![Status](https://img.shields.io/badge/Status-Complete-brightgreen)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Framework](https://img.shields.io/badge/Framework-FastAPI-blueviolet)

A smart, API-driven solution for assigning support tickets. It prioritizes critical issues, matches tickets to the right agent skills, and ensures a balanced workload across the team.

---

## ⚙️ How It Works: The Assignment Logic

Our system processes tickets in a logical, multi-step flow to find the best agent for each job.

**Ticket Processing Flow:**

`Start` -> `Load Agent Workloads from File` -> `Score Ticket Urgency` -> `Sort Tickets (Urgent First)` -> `Assign Tickets One-by-One` -> `Update Agent Workloads in Real-Time` -> `Save Final Workloads to File` -> `End`

**Finding the Best Agent (for each ticket):**

`Score Agent's Skills` + `Score Agent's Current Load` + `Score Agent's Experience` -> **`Final Suitability Score`**

The agent with the highest score gets the ticket.

## 🚀 How the System Handles a Request

The entire solution is wrapped in a web API, making it a scalable microservice.

**API Request Flow:**

`Test Script (or UI)` -> `POST Request with Ticket Data` -> `FastAPI Server` -> `Assignment Logic Runs` -> `Returns Assignments as JSON` -> `Test Script Shows Results`

---

## ✨ Key Features

*   **🧠 Smart Scoring:** We don't just match keywords. Our algorithm calculates a weighted score based on:
    *   **Skill Match:** How well the ticket's content matches an agent's skills.
    *   **Load Balancing:** Agents with less work are strongly preferred.
    *   **Urgency:** Critical issues are always handled first.

*   **💾 Stateful Workloads:** The system remembers agent workloads between API calls by saving them to a local `agent_state.json` file. This ensures the load balancing is fair and effective over time.

*   **⚡ Fast & Modern API:** Built with **FastAPI**, our solution is a high-performance web service. It comes with automatic, interactive API documentation for easy testing and demos.

---

## 🛠️ How to Run and Test

Get the project running in just a few steps.

### 1. Setup
First, clone the repository and install the necessary packages.
```bash
# Clone the repo
git clone [your-repo-url]
cd [your-repo-folder]

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

uvicorn main:app --reload```
The server will be live at `http://127.0.0.1:8000`.

### 3. Test the Service

**Option A: Interactive API Docs (Best for a Demo)**
1.  Open your browser to **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**.
2.  Expand the `POST /v1/ticket-assignment` endpoint.
3.  Click "**Try it out**", paste your `dataset.json` content into the request body, and click "**Execute**".

**Option B: Test Script**
1.  Keep the server running.
2.  Open a **new terminal** and run:
    ```bash
    python test_api.py
    ```
The script will call the API and print a summary of the results.

---

## 🔮 Future Improvements

*   **Smarter Analysis:** Use an AI model to understand ticket text more deeply.
*   **Database Integration:** Switch from a JSON file to a SQLite database for better data management.
*   **Real-time Processing:** Use WebSockets to handle tickets as soon as they are created.