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
hkDriver = webdriver.Chrome(service=service, options=chrome_options)
hkDriver.get("http://www.hkfund.co.kr/sub_perform.html")

def getAddress(etfName):
  result = {
    "url" : ""
  }
  try:
    #검색창 찾기
    search_bar = WebDriverWait(hkDriver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, "tbody > tr:nth-child(3) > td:nth-child(3) > input.dm"))
    )
    search_bar.send_keys(etfName.replace(" ", "") + Keys.ENTER)    
    time.sleep(2)
    
    first_element = WebDriverWait(hkDriver, 10).until(
      EC.element_to_be_clickable((By.CSS_SELECTOR, '#BContens > table:nth-child(6) > tbody > tr:nth-child(5) > td:nth-child(3) > a'))
    )
    first_element.click()

    result["url"] = hkDriver.current_url
    print(json.dumps(result))
  except:
    print(json.dumps(result))
  finally:
    hkDriver.quit()

if len(sys.argv) > 1:
  receivedName = sys.argv[1]
  getAddress(receivedName)
else:
  print("ETF 이름을 제공해야 합니다.")