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
solDriver = webdriver.Chrome(service=service, options=chrome_options)
solDriver.get("https://www.soletf.co.kr/ko/fund")

def getAddress(etfCode):
  result = {
    "url" : ""
  }
  try:
    #검색창 찾기
    search_bar = WebDriverWait(solDriver, 10).until(
      EC.presence_of_element_located((By.CLASS_NAME, "sch-ipt-in input[name='keyword']"))
    )
    search_bar.send_keys(etfCode + Keys.ENTER)
    time.sleep(2)

    search_res = WebDriverWait(solDriver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, "#container > div.contents > table > tbody"))
    )
    first_element = search_res.find_element(By.CSS_SELECTOR, "tr:first-child > td.tb-subj > a")
    first_element.click()

    result["url"] = solDriver.current_url    
    print(json.dumps(result))
  except:
    print(json.dumps(result))
  finally:
    solDriver.quit()

if len(sys.argv) > 1:
  receivedCode = sys.argv[1]
  getAddress(receivedCode)
else:
  print("ETF 이름을 제공해야 합니다.")  