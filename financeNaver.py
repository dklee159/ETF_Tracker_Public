from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import time
import sys
import json

chrome_options = Options()

# 백그라운드 모드
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gui") # 필요 시 GPU 렌더링 비활성화
chrome_options.add_argument("--window-size=1920x1080") # 헤드리스 모드에서 창 크기 설정

service = Service(executable_path="chromedriver.exe", port = 0)
financeNaverDriver = webdriver.Chrome(service=service, options=chrome_options)
financeNaverDriver.get("https://finance.naver.com/")

def getNaverData(etfCode):
  result = {
    'url': "",
    'name': "",
    'm1': "",
    'm3': "",
    'm6': "",
    'y1': "",
  }
  try:
    #검색창 찾기
    searchBar_element = WebDriverWait(financeNaverDriver, 10).until(
      EC.presence_of_element_located((By.CLASS_NAME, "search_input"))
    )
    searchBar_element.send_keys(etfCode + Keys.ENTER) #검색어 입력 후 검색

    #페이지 로드 대기
    time.sleep(2)
    etfName = WebDriverWait(financeNaverDriver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, "#middle > div.h_company > div.wrap_company > h2 > a"))
    )
    month_1 = WebDriverWait(financeNaverDriver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, "#tab_con1 > div:nth-child(6) > table > tbody > tr:nth-child(1) > td > em"))
    )
    month_3 = WebDriverWait(financeNaverDriver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, "#tab_con1 > div:nth-child(6) > table > tbody > tr:nth-child(2) > td > em"))
    )
    month_6 = WebDriverWait(financeNaverDriver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, "#tab_con1 > div:nth-child(6) > table > tbody > tr:nth-child(3) > td > em"))
    )
    year_1 = WebDriverWait(financeNaverDriver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, "#tab_con1 > div:nth-child(6) > table > tbody > tr:nth-child(4) > td > em"))
    )

    result["name"] = etfName.text
    result["m1"] = month_1.text
    result["m3"] = month_3.text
    result["m6"] = month_6.text
    result["y1"] = year_1.text
    result["url"] = financeNaverDriver.current_url
    print(json.dumps(result))
  except:
    print(json.dumps(result))
  finally:
    financeNaverDriver.quit()

if len(sys.argv) > 1:
  receivedName = sys.argv[1]
  getNaverData(receivedName)
else:
  print("ETF 이름을 제공해야 합니다.")