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
kodexDriver = webdriver.Chrome(service=service, options=chrome_options)
kodexDriver.get("https://m.samsungfund.com/etf/product/list.do")

def getAddress(etfCode):
  result = {
    "url" : ""
  }
  try:
    #데이터 로딩 기다리기
    WebDriverWait(kodexDriver, 10).until(
      EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#root-etf-list > div.prd-list-wrap > div > div.prd-grid > div > ul > li"))
    )
    time.sleep(2) ## 이 페이지는 초기화가 늦게 진행됨

    #검색창 찾기
    search_bar = WebDriverWait(kodexDriver, 10).until(
      EC.element_to_be_clickable((By.CSS_SELECTOR, "#root-etf-list > div:nth-child(1) > div > div.search-container > div > form > div input[id='searchKeyword']"))
    )    
    #검색
    search_bar.send_keys(etfCode + Keys.ENTER)   
    time.sleep(2)
    first_list = WebDriverWait(kodexDriver, 10).until(
      EC.element_to_be_clickable((By.XPATH, '//*[@id="root-etf-list"]/div[2]/div/div[2]/div/ul/li/div/div/a'))
    )
    first_list.click()

    result["url"] = kodexDriver.current_url
    print(json.dumps(result))
  except:
    print(json.dumps(result))
  finally:
    kodexDriver.quit()

if len(sys.argv) > 1:
  receivedCode = sys.argv[1]
  getAddress(receivedCode)
else:
  print("ETF 이름을 제공해야 합니다.")


