# Automated Daily Weather Report Pipeline

## Project Overview

This project is a fully automated data pipeline built in Python that fetches live weather data from the OpenWeatherMap API, stores it in a persistent CSV database, and sends a daily summary report via email.

This project demonstrates skills in data engineering, API integration, automation, and secure credential management. It shows the ability to build a system that runs independently on a schedule to gather and report on real-time data.

## Key Features

- **Live Data Ingestion:** Connects to the OpenWeatherMap API to pull current weather data for any specified city.
- **Data Persistence:** Appends new data to a `weather_data.csv` file, creating a historical time-series dataset with each run.
- **Automated Reporting:** Programmatically sends a formatted HTML email summary of the latest weather data.
- **Task Scheduling:** Uses the `schedule` library to automate the entire pipeline, running it at a pre-defined time every day.
- **Secure Key Management:** Utilizes a `.env` file and the `python-dotenv` library to keep sensitive API keys and passwords separate from the source code, following security best practices.

## Tech Stack

- **Language:** Python
- **Libraries:**
    - **requests:** For making HTTP requests to the API.
    - **pandas:** For structuring and saving the data.
    - **schedule:** For automating the script execution.
    - **yagmail:** For sending email reports.
    - **python-dotenv:** For managing environment variables.

## Setup and Usage

1.  Clone this repository.
2.  Create a virtual environment and install dependencies:
    ```bash
    pip install -r requirements.txt 
    # (Or: pip install requests pandas schedule yagmail python-dotenv)
    ```
3.  Create a `.env` file in the root directory by copying the `sample.env` file.
4.  Fill in your own keys and email details in the `.env` file. You will need to generate a [Google App Password](https://support.google.com/accounts/answer/185833) for the `SENDER_PASSWORD`.
5.  Customize the `CITY` variable and the schedule time in `pipeline.py` as desired.
6.  Run the pipeline:
    ```bash
    python pipeline.py
    ```
    The script will run once immediately and then continue to run in the background according to the schedule. Press `CTRL+C` to stop.
