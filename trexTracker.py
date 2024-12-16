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
trexDriver = webdriver.Chrome(service=service, options=chrome_options)
trexDriver.get("https://www.yurieasset.co.kr/yurie/information.asp")

def getAddress(etfName):
  result = {
    "url" : ""
  }
  try:
    #검색창 찾기
    search_bar = WebDriverWait(trexDriver, 10).until(
      EC.presence_of_element_located((By.XPATH, '//*[@id="Text2"]'))
    )
    replaced_name = etfName.replace(" ", "")
    search_bar.send_keys(replaced_name + Keys.ENTER)
    time.sleep(2)

    search_res = WebDriverWait(trexDriver, 10).until(
      EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#fund_list_table > table > tbody > tr"))
    )
    for _, row in enumerate(search_res):
      a_tag = row.find_element(By.CSS_SELECTOR, "td.align_l > a")
      title = a_tag.text
      if replaced_name in title:
        a_tag.click()
        break
    result["url"] = trexDriver.current_url    
    print(json.dumps(result))
  except:
    print(json.dumps(result))
  finally:
    trexDriver.quit()    

if len(sys.argv) > 1:
  receivedName = sys.argv[1]
  getAddress(receivedName)
else:
  print("ETF 이름을 제공해야 합니다.")