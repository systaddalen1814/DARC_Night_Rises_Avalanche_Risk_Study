from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime
import time
import os
from bs4 import BeautifulSoup


class CAICScraper:
    def __init__(self, url, zone_name):
        self.url = url
        self.zone_name = zone_name
        self.risk_mapping = {
            'low': 1,
            'moderate': 2,
            'considerable': 3,
            'high': 4,
            'extreme': 5
        }
        self.risk_data = {1: [], 2: [], 3: [], 4: [], 5: []}

    def setup_driver(self):
        chrome_options = Options()
        # chrome_options.add_argument('--headless')  # Uncomment to run without browser window
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--ignore-certificate-errors')
        
        # Set up Chrome service with automated driver installation
        service = Service(ChromeDriverManager().install())
        
        # Initialize the driver
        return webdriver.Chrome(service=service, options=chrome_options)

    def extract_data(self, driver):
        try:
            # Wait for the page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.font-bold.text-lg"))
            )

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Get the date element using the exact class structure shown in Image 1
            date_element = soup.find('div', class_='font-bold text-lg')
            if date_element:
                date_text = date_element.get_text().strip()
                print(f"Found date: {date_text}")
            else:
                print("Date element not found")
                return None
            
            # Get the risk element using the structure shown in Image 2
            risk_container = soup.find('div', class_='relative flex items-center pl-4 sm:pl-8')
            if risk_container:
                # Find any p tag within the container
                risk_text = risk_container.find('p', class_='w-full text-sm')
                if risk_text:
                    # Get just the "Moderate" text
                    risk_parts = risk_text.get_text().strip().split()
                    risk_value = next((part for part in risk_parts if part.lower() in self.risk_mapping), None)
                    if risk_value:
                        risk_text = risk_value.lower()
                        print(f"Found risk level: {risk_text}")
                    else:
                        print("Could not extract risk value from text")
                        return None
                else:
                    print("Risk paragraph not found")
                    return None
            else:
                print("Risk container not found")
                return None

            risk_level = self.risk_mapping.get(risk_text, None)

            if risk_level is None:
                print(f"Unknown risk level: {risk_text}")
                return None

            # Get description text
            description_container = soup.find('div', class_='sm:mt-4')
            if description_container:
                description_paragraphs = description_container.find_all('p')
                description = '\n'.join([p.text.strip() for p in description_paragraphs if p.text.strip()])
            else:
                description = ""

            # Convert date text to datetime
            try:
                date = datetime.strptime(date_text, '%A, %b %d')
                current_year = datetime.now().year
                date = date.replace(year=current_year)
            except ValueError as e:
                print(f"Error parsing date: {e}")
                return None

            return {
                'date': date,
                'risk_level': risk_level,
                'description': description
            }
        except Exception as e:
            print(f"Error extracting data: {e}")
            return None

    def click_back_button(self, driver):
        try:
            # Wait for the button to be present and clickable
            wait = WebDriverWait(driver, 10)
            back_button = wait.until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR,
                    "button[class*='text-primary'][class*='bg-white']"
                ))
            )

            # Scroll the button into view
            driver.execute_script("arguments[0].scrollIntoView(true);", back_button)
            time.sleep(1)

            try:
                # Try regular click first
                back_button.click()
            except:
                # If regular click fails, try JavaScript click
                driver.execute_script("arguments[0].click();", back_button)

            time.sleep(2)  # Wait for page to update
            print("Successfully clicked back button")
            return True

        except Exception as e:
            print(f"Error clicking back button: {e}")
            # Debug information
            try:
                buttons = driver.find_elements(By.TAG_NAME, "button")
                print(f"Found {len(buttons)} buttons on page:")
                for btn in buttons:
                    print(f"Button classes: {btn.get_attribute('class')}")
            except:
                pass
            return False

    def save_to_csvs(self):
        try:
            # Get current working directory
            current_dir = os.getcwd()
            print(f"Current working directory: {current_dir}")
            
            # Create avalanche_data directory in current working directory
            output_dir = os.path.join(current_dir, "avalanche_data")
            print(f"Attempting to create/access directory: {output_dir}")

            # Create directory if it doesn't exist
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                print(f"Created new directory: {output_dir}")
            else:
                print(f"Using existing directory: {output_dir}")

            # Save data for each risk level
            for risk_level, data in self.risk_data.items():
                if data:
                    try:
                        df = pd.DataFrame(data)
                        filename = os.path.join(output_dir, f"avalanche_risk_CAIC_{risk_level}.csv")
                        df.to_csv(filename, index=False)
                        print(f"Successfully saved {len(data)} records to {filename}")
                        
                        # Verify file was created
                        if os.path.exists(filename):
                            print(f"Verified file exists: {filename}")
                            print(f"File size: {os.path.getsize(filename)} bytes")
                        else:
                            print(f"Warning: File was not created: {filename}")
                    except Exception as e:
                        print(f"Error saving risk level {risk_level} data: {e}")
                else:
                    print(f"No data to save for risk level {risk_level}")
                    
        except Exception as e:
            print(f"Error in save_to_csvs: {e}")
            print(f"Current directory contents: {os.listdir(current_dir)}")
            raise

    def scrape(self, max_days=365):
        print("Setting up Chrome driver...")
        driver = self.setup_driver()
        print("Chrome driver setup complete!")

        try:
            print(f"Navigating to {self.url}")
            driver.get(self.url)
            
            # Wait for page to be fully loaded
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            print("Page loaded successfully!")
            print("Press Ctrl+C at any time to stop and save current data")

            days_scraped = 0
            while days_scraped < max_days:
                try:
                    data = self.extract_data(driver)
                    if data:
                        risk_level = data['risk_level']
                        self.risk_data[risk_level].append({
                            'date': data['date'].strftime('%Y-%m-%d'),
                            'risk_rating': risk_level,  # Add numerical risk rating
                            'description': data['description']
                        })
                        print(f"Scraped data for {data['date'].strftime('%Y-%m-%d')} - Risk Level: {risk_level}")

                    if not self.click_back_button(driver):
                        print("Reached end of available data or encountered an error")
                        break

                    days_scraped += 1

                    # Add delay between requests
                    time.sleep(2)

                except KeyboardInterrupt:
                    print("\nScraping interrupted by user. Saving current data...")
                    break
                except Exception as e:
                    print(f"An error occurred while scraping: {e}")
                    break

        except Exception as e:
            print(f"An error occurred during setup: {e}")
        finally:
            try:
                print("Closing Chrome driver...")
                driver.quit()
            except Exception as e:
                print(f"Error closing driver: {e}")
            
            print("Saving data to CSV files...")
            self.save_to_csvs()
            print("Scraping complete!")


# Usage example
if __name__ == "__main__":
    # Replace with your specific zone URL
    zone_url = "https://avalanche.state.co.us/?lat=39.741907569830374&lng=-106.10108581870382"
    zone_name = "your_zone_name"

    print("Starting CAIC Avalanche Risk Scraper...")
    scraper = CAICScraper(zone_url, zone_name)
    scraper.scrape()