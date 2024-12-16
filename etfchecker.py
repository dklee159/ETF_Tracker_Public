from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import time
import sys
import json
import re

chrome_options = Options()
# 인증서 오류 무시
chrome_options.add_argument("--ignore-certificate-errors") 
chrome_options.add_argument("--ignore-ssl-errors")

# 백그라운드 모드
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gui") # 필요 시 GPU 렌더링 비활성화
chrome_options.add_argument("--window-size=1920x1080") # 헤드리스 모드에서 창 크기 설정

service = Service(executable_path="chromedriver.exe")
etfCheckerDriver = webdriver.Chrome(service=service, options=chrome_options)
etfCheckerDriver.get("https://www.etfcheck.co.kr/mobile/search")


def extractNum(val):
  # 먼저 정규식으로 숫자와 쉼표만 추출
  num = re.sub(r"[^\d,]", "", val)
  # 추출된 수를 쉼표 제거 후 정수형으로 변환
  return int(num.replace(",", ""))

def getEtfCheckerAddress(etfCode):
  result = {
    "date": "",
    "cost": "",
    "realExpense": "",
    "trading": "",
    "url": ""
  }  
  try:
    #검색창 찾기
    search_bar = WebDriverWait(etfCheckerDriver, 10).until(
      EC.presence_of_element_located((By.CLASS_NAME, "v-text-field input"))
    )
    #검색어 입력
    search_bar.send_keys(etfCode)

    #정확히 일치하는 키워드 선택
    first_search_result = WebDriverWait(etfCheckerDriver, 10).until(
      EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#_content > div > div.v-card.v-card--flat.v-sheet.theme--light > div > div > div:nth-child(2) > div.table-box-wrap.th_none.v2 > div > table > tbody > tr"))
    )
    if first_search_result:
      #일치하는 항목 클릭
      first_search_result[0].click()

      #페이지 로드 기다리기
      time.sleep(2)
      
      listing_date = WebDriverWait(etfCheckerDriver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.jonginfo_w.jw4.pad_bot.v-card.v-card--flat.v-sheet.theme--light > div > div:nth-child(2) > div > table > tbody > tr:nth-child(2) > td.txt_right > span"))
      )
      total_cost = WebDriverWait(etfCheckerDriver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.jonginfo_w.jw4.pad_bot.v-card.v-card--flat.v-sheet.theme--light > div > div:nth-child(2) > div > table > tbody > tr:nth-child(5) > td.txt_right > span:nth-child(1)"))
      )
      real_customer_expense_ratio = WebDriverWait(etfCheckerDriver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.jonginfo_w.jw4.pad_bot.v-card.v-card--flat.v-sheet.theme--light > div > div:nth-child(4) > div > table > tbody > tr:nth-child(3) > td.txt_right > span"))
      )

      trading_volume = WebDriverWait(etfCheckerDriver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.layout.row.wrap.mt-1 > div > div > div.info_box.right > div.content"))
      )

      result["cost"] = extractNum(total_cost.text)
      result["date"] = listing_date.text.replace(".", "-")
      result["realExpense"] = real_customer_expense_ratio.text
      result["trading"] = trading_volume.text.replace(",", "")
      result["url"] = etfCheckerDriver.current_url

      print(json.dumps(result))
    else:
      print("There are no match result with %s" %(etfCode))
  except:
    print(json.dumps(result))
  finally:
    etfCheckerDriver.quit()

if len(sys.argv) > 1:
  receivedCode = sys.argv[1]
  getEtfCheckerAddress(receivedCode)
else:
  print("ETF 이름을 제공해야 합니다.")
