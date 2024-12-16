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
tigerDriver = webdriver.Chrome(service=service, options=chrome_options)
tigerDriver.get("https://www.tigeretf.com/ko/search/list.do")

def getAddress(etfCode):
  result = {
    "url" : ""
  }
  try:
    # 검색창 찾기
    search_bar = WebDriverWait(tigerDriver, 10).until(
      EC.presence_of_element_located((By.CLASS_NAME, "form-input-item input[name='q']"))
    )
    search_bar.send_keys(etfCode + Keys.ENTER)
    time.sleep(2)

    #리스트 일치하는 ETF 찾기
    search_res = WebDriverWait(tigerDriver, 10).until(
      EC.element_to_be_clickable((By.CSS_SELECTOR, "#listArea > tr > td:nth-child(1) > div > div.item-subject > a"))
    )
    search_res.click()  

    #타이거는 새창에서 열리기 때문에 페이지 변경 필요
    tigerDriver.switch_to.window(tigerDriver.window_handles[-1])

    result["url"] = tigerDriver.current_url    
    print(json.dumps(result))
  except:
    print(json.dumps(result))
  finally:
    tigerDriver.quit()

if len(sys.argv) > 1:
  receivedCode = sys.argv[1]
  getAddress(receivedCode)
else:
  print("ETF 이름을 제공해야 합니다.")