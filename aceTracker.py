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
aceDriver = webdriver.Chrome(service=service, options=chrome_options)
aceDriver.get("https://www.aceetf.co.kr/fund?searchText=")


def getAddress(etfCode):
  result = {
    "url" : ""
  }
  try:
    #검색창 찾기
    search_bar = WebDriverWait(aceDriver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, ".search-form.align.both.vm input[name='searchTxt']"))
    )
    #검색어 입력 + 찾기
    search_bar.send_keys(etfCode + Keys.ENTER)
    time.sleep(2)
    
    # 리스트 업데이트 될 때까지 기다리기
    WebDriverWait(aceDriver, 10).until(
      EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "#main > div.fund > div.fund__list > div.fund__list__wrap > ul > li"))
    )

    search_Result = WebDriverWait(aceDriver, 10).until(
      EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div[1]/div[2]/div[3]/ul/li/div[1]/a'))
    )
    search_Result.click()
    result['url'] = aceDriver.current_url

    print(json.dumps(result))
  except: 
    print(json.dumps(result))
  finally:
    aceDriver.quit()

if len(sys.argv) > 1:
  receivedCode = sys.argv[1]
  getAddress(receivedCode)
else:
  print("ETF 이름을 제공해야 합니다.")