from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import sys
import json

# 백그라운드 모드
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gui") # 필요 시 GPU 렌더링 비활성화
chrome_options.add_argument("--window-size=1920x1080") # 헤드리스 모드에서 창 크기 설정

service = Service(executable_path="chromedriver.exe", port = 0)
folioDriver = webdriver.Chrome(service=service, options=chrome_options)
folioDriver.get("https://www.timefolio.co.kr/etf/funds_list.php")

def getAddress(etfName):
  result = {
    "url" : ""
  }
  try:    
    #리스트에서 일치하는 ETF 찾기
    etf_lists = WebDriverWait(folioDriver, 10).until(
      EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#container > div.contents.type2 > div.pdListWrap_230224 > div > form > table > tbody > tr"))
    )
    for _, row in enumerate(etf_lists):
      a_tag = row.find_element(By.CSS_SELECTOR, "td.txtBox > a")
      title = a_tag.text
      if etfName in title:
        a_tag.click()      
        break
    
    result["url"] = folioDriver.current_url    
    print(json.dumps(result))    
  except:
    print(json.dumps(result))
  finally:
    folioDriver.quit()

if len(sys.argv) > 1:
  receivedName = sys.argv[1]
  getAddress(receivedName)
else:
  print("ETF 이름을 제공해야 합니다.")