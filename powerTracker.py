from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import json

# 백그라운드 모드
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gui") # 필요 시 GPU 렌더링 비활성화
chrome_options.add_argument("--window-size=1920x1080") # 헤드리스 모드에서 창 크기 설정

service = Service(executable_path="chromedriver.exe", port = 0)
powerDriver = webdriver.Chrome(service=service, options=chrome_options)
powerDriver.get("https://www.kyoboaxa-im.co.kr/prdtInfo/powerETFList.do")

def getAddress():
  result = {
    "url" : ""
  }
  try:
    result["url"] = powerDriver.current_url
    print(json.dumps(result))
  except:
    print(json.dumps(result))
  finally:
    powerDriver.quit()

getAddress()