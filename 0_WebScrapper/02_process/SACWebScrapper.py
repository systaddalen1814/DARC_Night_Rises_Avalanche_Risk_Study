import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

Data = pd.DataFrame({"day":[],"month":[],"year":[],"report":[],"danger_rating":[]})

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
    def getRow(self) -> dict:
        '''
        :return: Outputs a properly formated new row that can be added to Data
        '''
        return {"day" : self.day, "month" : self.month, "year" : self.year, "report" : self.report, "danger_rating" : self.danger_rating}

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
        new_row.day = re.search(r"(\b\d+\b)", column.get_text()).group(1)
        new_row.year = re.search(r"(\b\d\d\d\d\b)", column.get_text()).group(1)
        new_row.report = column.get_text()
        Data = Data._append(new_row.getRow(), ignore_index=True)

Data.to_csv("../04_product/Prev_2021_avi_SAC_Data.csv")
