from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import json
import sys

# 백그라운드 모드
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gui") # 필요 시 GPU 렌더링 비활성화
chrome_options.add_argument("--window-size=1920x1080") # 헤드리스 모드에서 창 크기 설정

service = Service(executable_path="chromedriver.exe", port = 0)
dbDriver = webdriver.Chrome(service=service, options=chrome_options)
dbDriver.get("https://db-asset.com/front/kr/fund/etf")

def getAddress(etfName):
  result = {
    "url" : ""
  }
  try:
    # tbody 내 모든 tr 요소 가져오기
    rows = WebDriverWait(dbDriver, 10).until(
      EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tbody > tr"))
    )
    
    for _, row in enumerate(rows):
      a_tag = row.find_element(By.CSS_SELECTOR, "td.title > a")
      title = a_tag.text      
      if etfName.replace(" ", "") in title:
        a_tag.click()
        break      

    result["url"] = dbDriver.current_url
    print(json.dumps(result))
  except:
    print(json.dumps(result))
  finally:
    dbDriver.quit()

if len(sys.argv) > 1:
  receivedName = sys.argv[1]
  getAddress(receivedName)
else:
  print("ETF 이름을 제공해야 합니다.")
