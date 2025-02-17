from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import pandas as pd

Data_LOW = pd.DataFrame({"month":[], "day":[], "year":[],"Danger Message":[],"source":[]})
Data_MODERATE = pd.DataFrame({"month":[], "day":[], "year":[],"Danger Message":[],"source":[]})
Data_CONSIDERABLE = pd.DataFrame({"month":[], "day":[], "year":[],"Danger Message":[],"source":[]})
Data_HIGH = pd.DataFrame({"month":[], "day":[], "year":[],"Danger Message":[],"source":[]})
Data_EXTREME = pd.DataFrame({"month":[], "day":[], "year":[],"Danger Message":[],"source":[]})

add_map = {1 : Data_LOW, 2 : Data_MODERATE, 3 : Data_CONSIDERABLE, 4 : Data_HIGH, 5 : Data_EXTREME}

class Data_ROW:
    '''
    This is the class for managing new rows
    '''
    def __init__(self):
        self.day : int = 0
        self.month : str = ""
        self.year : int = 0
        self.report : str = ""
        self.danger_rating : int = 0
        self.source : str = "SAC"
    def getRow(self) -> dict:
        '''
        :return: Outputs a properly formated new row that can be added to Data
        '''
        return {"month" : self.day, "day" : self.month, "year" : self.year, "Danger Message" : self.report, "source" : self.source}


def incr_url_via_button_press(button_CSS_Selector : str) -> str:
    '''
    :param button_CSS_Selector: The class of the button you want to press in the form "button[class='class_name']" if the class name is not a tailwind thingy then it wont work I dont think
    :return:  html of page found from button press the driver object now has new current url
    '''
    try:
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, button_CSS_Selector))
        )
        button.click()
        # Wait until the page's document.readyState is "complete"
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "nac-forecast-container"))
        )
        return driver.page_source
    except ModuleNotFoundError:
        return None

def scrape(html : str) -> Data_ROW:
    '''
    :param html: this is raw string html
    :return: data that is a row of the database in the form output by Data_ROW
    '''
    try:
        soup = BeautifulSoup(html, 'html.parser')
        date_text = soup.find('div', attrs={'class': 'nac-header-meta'}).get_text()
        bottom_line_text = soup.find('div', attrs={'class': 'nac-bottomLine-text nac-tinymce'}).get_text()
        danger_text = soup.find('span', attrs={'class': 'nac-dangerLabel'}).get_text()

        new_row = Data_ROW()

        new_row.month = re.search(r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\b", date_text).group(1)
        new_row.day = re.search(r"(\b\d{1,2}\b)", date_text).group(1)
        new_row.year = re.search(r"(\b\d\d\d\d\b)", date_text).group(1)
        new_row.report = bottom_line_text
        new_row.danger_rating = int(re.search(r"(\d)", danger_text).group(1))

        return new_row
    except Exception as e:
        print(e)
        return None


list_of_base_urls = ["https://www.sierraavalanchecenter.org/forecasts/#/central-sierra-nevada"]


for url in list_of_base_urls:
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    while True:
        html = incr_url_via_button_press("button[class='nac-btn nac-btn-light nac-btn-lg']")
        new_row = scrape(html)
        if new_row == None:
            print(f"Error Collectiong Data From {driver.current_url}")
            break
        add_map[new_row.danger_rating] = add_map[new_row.danger_rating]._append(new_row.getRow(), ignore_index=True)


    Data_LOW.to_csv("../04_product/avi_risk_SAC_MultiPage-LOW.csv")
    Data_MODERATE.to_csv("../04_product/avi_risk_SAC_MultiPage-MODERATE.csv")
    Data_CONSIDERABLE.to_csv("../04_product/avi_risk_SAC_MultiPage-CONSIDERABLE.csv")
    Data_HIGH.to_csv("../04_product/avi_risk_SAC_MultiPage-HIGH.csv")
    Data_EXTREME.to_csv("../04_product/avi_risk_SAC_MultiPage-EXTREME.csv")