
import pandas as pd
import re
import json
from fastapi import FastAPI
from typing import Dict, Any
import os
import threading

# --- 1. State Management & Configuration ---

AGENT_STATE_FILE = "agent_state.json"
# A lock to prevent race conditions when reading/writing the state file
file_lock = threading.Lock()

def load_agent_state():
    """Loads the current state of agents (especially their load) from a file."""
    with file_lock:
        if not os.path.exists(AGENT_STATE_FILE):
            return {}  # Return empty dict if state file doesn't exist
        try:
            with open(AGENT_STATE_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

def save_agent_state(agent_data: dict):
    """Saves the updated state of agents to a file."""
    with file_lock:
        with open(AGENT_STATE_FILE, 'w') as f:
            json.dump(agent_data, f, indent=2)

# --- 2. Core Logic & Mappings ---

SKILL_KEYWORDS = {
    'Networking': ['network', 'networking', 'firewall', 'vpn', 'routing', 'switch', 'cisco', 'dns'], 'Linux_Administration': ['linux', 'ubuntu', 'samba', 'server'], 'Cloud_AWS': ['aws', 'ec2', 's3', 'amazon web services'], 'VPN_Troubleshooting': ['vpn', 'tunnel', 'disconnection', 'authentication error'], 'Hardware_Diagnostics': ['hardware', 'laptop', 'desktop', 'monitor', 'port', 'boot', 'fan', 'battery', 'memory', 'disk space'], 'Windows_Server_2022': ['windows server', 'active directory'], 'Active_Directory': ['active directory', 'ad', 'user account', 'group policy', 'sso', 'saml'], 'Virtualization_VMware': ['vmware', 'virtualization', 'vm'], 'Software_Licensing': ['license', 'licensing', 'adobe', 'visio', 'tableau'], 'Network_Security': ['firewall', 'security', 'phishing', 'malware', 'antivirus', 'siem', 'ids'], 'Database_SQL': ['sql', 'database', 'query', 'backup', 'db'], 'Firewall_Configuration': ['firewall', 'ruleset', 'port'], 'Identity_Management': ['identity', 'sso', 'saml', 'account', 'login'], 'SaaS_Integrations': ['saas', 'salesforce', 'jira', 'trello', 'integration'], 'Microsoft_365': ['microsoft 365', 'm365', 'outlook', 'teams', 'sharepoint', 'onedrive'], 'SharePoint_Online': ['sharepoint'], 'PowerShell_Scripting': ['powershell', 'scripting'], 'Endpoint_Management': ['endpoint', 'mdm', 'compliant'], 'Windows_OS': ['windows', 'os', 'boot'], 'Cloud_Azure': ['azure', 'app service'], 'DevOps_CI_CD': ['devops', 'ci/cd', 'jenkins', 'docker'], 'Kubernetes_Docker': ['kubernetes', 'docker', 'container'], 'Python_Scripting': ['python', 'script'], 'Mac_OS': ['mac', 'macos', 'macbook'], 'Printer_Troubleshooting': ['printer', 'printing'], 'Laptop_Repair': ['laptop', 'repair', 'hardware'], 'Network_Cabling': ['cabling', 'cable', 'rack'], 'Voice_VoIP': ['voip', 'phone', 'voice'], 'Network_Monitoring': ['monitoring', 'network performance'], 'Switch_Configuration': ['switch', 'cisco'], 'Routing_Protocols': ['routing', 'protocol'], 'Cisco_IOS': ['cisco'], 'Endpoint_Security': ['endpoint', 'security', 'antivirus', 'malware'], 'Antivirus_Malware': ['antivirus', 'malware', 'trojan', 'virus', 'spyware'], 'Phishing_Analysis': ['phishing', 'email', 'security'], 'Security_Audits': ['audit', 'security'], 'SIEM_Logging': ['siem', 'log', 'logging'], 'ETL_Processes': ['etl'], 'Data_Warehousing': ['data warehouse'], 'PowerBI_Tableau': ['powerbi', 'tableau'], 'API_Troubleshooting': ['api'], 'Web_Server_Apache_Nginx': ['apache', 'nginx', 'web server', '502', '503', '404'], 'DNS_Configuration': ['dns'], 'SSL_Certificates': ['ssl', 'certificate']
}
URGENCY_KEYWORDS = {
    'critical': 5, 'outage': 5, 'down': 5, 'unavailable': 5, 'breach': 5, 'urgent': 4, 'security': 4, 'vulnerable': 4, 'high-priority': 3, 'affecting': 3, 'intermittent': 2, 'slow': 2, 'request': 1, 'low-priority': 1
}

def generate_assignments(data: Dict[str, Any]) -> list:
    agents_df = pd.DataFrame(data['agents'])
    tickets_df = pd.DataFrame(data['tickets'])
    agents_df['skills_dict'] = agents_df['skills'].apply(lambda x: x if isinstance(x, dict) else {})

    # Load the last known state for agent loads
    agent_state = load_agent_state()
    initial_agent_loads = {agent['agent_id']: agent['current_load'] for agent in data['agents']}
    # If a state file exists, override the initial loads with the saved loads
    if agent_state and 'agents' in agent_state:
        saved_loads = {agent['agent_id']: agent['current_load'] for agent in agent_state['agents']}
        initial_agent_loads.update(saved_loads)
    
    agent_loads = initial_agent_loads.copy()

    def calculate_priority(row):
        text = (row['title'] + ' ' + row['description']).lower()
        score = sum(score for keyword, score in URGENCY_KEYWORDS.items() if keyword in text)
        return score + (row['creation_timestamp'] / 1e10)
    
    tickets_df['priority'] = tickets_df.apply(calculate_priority, axis=1)
    sorted_tickets = tickets_df.sort_values(by='priority', ascending=False)
    
    assignments = []
    for _, ticket in sorted_tickets.iterrows():
        ticket_text = (ticket['title'] + ' ' + ticket['description']).lower()
        agent_scores = {}
        for _, agent in agents_df.iterrows():
            if agent['availability_status'] != 'Available':
                continue
            skill_score = 0
            for skill, keywords in SKILL_KEYWORDS.items():
                if skill in agent['skills_dict'] and any(re.search(r'\b' + re.escape(kw) + r'\b', ticket_text) for kw in keywords):
                    skill_score += agent['skills_dict'][skill]
            load_score = (1 / (1 + agent_loads.get(agent['agent_id'], 0))) * 10
            experience_score = agent['experience_level'] * 0.1
            total_score = (skill_score * 0.7) + (load_score * 0.3) + experience_score
            agent_scores[agent['agent_id']] = total_score
        
        if agent_scores:
            best_agent_id = max(agent_scores, key=agent_scores.get)
            agent_loads[best_agent_id] += 1
            best_agent_details = agents_df[agents_df['agent_id'] == best_agent_id].iloc[0]
            rationale = (f"Assigned to {best_agent_details['name']} due to a high suitability score. Key factors: Relevant skills, current workload of {agent_loads[best_agent_id]-1}, and experience level.")
            assignments.append({"ticket_id": ticket['ticket_id'], "assigned_agent_id": best_agent_id, "rationale": rationale})
    
    # Save the final state of agent loads for the next run
    final_agent_states = []
    for _, agent in agents_df.iterrows():
        agent_id = agent['agent_id']
        final_agent_states.append({"agent_id": agent_id, "name": agent['name'], "current_load": agent_loads.get(agent_id, agent['current_load'])})
    save_agent_state({"agents": final_agent_states})

    return assignments

# --- 3. FastAPI Web Application ---

app = FastAPI(title="PyCon25 Hackathon: Ticket Assignment API", description="An API to intelligently assign support tickets to agents.", version="1.0.0")

@app.post("/v1/ticket-assignment", tags=["Ticket Assignment"])
def run_assignment(payload: Dict[str, Any]):
    """Accepts the full `dataset.json` as input and returns the optimal ticket assignments."""
    try:
        assignments = generate_assignments(payload)
        return {"assignments": assignments}
    except Exception as e:
        return {"error": str(e)}

@app.get("/", tags=["Health Check"])
def read_root():
    return {"status": "ok", "message": "Ticket Assignment API is running. Go to /docs to test the endpoint."}