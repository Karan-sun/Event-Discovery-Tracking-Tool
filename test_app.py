import requests
import time

BASE_URL = "http://127.0.0.1:5000/api"

def test_api():
    print("Testing API...")
    
    # 1. Test Scrape
    print("1. Triggering Scrape for Mumbai...")
    try:
        res = requests.post(f"{BASE_URL}/scrape", json={"city": "mumbai"})
        if res.status_code == 200:
            print("   Success!", res.json()['message'])
        else:
            print("   Failed!", res.text)
    except Exception as e:
        print(f"   Connection failed: {e}")
        return

    # 2. Get Events
    print("2. Fetching Events...")
    res = requests.get(f"{BASE_URL}/events")
    events = res.json()
    print(f"   Got {len(events)} events.")
    if len(events) > 0:
        print(f"   Sample: {events[0]['name']}")

    # 3. Test Scheduler
    print("3. Starting Scheduler...")
    requests.post(f"{BASE_URL}/scheduler/start", json={"city": "pune"})
    
    print("4. Stopping Scheduler...")
    requests.post(f"{BASE_URL}/scheduler/stop")
    
    print("Tests Completed.")

if __name__ == "__main__":
    time.sleep(3) 
    test_api()
