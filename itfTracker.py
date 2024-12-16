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

# 백그라운드 모드
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gui") # 필요 시 GPU 렌더링 비활성화
chrome_options.add_argument("--window-size=1920x1080") # 헤드리스 모드에서 창 크기 설정

service = Service(executable_path="chromedriver.exe", port = 0)
itfDriver = webdriver.Chrome(service=service, options=chrome_options)
itfDriver.get("https://www.ibkasset.com/etf")

def getAddress(etfName):
  result = {
    "url" : ""
  }
  try:
    #검색창 찾기
    search_bar = WebDriverWait(itfDriver, 10).until(
      EC.presence_of_element_located((By.CLASS_NAME, "fund-list-search-form input[id='searchText']"))
    )
    search_bar.send_keys(etfName + Keys.ENTER)
    time.sleep(2)
    
    #첫 번째 결과물 찾기
    first_element = WebDriverWait(itfDriver, 10).until(
      EC.element_to_be_clickable((By.XPATH, '//*[@id="etf-fund-list"]/div/div[2]/ul/li'))
    )
    first_element.click()
    
    result["url"] = itfDriver.current_url
    print(json.dumps(result))
  except:
    print(json.dumps(result))
  finally:
    itfDriver.quit()

if len(sys.argv) > 1:
  receivedName = sys.argv[1]
  getAddress(receivedName)
else:
  print("ETF 이름을 제공해야 합니다.")


