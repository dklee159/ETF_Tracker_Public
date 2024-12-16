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
wonDriver = webdriver.Chrome(service=service, options=chrome_options)
wonDriver.get("https://www.wooriam.kr/investment/fund-list")

def getAddress(etfCode):
  result = {
    "url" : ""
  }
  try:
    search_bar = WebDriverWait(wonDriver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, "#listForm > div > div.base-search.base-search--lg input[name='searchWord']"))
    )    
    search_bar.send_keys(etfCode + Keys.ENTER)
    time.sleep(2)

    search_res = WebDriverWait(wonDriver, 10).until(
      EC.element_to_be_clickable((By.CSS_SELECTOR, "#wrapper > div.fund-list > section.fund-view__result > ul > li > a"))
    )
    search_res.click()

    result["url"] = wonDriver.current_url    
    print(json.dumps(result))
  except:
    print(json.dumps(result))
  finally:
    wonDriver.quit()

if len(sys.argv) > 1:
  receivedCode = sys.argv[1]
  getAddress(receivedCode)
else:
  print("ETF 이름을 제공해야 합니다.")