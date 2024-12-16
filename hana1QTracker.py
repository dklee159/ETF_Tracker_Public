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
hana1qDriver = webdriver.Chrome(service=service, options=chrome_options)
hana1qDriver.get("https://1qetf.com/pages/ETFproducts/ETF.list.php")

def getAddress(etfCode):
  result = {
    "url" : ""
  }
  try:
    #검색창 찾기
    search_bar = WebDriverWait(hana1qDriver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, ".no-mainSearch__search-bar input[name='keyword']"))
    )
    #검색어 입력
    search_bar.send_keys(etfCode + Keys.ENTER)
    time.sleep(2)
    ### 방법 1 - 전체 테이블 기다린 후 자식에 접근 ####
    # search_res = WebDriverWait(hana1qDriver, 10).until(
    #   EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#no-contents > section.no-Contents__wrap > div > div > form > ul.etf-table > li"))
    # )

    # if search_res:
    #   # 결과 클릭
    #   first_list = search_res[0].find_element(By.CSS_SELECTOR, "div.etf-table-name > h4 > a")
    #   first_list.click()
    # else:
    #   print("NO ITEMS FOUND in this Page")

    #### 방법 2 - 버튼 활성화 기다리기 ####
    first_list = WebDriverWait(hana1qDriver, 10).until(
      EC.element_to_be_clickable((By.XPATH, '//*[@id="no-contents"]/section[2]/div/div/form/ul[2]/li/div[1]/h4/a'))
    )
    first_list.click()

    result["url"] = hana1qDriver.current_url      
    print(json.dumps(result))
  except:
    print(json.dumps(result))
  finally:
    hana1qDriver.quit()

if len(sys.argv) > 1:
  receivedCode = sys.argv[1]
  getAddress(receivedCode)
else:
  print("ETF 이름을 제공해야 합니다.")