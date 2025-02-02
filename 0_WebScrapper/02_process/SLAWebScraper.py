import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import csv
import random

# Function to extract data from a single forecast page
def extract_forecast_data(url, expected_date):
    """Fetch and parse the avalanche forecast data, ensuring the date matches the expected date."""
    
    for attempt in range(3):
        response = requests.get(url)
        if response.status_code == 200:
            break
        elif response.status_code == 429:  # Too many requests
            wait_time = 2 ** attempt  # Exponential backoff
            print(f"Rate limited. Waiting {wait_time} seconds...")
            time.sleep(wait_time)
        else:
            print(f"Failed to fetch {url}. Status code: {response.status_code}")
            return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the div containing the forecast date
    forecaster_text_div = soup.find('div', class_='forecaster-text')

    if forecaster_text_div:
        forecast_date_elem = forecaster_text_div.find('span', class_='nowrap')
    else:
        forecast_date_elem = None  # Prevent errors if div is missing

    if forecast_date_elem:
        forecast_date_str = forecast_date_elem.text.strip()
    else:
        print(f"No forecast date found on {url}")
        return None
    
    forecast_date_str = forecast_date_elem.text.strip()
    
    try:
        forecast_date = datetime.strptime(forecast_date_str, "%A morning, %B %d, %Y").date()
    except ValueError:
        print(f"Date format mismatch on {url}: {forecast_date_str}")
        return None

    # Ensure the extracted forecast date matches the expected date
    if forecast_date != expected_date:
        print(f"Date mismatch on {url}. Expected {expected_date}, but got {forecast_date}")
        return None

    # Extract the avalanche danger message
    danger_message_elem = soup.find('div', class_='text_03 pt2')
    if not danger_message_elem:
        print(f"No danger message found for {url}")
        return None
    
    danger_message = danger_message_elem.text.strip()

    # Extract month, day, year from the forecast date
    month = forecast_date.strftime("%B")
    day = forecast_date.strftime("%d")
    year = forecast_date.strftime("%Y")

    return [month, day, year, danger_message]

# Function to iterate over specified date ranges in reverse and fetch data
def scrape_forecast_data(base_url, start_year, end_year, output_file):
    results = []

    # Iterate over each year in reverse order (2024 → 2020)
    for year in range(start_year, end_year - 1, -1):
        # Iterate from March (3) back to November (11)
        for month in [12, 11]: ### Temprorary, switch back to [4,3,2,1,12,11,10]
            for day in range(31, 0, -1):  # Iterate backward from 31 to 1
                try:
                    expected_date = datetime(year, month, day).date()
                except ValueError:
                    continue  # Skip invalid dates (e.g., Feb 30)

                url = f"{base_url}/{month}/{day}/{year}"
                data = extract_forecast_data(url, expected_date)

                if data:
                    results.append(data)
                    print(f"Scraped: {data[0]} {data[1]}, {data[2]}")  # Print progress
                
                time.sleep(1)  # Be nice to the server by adding a delay

    # Write results to CSV
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Month", "Day", "Year", "Danger Message"])  # CSV Header
        writer.writerows(results)

    print(f"\n Data successfully saved to {output_file} with {len(results)} records.")

# Example usage:
base_url = "https://utahavalanchecenter.org/forecast/salt-lake"
start_year = 2021
end_year = 2021
output_file = "/0_WebScrapper/avalanche_forecast_data.csv"

scrape_forecast_data(base_url, start_year, end_year, output_file)
