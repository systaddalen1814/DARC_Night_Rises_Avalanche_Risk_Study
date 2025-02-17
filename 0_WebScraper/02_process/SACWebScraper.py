import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

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

def DangerNumber(danger : str) -> int:
    match danger:
        case "LOW":
            return 1

        case "MODERATE":
            return 2

        case "CONSIDERABLE":
            return 3

        case "HIGH":
            return 4

        case "EXTREME":
            return 5

        case _:
            return 0



for i in range(0,10):
    baseURL = f"https://www.sierraavalanchecenter.org/prior-jan-6-2021/archive?date_filter_op=%3C%3D&date_filter%5Bvalue%5D%5Bdate%5D=01/30/2025&date_filter%5Bmin%5D%5Bdate%5D=01/30/2025&date_filter%5Bmax%5D%5Bdate%5D=&items_per_page=200&page={i}"
    resp  = requests.get(baseURL)
    print(resp.status_code)
    soup = BeautifulSoup(resp.content, 'html.parser')
    list_of_table_row = soup.find_all("td", "views-field views-field-field-bottomlinetext")
    for column in list_of_table_row:
        new_row = Data_ROW()
        danger = re.search(r"(\bLOW\b|\bMODERATE\b|\bCONSIDERABLE\b|\bHIGH\b|\bEXTREME\b)", column.get_text())
        if not danger:
            continue
        new_row.danger_rating = int(DangerNumber(danger.group(1)))

        new_row.month = re.search(
            r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\b",
            column.get_text()).group(1)
        new_row.day = re.search(r"(\b\d{1,2}\b)", column.get_text()).group(1)
        new_row.year = re.search(r"(\b\d{4}\b)", column.get_text()).group(1)
        new_row.report = column.get_text()
        add_map[new_row.danger_rating] = add_map[new_row.danger_rating]._append(new_row.getRow(), ignore_index=True)

Data_LOW.to_csv("../04_product/avi_risk_SAC-LOW.csv")
Data_MODERATE.to_csv("../04_product/avi_risk_SAC-MODERATE.csv")
Data_CONSIDERABLE.to_csv("../04_product/avi_risk_SAC-CONSIDERABLE.csv")
Data_HIGH.to_csv("../04_product/avi_risk_SAC-HIGH.csv")
Data_EXTREME.to_csv("../04_product/avi_risk_SAC-EXTREME.csv")
