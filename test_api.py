import requests
import json
import os

API_URL = "http://127.0.0.1:8000/v1/ticket-assignment"
DATASET_FILE = "dataset.json"

def run_test():
    print("--- Starting API Test ---")
    if not os.path.exists(DATASET_FILE):
        print(f"Error: The file '{DATASET_FILE}' was not found.")
        return
    try:
        with open(DATASET_FILE, 'r') as f:
            payload = json.load(f)
        print(f"Successfully loaded '{DATASET_FILE}'.")
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    print(f"Sending data to the API endpoint: {API_URL}")
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            print("\n✅ Success! The API returned a 200 OK status.")
            results = response.json()
            print("\n--- Sample of Assignments Received ---")
            assignments = results.get("assignments", [])
            if assignments:
                for i, assignment in enumerate(assignments[:5]):
                    print(f"  Assignment {i+1}:")
                    print(f"    Ticket ID: {assignment.get('ticket_id')}")
                    print(f"    Assigned to: {assignment.get('assigned_agent_id')}")
                    print(f"    Rationale: {assignment.get('rationale')}")
                if len(assignments) > 5:
                    print(f"\n... and {len(assignments) - 5} more assignments.")
            else:
                print("The response did not contain any assignments.")
        else:
            print(f"\n❌ Error! API returned status code: {response.status_code}")
            print(f"--- Server Response ---\n{response.text}")

    except requests.exceptions.ConnectionError:
        print("\n❌ Connection Error! Make sure the FastAPI server is running.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    run_test()