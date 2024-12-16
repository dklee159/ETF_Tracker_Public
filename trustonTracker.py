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
trustonDriver = webdriver.Chrome(service=service, options=chrome_options)
trustonDriver.get("https://www.trustonasset.com/?taxonomy=ta_fund_cat&term=all")

def getAddress(etfName):
  result = {
    "url" : ""
  }
  try:
    #검색창 찾기
    search_bar = WebDriverWait(trustonDriver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, "div.fund_tab_under > table > tbody > tr > td input[name='fund_name']"))
    )
    search_bar.send_keys(etfName + Keys.ENTER)
    time.sleep(2)

    search_res = WebDriverWait(trustonDriver, 10).until(
      EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#fund_search_result > div > table > tbody > tr"))
    )
    for _, row in enumerate(search_res):
      a_tag = row.find_element(By.CSS_SELECTOR, "td.fsr_td2 > a")
      title = a_tag.text
      if etfName in title:
        a_tag.click()
        break
    
    result["url"] = trustonDriver.current_url    
    print(json.dumps(result))
  except:
    print(json.dumps(result))
  finally:
    trustonDriver.quit()

if len(sys.argv) > 1:
  receivedName = sys.argv[1]
  getAddress(receivedName)
else:
  print("ETF 이름을 제공해야 합니다.")