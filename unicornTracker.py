from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
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
unicornDriver = webdriver.Chrome(service=service, options=chrome_options)
unicornDriver.get("https://www.hyundaiam.com/kor/HD-KP-FG/HD-KP-FG-02.html")

def getAddress(etfName):
  result = {
    "url" : ""
  }
  try:    
    #검색창 찾기
    search_bar = WebDriverWait(unicornDriver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, "#divList > div.inner > form > div.board-caption > div > div input[id='txtSearch']"))
    )
    replaced_name = etfName.replace(" ", "")
    search_bar.send_keys(replaced_name)

    search_btn = unicornDriver.find_element(By.CSS_SELECTOR, "#divList > div.inner > form > div.board-caption > div > div button[id='btnSearch']")
    search_btn.click()
    time.sleep(2)

    #검색 결과에서 찾기
    search_res = WebDriverWait(unicornDriver, 10).until(
      EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#tbList > tbody > tr"))
    )

    for _, row in enumerate(search_res):
      a_tag = row.find_element(By.CSS_SELECTOR, "td.align-L > a")
      title = a_tag.text.replace(" ", "")
      if replaced_name in title:
        a_tag.click()
        break

    result["url"] = unicornDriver.current_url    
    print(json.dumps(result))  
  except:
    print(json.dumps(result))
  finally:
    unicornDriver.quit()
    
if len(sys.argv) > 1:
  receivedName = sys.argv[1]
  getAddress(receivedName)
else:
  print("ETF 이름을 제공해야 합니다.")