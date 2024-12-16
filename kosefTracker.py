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
kosefDriver = webdriver.Chrome(service=service, options=chrome_options)
kosefDriver.get("https://www.kosef.co.kr/service/etf/KO02010100M")

def getAddress(etfName):
  result = {
    "url" : ""
  }
  try:
    #검색창 찾기
    search_bar = WebDriverWait(kosefDriver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, ".sch-top.ui-input-txt input[id='schName']"))
    )
    search_bar.send_keys(etfName + Keys.ENTER)
    
    time.sleep(2)
    #일치하는 녀석 검색하기
    search_res = WebDriverWait(kosefDriver, 10).until(
      EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#etf-tbody > tr"))
    )

    for _, row in enumerate(search_res):
      a_tag = row.find_element(By.CSS_SELECTOR, "td:nth-child(1) > div > div > a")      
      title = a_tag.text
      if etfName in title :
        a_tag.click()
        break

    result["url"] = kosefDriver.current_url      
    print(json.dumps(result))
  except:
    print(json.dumps(result))
  finally:
    kosefDriver.quit()

if len(sys.argv) > 1:
  receivedName = sys.argv[1]
  getAddress(receivedName)
else:
  print("ETF 이름을 제공해야 합니다.")