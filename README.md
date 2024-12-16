<!-- Heading -->

# ETF Profiler

---

이 프로젝트는 국내에 상장된 ETF 상품의 모든 정보를 한 눈에 보기 쉽도록 도와주는 역할을 하는 프로젝트입니다.

구글 시트를 기반으로 작동되며, 종목 코드를 입력하면 해당 코드의 **ETF 상품명, 기간 수익률, 현재 거래량, 총 보수율, 출시일, 순자산 총액** 데이터를 업데이트 해주며, 해당 상품의 **네이버 증권 페이지**, **ETF CHECK 페이지** 그리고 **자산 운용사의 소개 페이지**까지 검색해서 주소를 연동하도록 설정되어 있습니다.

## Features

---

- **네이버 증권 페이지 데이터 크롤링**

ETF 상품명, 기간 수익률 데이터 및 URL 추출
예: "SOL 미국나스닥100", 기간수익률: 5.34%, URL: ""

- **ETF CHECK 페이지 데이터 크롤링**

현재 거래량, 총보수율, 설정일, 순자산 총액 및 URL 추출

- **자산운용사 페이지 검색 및 URL 추출**

자산운용사 웹사이트에서 해당 ETF 상품 검색 후 URL 추출

- **구글 시트 업데이트**

크롤링한 데이터를 구글 시트 셀에 업데이트 및 열 추가

## Installation

#### 업로드 계정 설정

1. [구글 클라우드 프로젝트 생성](https://console.cloud.google.com/projectcreate)
2. 프로젝트에 Google Sheets API 활성화 후 서비스 계정 생성 및 인증 키(JSON) 다운로드
3. 생성된 서비스 계정 이메일을 구글 시트 **편집자**로 추가

#### 코드 실행

1. 다운로드한 JSON 파일을 프로젝트 폴더에 저장
2. 필요 라이브러리를 설치해준다.

```bash
npm install
```

3.  `index.js` 파일에서 **spreadsheetId** 값 교체

```javascript
// spreadsheetId는 업데이트 할 구글 시트의 URL 참조
// https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit?gid=SHEET_ID#gid=SHEET_ID

const spreadsheetId = "SPREADSHEET_ID"; // 여기에 구글 시트 ID 입력
```

4. `index.js` 파일 실행

```bash
npm start # or node index.js
```

## Usage

### 사용 예시

1. 구글시트 종목코드에 "476030" 입력
2. 실행 후, 구글 시트가 다음과 같이 업데이트 됨:
   - ETF명 : SOL 미국나스닥100
   - 기간수익률 1M : 5.34%
   - 기간수익률 3M : 20.51%
   - 기간수익률 6M : 15.38%
   - 기간수익률 1Y : N/A
   - 거래량 : 31,024
   - 총보수율 : 0.55%
   - 설정일 : 2024-03-12
   - 네이버 증권 : https://finance.naver.com/item/main.naver?code=476030
   - 홈페이지 : https://www.soletf.co.kr/ko/fund/etf/211056
   - ETF CHECK : https://www.etfcheck.co.kr/mobile/etpitem/476030/basic
   - 순자산 총액 : 315
3. 초기 업데이트 이후 실행 시 순자산 총액은 우측에 1열에 추가.
4. 상품이 폐지 되었을 경우 ETF명에 "폐지"로 표시

자세한 지원/미지원 목록은 아래를 참고하세요.

## Support

현재 기준 (2024.12.16) 총 27개 자산운용사(KoAct와 히어로즈 포함) 중 25개 자산운용사 상품 대상 상세 URL 업데이트 지원

미지원 자산운용사는 검색기능 제공 X, 수동 입력

| 지원 운용사          | ETF 브랜드      |
| -------------------- | --------------- |
| 한국투자신탁운용     | ACE             |
| BNK자산운용          | BNK             |
| 대신자산운용         | 대신343         |
| DB자산운용           | 마이티          |
| 브이아이자산운용     | FOCUS           |
| 하나자산운용         | 1Q              |
| NH-Amundi자산운용    | HANARO          |
| 흥국자산운용         | HK              |
| IBK자산운용          | ITF             |
| KCGI자산운용         | KCGI            |
| 삼성자산운용         | KoAct, KODEX    |
| 키움자산운용         | KOSEF, 히어로즈 |
| 마이다스에셋자산운용 | MIDAS           |
| 한화자산운용         | PLUS            |
| 신한자산운용         | SOL             |
| 미래에셋자산운용     | TIGER           |
| 타임폴리오자산운용   | TIMEFOLIO       |
| 유리자산운용         | TREX            |
| 트러스톤자산운용     | TRUSTON         |
| 현대자산운용         | UNICORN         |
| 우리자산운용         | WON             |

**미지원 목록**

- 한국투자밸류자산운용 (VITA)
- 에셋플러스자산운용 (에셋플러스)
