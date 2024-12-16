from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
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
daishinDriver = webdriver.Chrome(service=service, options=chrome_options)
daishinDriver.get("https://asset.daishin.com/ko/?pages=etf")

def getAddress(etfName):
  result = {
    "url" : ""
  }
  try:
    #리스트된 모든 요소 가져오기
    fund_elements = WebDriverWait(daishinDriver, 10).until(
      EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.FUND_NM"))
    )

    # 이름 변경
    replaced_name = etfName.replace("대신", "DAISHIN")

    # 각 요소의 텍스트 비교
    for fund in fund_elements:
      title = fund.text
      if replaced_name in title:
        # 일치하는 요소의 부모를 클릭
        parent_element = fund.find_element(By.XPATH, "./ancestor::div[contains(@class, 'etfinner')]")
        parent_element.click()
        break
    
    result["url"] = daishinDriver.current_url    
    print(json.dumps(result))
  except:
    print(json.dumps(result))
  finally:
    daishinDriver.quit()

if len(sys.argv) > 1:
  receivedName = sys.argv[1]
  getAddress(receivedName)
else:
  print("ETF 이름을 제공해야 합니다.")