# In pipeline.py (Final Automated Version)

import requests
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
import time
import schedule # For scheduling
import yagmail # For sending emails

# --- SETUP ---
load_dotenv()
API_KEY = os.getenv("API_KEY")
CITY = "Pretoria"
DATABASE_FILE = "weather_data.csv"

# Email credentials from .env file
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")


def get_weather_data(api_key, city):
    """Fetches weather data."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def process_data(data):
    """Processes the raw JSON data."""
    if not data: return None
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "city": CITY,
        "temperature_celsius": data['main']['temp'],
        "feels_like_celsius": data['main']['feels_like'],
        "humidity_percent": data['main']['humidity'],
        "weather_description": data['weather'][0]['description'],
        "wind_speed_mps": data['wind']['speed']
    }

def save_data_to_csv(data, filename):
    """Saves data by appending to a CSV."""
    df = pd.DataFrame([data])
    try:
        file_exists = os.path.isfile(filename)
        df.to_csv(filename, mode='a', header=not file_exists, index=False)
    except IOError as e:
        print(f"Error saving data: {e}")

def send_email_report(data):
    """Sends an email summary of the weather data."""
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("Email credentials not set. Skipping email.")
        return
        
    try:
        yag = yagmail.SMTP(SENDER_EMAIL, SENDER_PASSWORD)
        
        subject = f"Daily Weather Report for {CITY} - {datetime.now().strftime('%Y-%m-%d')}"
        
        # Create a nice HTML body for the email
        body = f"""
        <html>
        <body>
            <h2>Today's Weather Update for {data['city']}:</h2>
            <p><strong>Temperature:</strong> {data['temperature_celsius']:.1f}°C</p>
            <p><strong>Feels Like:</strong> {data['feels_like_celsius']:.1f}°C</p>
            <p><strong>Humidity:</strong> {data['humidity_percent']}%</p>
            <p><strong>Conditions:</strong> {data['weather_description'].title()}</p>
            <p><strong>Wind Speed:</strong> {data['wind_speed_mps']} m/s</p>
            <p>This report was generated automatically by the Python Weather Pipeline.</p>
        </body>
        </html>
        """
        
        yag.send(
            to=RECEIVER_EMAIL,
            subject=subject,
            contents=body
        )
        print(f"Email report sent successfully to {RECEIVER_EMAIL}!")
    except Exception as e:
        print(f"Error sending email: {e}")

# --- THE MAIN JOB FUNCTION ---
def job():
    """The main function that defines the pipeline's single run."""
    print(f"--- Running pipeline job at {datetime.now()} ---")
    weather_json = get_weather_data(API_KEY, CITY)
    if weather_json:
        processed_data = process_data(weather_json)
        if processed_data:
            save_data_to_csv(processed_data, DATABASE_FILE)
            send_email_report(processed_data)
    print("--- Job finished. ---")


# --- SCHEDULING LOGIC ---
if __name__ == "__main__":
    print("--- Starting Automated Weather Pipeline Scheduler ---")
    
    # Schedule the job to run every day at a specific time, e.g., "08:00"
    schedule.every().day.at("08:00").do(job)
    
    # You can also use other schedules for testing:
    # schedule.every(10).seconds.do(job)
    # schedule.every().hour.do(job)
    
    # Run the initial job once right away without waiting
    job() 
    
    # This loop keeps the script running forever to check the schedule
    while True:
        schedule.run_pending()
        time.sleep(1)