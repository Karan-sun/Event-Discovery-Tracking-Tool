import schedule
import time
import threading
from scraper import scrape_events
from managers import save_events

class SchedulerService:
    def __init__(self):
        self.running = False
        self.jobs = []
        self.thread = None

    def job(self, city):
        print(f"Running scheduled job for {city}...")
        events = scrape_events(city)
        save_events(events)

    def start(self, city="mumbai", interval_minutes=60):
        if self.running:
            return
        
        self.running = True
        schedule.every(interval_minutes).minutes.do(self.job, city=city)
        
        self.thread = threading.Thread(target=self._run_continuously)
        self.thread.daemon = True
        self.thread.start()
        print(f"Scheduler started for {city} every {interval_minutes} minutes.")

    def _run_continuously(self):
        while self.running:
            schedule.run_pending()
            time.sleep(1)

    def stop(self):
        self.running = False
        schedule.clear()
        print("Scheduler stopped.")

scheduler_service = SchedulerService()
