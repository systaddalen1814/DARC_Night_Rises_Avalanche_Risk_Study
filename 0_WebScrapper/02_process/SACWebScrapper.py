import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import html

avi_risk_summary = {"low" : [], "moderate" : [],"considerable" : [],"high" : [],"extreme" : []}
x = [x for x in range(0, 10)]

for i in x:
    baseURL = f"https://www.sierraavalanchecenter.org/prior-jan-6-2021/archive?date_filter_op=%3C%3D&date_filter%5Bvalue%5D%5Bdate%5D=01/30/2025&date_filter%5Bmin%5D%5Bdate%5D=01/30/2025&date_filter%5Bmax%5D%5Bdate%5D=&items_per_page=200&page={i}"
    resp  = requests.get(baseURL)
    print(resp.status_code)
    soup = BeautifulSoup(resp.content, 'html.parser')
    list_of_table_row = soup.find_all("td", "views-field views-field-field-bottomlinetext")
    for column in list_of_table_row:
        danger = re.search(r"(\bLOW\b|\bMODERATE\b|\bCONSIDERABLE\b|\bHIGH\b|\bEXTREME\b)", column.get_text())
        if not danger:
            continue
        avi_risk_summary[danger.group(1).lower()].append(column.get_text())

for key in avi_risk_summary.keys():
    pd.Series(avi_risk_summary[key]).to_csv(f"../04_product/avi_risk_SAC_{key}.csv")