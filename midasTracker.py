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
midasDriver = webdriver.Chrome(service=service, options=chrome_options)
midasDriver.get("https://midasasset.com/%ed%88%ac%ec%9e%90%ec%83%81%ed%92%88/%ed%8e%80%eb%93%9c%eb%a7%b5/")

def getAddress(etfName):
  result = {
    "url" : ""
  }
  try:
    #검색창 찾기
    search_bar = WebDriverWait(midasDriver, 10).until(
      EC.presence_of_element_located((By.CLASS_NAME, "textBox input[name='ma_fund_name']"))
    )
    search_bar.send_keys(etfName + Keys.ENTER)
    #페이지 업데이트 기다리기
    time.sleep(2)

    # search_res = WebDriverWait(midasDriver, 10).until(
    #   EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#fundmapTb > tr'))
    # )
    # # 일치하는 상품 찾기 & 클릭
    # for _, row in enumerate(search_res):
    #   a_tag = WebDriverWait(midasDriver, 10).until(
    #     EC.element_to_be_clickable((By.CSS_SELECTOR, "td.tit > a"))
    #   )
    #   # a_tag = row.find_element(By.CSS_SELECTOR, "td.tit > a")
    #   title = a_tag.text
    #   if etfName in title:
    #     a_tag.click()
    #     break
    first_list = WebDriverWait(midasDriver, 10).until(
      EC.element_to_be_clickable((By.XPATH, '//*[@id="fundmapTb"]/tr/td[1]/a'))
    )    
    first_list.click()

    result["url"] = midasDriver.current_url    
    print(json.dumps(result))
  except:
    print(json.dumps(result))
  finally:
    midasDriver.quit()
    
if len(sys.argv) > 1:
  receivedName = sys.argv[1]
  getAddress(receivedName)
else:
  print("ETF 이름을 제공해야 합니다.")