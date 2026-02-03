from flask import Flask, render_template, jsonify, request, send_file
from scraper import scrape_events
from managers import save_events, get_all_events
from scheduler_service import scheduler_service
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/scrape', methods=['POST'])
def trigger_scrape():
    city = request.json.get('city', 'mumbai')
    try:
        events = scrape_events(city)
        save_events(events)
        return jsonify({"success": True, "message": f"Scraped {len(events)} events for {city}", "events": events})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/events', methods=['GET'])
def get_events():
    events = get_all_events()
    return jsonify(events)

@app.route('/api/download')
def download_excel():
    if os.path.exists("events.xlsx"):
        return send_file("events.xlsx", as_attachment=True)
    return "No file found", 404

@app.route('/api/scheduler/start', methods=['POST'])
def start_scheduler():
    city = request.json.get('city', 'mumbai')
    scheduler_service.start(city=city, interval_minutes=60) # Default 1 hour
    return jsonify({"success": True, "message": "Scheduler started"})

@app.route('/api/scheduler/stop', methods=['POST'])
def stop_scheduler():
    scheduler_service.stop()
    return jsonify({"success": True, "message": "Scheduler stopped"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
