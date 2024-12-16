const {google} = require('googleapis');
const {spawn} = require('child_process');

const scopes = ['https://www.googleapis.com/auth/spreadsheets'];

const auth = new google.auth.GoogleAuth({
  keyFile: "./credentials.json",
  scopes
});

const spreadsheetId = "1d4fvSmEIZ5Zvx6f3nI8KJAKLwdq_XjqntgQi8Ggb6Jk";

const googleSheets = google.sheets({
  version: 'v4',
  auth
});

async function writeToSheet(range, values) {
  const valueInputOption = "USER_ENTERED";
  const resource = { values };
  try {
    const res = await googleSheets.spreadsheets.values.update({      
      spreadsheetId, range, valueInputOption, resource
    });
    return res;
  } catch (err) {
    console.log('err', err);
  }
}

async function initSheet(rowIndex, _values) {
  const valueInputOption = "USER_ENTERED";
  const ranges = {
    etfName : `ETF!H${rowIndex}`,
    profit_m1 : `ETF!J${rowIndex}`,
    profit_m3 : `ETF!M${rowIndex}`,
    profit_m6 : `ETF!O${rowIndex}`,
    profit_y1 : `ETF!P${rowIndex}`,
    trading : `ETF!Q${rowIndex}`,
    expense : `ETF!R${rowIndex}`,
    date : `ETF!U${rowIndex}`,
    naverUrl : `ETF!V${rowIndex}`,
    home : `ETF!W${rowIndex}`,
    etfCheck: `ETF!Y${rowIndex}`,
    totalCost: `ETF!Z${rowIndex}`
  }

  const data = [];

  for (let key in ranges) {
    data.push({
      range: ranges[key],
      values: [_values[key]]
    });
  }

  const resource = { data, valueInputOption };
  try {
    const res = await googleSheets.spreadsheets.values.batchUpdate({
      spreadsheetId, resource
    });
    console.log('%d cells updated.', res.data.totalUpdatedCells);
    return res;
  } catch (err) {
    console.log('err', err);
  }
}

async function updateSheet(nameChanged, rowIndex, _values) {
  const valueInputOption = "USER_ENTERED";
  const endColumn = await getColumnEnd();

  const ranges = {
    profit_m1 : `ETF!J${rowIndex}:J${rowIndex}`,
    profit_m3 : `ETF!M${rowIndex}:M${rowIndex}`,
    profit_m6 : `ETF!O${rowIndex}:O${rowIndex}`,
    profit_y1 : `ETF!P${rowIndex}:P${rowIndex}`,
    trading : `ETF!Q${rowIndex}:Q${rowIndex}`,
    expense : `ETF!R${rowIndex}:R${rowIndex}`,
    totalCost: `ETF!${endColumn}${rowIndex}`
  }

  if (nameChanged) {
    ranges.etfName = `ETF!H${rowIndex}:H${rowIndex}`
  }

  const data = [];

  for (let key in ranges) {
    data.push({
      range: ranges[key],
      values: [_values[key]]
    });
  }

  const resource = { data, valueInputOption };
  try {
    const res = await googleSheets.spreadsheets.values.batchUpdate({
      spreadsheetId, resource
    });
    console.log('%d cells updated.', res.data.totalUpdatedCells);
    return res;
  } catch (err) {
    console.log('err', err);
  }
}

async function readSheet(_ranges) {
  let ranges = _ranges;

  try {
    const res = await googleSheets.spreadsheets.values.batchGet({
      spreadsheetId, ranges
    });
    console.log(`${res.data.valueRanges.length} ranges retrieved.`);
    return res;
  } catch(err) {
    throw err;
  }
}

//시트에 마지막 열 추가하기
async function addColumn() {
  const sheet = await googleSheets.spreadsheets.get({
    spreadsheetId
  });      
  const matchedSheet = sheet.data.sheets.find(s => s.properties.title === "ETF");

  //맨 우측에 1열 추가 로직
  const requests = [
    {
      appendDimension : {
        sheetId: matchedSheet.properties.sheetId,
        dimension: "COLUMNS",
        length: 1 // 열 1개 추가
      }
    }
  ];
  const resource = { requests };

  try {
    const res = await googleSheets.spreadsheets.batchUpdate({
      spreadsheetId, resource
    });
    console.log('New Column Added Successfully');
    return res;
  } catch(err) {
    console.error("Error when adding column:", err);
  }
}

//시트의 마지막 열 구하기
async function getColumnEnd() {
  const sheet = await googleSheets.spreadsheets.get({
    spreadsheetId
  });      
  const matchedSheet = sheet.data.sheets.find(s => s.properties.title === "ETF");  
  const columnCount = matchedSheet.properties.gridProperties.columnCount;
  
  return changeColumnToLetter(columnCount);  
}

//마지막 열을 문자로 치환하기
function changeColumnToLetter(columnNum) {
  let letter = "";
  while (columnNum > 0) {
    const mod = (columnNum - 1) % 26;
    letter = String.fromCharCode(65 + mod) + letter;
    columnNum = Math.floor((columnNum - 1) / 26);
  }
  return letter
}

async function getEtfCheckData(etfCode) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', ['etfchecker.py', etfCode]);
    pythonProcess.stdout.on('data', (data) => {
      console.log(`Python stdout: ${data}`);
      try {
        const result = JSON.parse(data.toString()); // JSON 파싱
        resolve(result);
      } catch (err) {
        reject(`Failed to parse JSON: ${err}`);
      }
    });

    pythonProcess.stderr.on('data', (data) => {
      console.log(`Python stderr: ${data}`);
      reject(data.toString());
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) { //code 가 0 이면 종료됨을 의미
        reject(`Python script exited with code - ${code}`);
      }
    });
  });
}

async function getEtfFinanceData(etfCode) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', ['financeNaver.py', etfCode]);
    pythonProcess.stdout.on('data', (data) => {
      console.log(`Python stdout: ${data}`);
      try {
        const result = JSON.parse(data.toString()); // JSON 파싱
        resolve(result);
      } catch (err) {
        reject(`Failed to parse JSON: ${err}`);
      }
    });

    pythonProcess.stderr.on('data', (data) => {
      console.log(`Python stderr: ${data}`);
      reject(data.toString());
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(`Python script exited with code - ${code}`);
      }
    });
  });
}

async function get1QUrl(etfCode) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', ['hana1QTracker.py', etfCode]);
    pythonProcess.stdout.on('data', (data) => {
      console.log(`hana1QTracker.py stdout: ${data}`);
      try {
        const result = JSON.parse(data.toString()).url; // JSON 파싱
        resolve(result);
      } catch (err) {
        console.log(`Failed to parse JSON: ${err}`);
        resolve("");
      }
    });

    pythonProcess.stderr.on('data', (data) => {
      console.log(`Python stderr: ${data}`);
      reject(data.toString());
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(`Python script exited with code - ${code}`);
      }
    });
  });
}

async function getAceUrl(etfCode) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', ['aceTracker.py', etfCode]);
    pythonProcess.stdout.on('data', (data) => {
      console.log(`aceTracker.py stdout: ${data}`);
      try {
        const result = JSON.parse(data.toString()).url; // JSON 파싱
        resolve(result);
      } catch (err) {
        console.log(`Failed to parse JSON: ${err}`);
        resolve("");
      }
    });

    pythonProcess.stderr.on('data', (data) => {
      console.log(`Python stderr: ${data}`);
      reject(data.toString());
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(`Python script exited with code - ${code}`);
      }
    });
  });
}

async function getBnkUrl(etfName) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', ['bnkTracker.py', etfName]);
    pythonProcess.stdout.on('data', (data) => {
      console.log(`bnkTracker.py stdout: ${data}`);
      try {
        const result = JSON.parse(data.toString()).url; // JSON 파싱
        resolve(result);
      } catch (err) {
        console.log(`Failed to parse JSON: ${err}`);
        resolve("");
      }
    });

    pythonProcess.stderr.on('data', (data) => {
      console.log(`Python stderr: ${data}`);
      reject(data.toString());
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(`Python script exited with code - ${code}`);
      }
    });
  });
}

async function getDaishinUrl(etfName) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', ['daishinTracker.py', etfName]);
    pythonProcess.stdout.on('data', (data) => {
      console.log(`daishinTracker.py stdout: ${data}`);
      try {
        const result = JSON.parse(data.toString()).url; // JSON 파싱
        resolve(result);
      } catch (err) {
        console.log(`Failed to parse JSON: ${err}`);
        resolve("");
      }
    });

    pythonProcess.stderr.on('data', (data) => {
      console.log(`Python stderr: ${data}`);
      reject(data.toString());
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(`Python script exited with code - ${code}`);
      }
    });
  });
}

async function getDBUrl(etfName) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', ['dbTracker.py', etfName]);
    pythonProcess.stdout.on('data', (data) => {
      console.log(`dbTracker.py stdout: ${data}`);
      try {
        const result = JSON.parse(data.toString()).url; // JSON 파싱
        resolve(result);
      } catch (err) {
        console.log(`Failed to parse JSON: ${err}`);
        resolve("");
      }
    });

    pythonProcess.stderr.on('data', (data) => {
      console.log(`Python stderr: ${data}`);
      reject(data.toString());
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(`Python script exited with code - ${code}`);
      }
    });
  });
}

async function getFocusUrl(etfName) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', ['focusTracker.py', etfName]);
    pythonProcess.stdout.on('data', (data) => {
      console.log(`focusTracker.py stdout: ${data}`);
      try {
        const result = JSON.parse(data.toString()).url; // JSON 파싱
        resolve(result);
      } catch (err) {
        console.log(`Failed to parse JSON: ${err}`);
        resolve("");
      }
    });

    pythonProcess.stderr.on('data', (data) => {
      console.log(`Python stderr: ${data}`);
      reject(data.toString());
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(`Python script exited with code - ${code}`);
      }
    });
  });
}

async function getHanaroUrl(etfName) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', ['hanaroTracker.py', etfName]);
    pythonProcess.stdout.on('data', (data) => {
      console.log(`hanaroTracker.py stdout: ${data}`);
      try {
        const result = JSON.parse(data.toString()).url; // JSON 파싱
        resolve(result);
      } catch (err) {
        console.log(`Failed to parse JSON: ${err}`);
        resolve("");
      }
    });

    pythonProcess.stderr.on('data', (data) => {
      console.log(`Python stderr: ${data}`);
      reject(data.toString());
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(`Python script exited with code - ${code}`);
      }
    });
  });
}

async function getHkUrl(etfName) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', ['hkTracker.py', etfName]);
    pythonProcess.stdout.on('data', (data) => {
      console.log(`hkTracker.py stdout: ${data}`);
      try {
        const result = JSON.parse(data.toString()).url; // JSON 파싱
        resolve(result);
      } catch (err) {
        console.log(`Failed to parse JSON: ${err}`);
        resolve("");
      }
    });

    pythonProcess.stderr.on('data', (data) => {
      console.log(`Python stderr: ${data}`);
      reject(data.toString());
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(`Python script exited with code - ${code}`);
      }
    });
  });
}

async function getItfUrl(etfName) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', ['itfTracker.py', etfName]);
    pythonProcess.stdout.on('data', (data) => {
      console.log(`itfTracker.py stdout: ${data}`);
      try {
        const result = JSON.parse(data.toString()).url; // JSON 파싱
        resolve(result);
      } catch (err) {
        console.log(`Failed to parse JSON: ${err}`);
        resolve("");
      }
    });

    pythonProcess.stderr.on('data', (data) => {
      console.log(`Python stderr: ${data}`);
      reject(data.toString());
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(`Python script exited with code - ${code}`);
      }
    });
  });
}

async function getKoactUrl(etfCode) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', ['koactTracker.py', etfCode]);
    pythonProcess.stdout.on('data', (data) => {
      console.log(`koactTracker.py stdout: ${data}`);
      try {
        const result = JSON.parse(data.toString()).url; // JSON 파싱
        resolve(result);
      } catch (err) {
        console.log(`Failed to parse JSON: ${err}`);
        resolve("");
      }
    });

    pythonProcess.stderr.on('data', (data) => {
      console.log(`Python stderr: ${data}`);
      reject(data.toString());
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(`Python script exited with code - ${code}`);
      }
    });
  });
}

async function getKodexUrl(etfCode) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', ['kodexTracker.py', etfCode]);
    pythonProcess.stdout.on('data', (data) => {
      console.log(`kodexTracker.py stdout: ${data}`);
      try {
        const result = JSON.parse(data.toString()).url; // JSON 파싱
        resolve(result);
      } catch (err) {
        console.log(`Failed to parse JSON: ${err}`);
        resolve("");
      }
    });

    pythonProcess.stderr.on('data', (data) => {
      console.log(`Python stderr: ${data}`);
      reject(data.toString());
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(`Python script exited with code - ${code}`);
      }
    });
  });
}

async function getKosefUrl(etfName) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', ['kosefTracker.py', etfName]);
    pythonProcess.stdout.on('data', (data) => {
      console.log(`kosefTracker.py stdout: ${data}`);
      try {
        const result = JSON.parse(data.toString()).url; // JSON 파싱
        resolve(result);
      } catch (err) {
        console.log(`Failed to parse JSON: ${err}`);
        resolve("");
      }
    });

    pythonProcess.stderr.on('data', (data) => {
      console.log(`Python stderr: ${data}`);
      reject(data.toString());
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(`Python script exited with code - ${code}`);
      }
    });
  });
}

async function getMidasUrl(etfName) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', ['midasTracker.py', etfName]);
    pythonProcess.stdout.on('data', (data) => {
      console.log(`midasTracker.py stdout: ${data}`);
      try {
        const result = JSON.parse(data.toString()).url; // JSON 파싱
        resolve(result);
      } catch (err) {
        console.log(`Failed to parse JSON: ${err}`);
        resolve("");
      }
    });

    pythonProcess.stderr.on('data', (data) => {
      console.log(`Python stderr: ${data}`);
      reject(data.toString());
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(`Python script exited with code - ${code}`);
      }
    });
  });
}

async function getPlusUrl(etfCode) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', ['plusTracker.py', etfCode]);
    pythonProcess.stdout.on('data', (data) => {
      console.log(`plusTracker.py stdout: ${data}`);
      try {
        const result = JSON.parse(data.toString()).url; // JSON 파싱
        resolve(result);
      } catch (err) {
        console.log(`Failed to parse JSON: ${err}`);
        resolve("");
      }
    });

    pythonProcess.stderr.on('data', (data) => {
      console.log(`Python stderr: ${data}`);
      reject(data.toString());
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(`Python script exited with code - ${code}`);
      }
    });
  });
}

async function getPowerUrl() {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', ['powerTracker.py']);
    pythonProcess.stdout.on('data', (data) => {
      console.log(`powerTracker.py stdout: ${data}`);
      try {
        const result = JSON.parse(data.toString()).url; // JSON 파싱
        resolve(result);
      } catch (err) {
        console.log(`Failed to parse JSON: ${err}`);
        resolve("");
      }
    });

    pythonProcess.stderr.on('data', (data) => {
      console.log(`Python stderr: ${data}`);
      reject(data.toString());
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(`Python script exited with code - ${code}`);
      }
    });
  });
}

async function getRiseUrl(etfCode) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', ['riseTracker.py', etfCode]);
    pythonProcess.stdout.on('data', (data) => {
      console.log(`riseTracker.py stdout: ${data}`);
      try {
        const result = JSON.parse(data.toString()).url; // JSON 파싱
        resolve(result);
      } catch (err) {
        console.log(`Failed to parse JSON: ${err}`);
        resolve("");
      }
    });

    pythonProcess.stderr.on('data', (data) => {
      console.log(`Python stderr: ${data}`);
      reject(data.toString());
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(`Python script exited with code - ${code}`);
      }
    });
  });
}

async function getSolUrl(etfCode) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', ['solTracker.py', etfCode]);
    pythonProcess.stdout.on('data', (data) => {
      console.log(`solTracker.py stdout: ${data}`);
      try {
        const result = JSON.parse(data.toString()).url; // JSON 파싱
        resolve(result);
      } catch (err) {
        console.log(`Failed to parse JSON: ${err}`);
        resolve("");
      }
    });

    pythonProcess.stderr.on('data', (data) => {
      console.log(`Python stderr: ${data}`);
      reject(data.toString());
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(`Python script exited with code - ${code}`);
      }
    });
  });
}

async function getTigerUrl(etfCode) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', ['tigerTracker.py', etfCode]);
    pythonProcess.stdout.on('data', (data) => {
      console.log(`tigerTracker.py stdout: ${data}`);
      try {
        const result = JSON.parse(data.toString()).url; // JSON 파싱
        resolve(result);
      } catch (err) {
        console.log(`Failed to parse JSON: ${err}`);
        resolve("");
      }
    });

    pythonProcess.stderr.on('data', (data) => {
      console.log(`Python stderr: ${data}`);
      reject(data.toString());
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(`Python script exited with code - ${code}`);
      }
    });
  });
}

async function getTimefolioUrl(etfName) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', ['timefolioTracker.py', etfName]);
    pythonProcess.stdout.on('data', (data) => {
      console.log(`timefolioTracker.py stdout: ${data}`);
      try {
        const result = JSON.parse(data.toString()).url; // JSON 파싱
        resolve(result);
      } catch (err) {
        console.log(`Failed to parse JSON: ${err}`);
        resolve("");
      }
    });

    pythonProcess.stderr.on('data', (data) => {
      console.log(`Python stderr: ${data}`);
      reject(data.toString());
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(`Python script exited with code - ${code}`);
      }
    });
  });
}

async function getTrexUrl(etfName) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', ['trexTracker.py', etfName]);
    pythonProcess.stdout.on('data', (data) => {
      console.log(`trexTracker.py stdout: ${data}`);
      try {
        const result = JSON.parse(data.toString()).url; // JSON 파싱
        resolve(result);
      } catch (err) {
        console.log(`Failed to parse JSON: ${err}`);
        resolve("");
      }
    });

    pythonProcess.stderr.on('data', (data) => {
      console.log(`Python stderr: ${data}`);
      reject(data.toString());
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(`Python script exited with code - ${code}`);
      }
    });
  });
}

async function getTrustonUrl(etfName) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', ['trustonTracker.py', etfName]);
    pythonProcess.stdout.on('data', (data) => {
      console.log(`trustonTracker.py stdout: ${data}`);
      try {
        const result = JSON.parse(data.toString()).url; // JSON 파싱
        resolve(result);
      } catch (err) {
        console.log(`Failed to parse JSON: ${err}`);
        resolve("");
      }
    });

    pythonProcess.stderr.on('data', (data) => {
      console.log(`Python stderr: ${data}`);
      reject(data.toString());
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(`Python script exited with code - ${code}`);
      }
    });
  });
}

async function getUnicornUrl(etfName) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', ['unicornTracker.py', etfName]);
    pythonProcess.stdout.on('data', (data) => {
      console.log(`unicornTracker.py stdout: ${data}`);
      try {
        const result = JSON.parse(data.toString()).url; // JSON 파싱
        resolve(result);
      } catch (err) {
        console.log(`Failed to parse JSON: ${err}`);
        resolve("");
      }
    });

    pythonProcess.stderr.on('data', (data) => {
      console.log(`Python stderr: ${data}`);
      reject(data.toString());
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(`Python script exited with code - ${code}`);
      }
    });
  });
}

async function getWonUrl(etfCode) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', ['wonTracker.py', etfCode]);
    pythonProcess.stdout.on('data', (data) => {
      console.log(`wonTracker.py stdout: ${data}`);
      try {
        const result = JSON.parse(data.toString()).url; // JSON 파싱
        resolve(result);
      } catch (err) {
        console.log(`Failed to parse JSON: ${err}`);
        resolve("");
      }
    });

    pythonProcess.stderr.on('data', (data) => {
      console.log(`Python stderr: ${data}`);
      reject(data.toString());
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(`Python script exited with code - ${code}`);
      }
    });
  });
}

(async() => {
  const startRowIndex = 7;
  const codeColumn = await readSheet([`ETF!G${startRowIndex}:G`, `ETF!H${startRowIndex}:H`, `ETF!R${startRowIndex}:R`]);
  const codeNums = codeColumn.data.valueRanges[0].values.map(row => row[0]);
  const etfNames = codeColumn.data.valueRanges[1].values?.map(row => row[0]);
  // await addColumn();

  for (let i = 0; i < codeNums.length; i++) {
    const etfCode = codeNums[i];
    const rowIndex = startRowIndex + i;    

    try {
      const etfFinance_data = await getEtfFinanceData(etfCode);
      console.log(`Fetched ETF Finance Data for ${etfCode}: ${etfFinance_data}`);
      
      const etfName = etfFinance_data.name;
      if (etfName !== "") {
        const etfCheck_data = await getEtfCheckData(etfCode);
        console.log(`Fetched ETF Checker Data for ${etfCode}: ${etfCheck_data}`);
        
        if (etfNames && etfNames[i]) {
          // 만약 ETF 이름이 변경된 경우 업데이트 필요
          const nameChanged = etfNames[i] !== etfFinance_data.name;
          const values = {
            profit_m1 : [etfFinance_data.m1],
            profit_m3 : [etfFinance_data.m3],
            profit_m6 : [etfFinance_data.m6],
            profit_y1 : [etfFinance_data.y1],
            trading : [etfCheck_data.trading],
            expense : [etfCheck_data.realExpense],
            totalCost : [etfCheck_data.cost]
          }
          if (nameChanged) {
            values.etfName = [etfFinance_data.name]
          };
  
          //변화가 있는 셀은 업데이트
          await updateSheet(nameChanged, rowIndex, values);          
          // 순자산 총액을 위한 새로운 열 추가
          // await updateNewColumn(rowIndex, etfCheck_data.cost);
  
        } else {
          // INIT
          console.log(`Init Data for ${etfCode}`)
          const assets = ["1Q", "ACE", "BNK", "FOCUS", "HANARO", "HK", "ITF", "KCGI", "KoAct", "KODEX", "KOSEF", "PLUS", "RISE", "SOL", "TIGER", "TIMEFOLIO", "TREX", "TRUSTON", "UNICORN", "WON", "대신343", "마이다스", "마이티", "파워", "히어로즈"];
          
  
          const managementName = etfName.split(" ")[0];
          const inAssets = assets.includes(managementName);
  
          let homepage = null;
          if (inAssets) {
            if (managementName === "1Q") {
              homepage = await get1QUrl(etfCode);
            } else if (managementName === "ACE") {
              homepage = await getAceUrl(etfCode);             
            } else if (managementName === "BNK") {
              homepage = await getBnkUrl(etfName);
            } else if (managementName === "FOCUS") {
              homepage = await getFocusUrl(etfName);
            } else if (managementName === "HANARO") {
              homepage = await getHanaroUrl(etfName);
            } else if (managementName === "HK") {
              homepage = await getHkUrl(etfName);
            } else if (managementName === "ITF") {
              homepage = await getItfUrl(etfName);
            } else if (managementName === "KoAct") {
              homepage = await getKoactUrl(etfCode);
            } else if (managementName === "KODEX") {
              homepage = await getKodexUrl(etfCode);
            } else if (managementName === "KOSEF" || managementName === "히어로즈") {
              homepage = await getKosefUrl(etfName);
            } else if (managementName === "PLUS") {
              homepage = await getPlusUrl(etfCode);
            } else if (managementName === "RISE") {
              homepage = await getRiseUrl(etfCode);
            } else if (managementName === "SOL") {
              homepage = await getSolUrl(etfCode);
            } else if (managementName === "TIGER") {
              homepage = await getTigerUrl(etfCode);
            } else if (managementName === "TIMEFOLIO") {
              homepage = await getTimefolioUrl(etfName);
            } else if (managementName === "TREX") {
              homepage = await getTrexUrl(etfName);
            } else if (managementName === "TRUSTON") {
              homepage = await getTrustonUrl(etfName);
            } else if (managementName === "UNICORN") {
              homepage = await getUnicornUrl(etfName);
            } else if (managementName === "WON") {
              homepage = await getWonUrl(etfCode);
            } else if (managementName === "대신343") {
              homepage = await getDaishinUrl(etfName);
            } else if (managementName === "마이다스") {
              homepage = await getMidasUrl(etfName);
            } else if (managementName === "마이티") {
              homepage = await getDBUrl(etfName);
            } else if (managementName === "파워") {
              homepage = await getPowerUrl();
            }
          } 
          const values = {
            etfName : [etfFinance_data.name],
            profit_m1 : [etfFinance_data.m1],
            profit_m3 : [etfFinance_data.m3],
            profit_m6 : [etfFinance_data.m6],
            profit_y1 : [etfFinance_data.y1],
            trading : [etfCheck_data.trading],
            expense : [etfCheck_data.realExpense],
            date : [etfCheck_data.date],
            naverUrl : [etfFinance_data.url],
            home : [homepage],
            etfCheck: [etfCheck_data.url],
            totalCost: [etfCheck_data.cost]
          };
          console.log(values);
          await initSheet(rowIndex, values);
        }
      } else {
        console.log(`${etfCode} - ETF gonna abolished`);
        writeToSheet(`ETF!H${rowIndex}`, [["ETF Abolished"]]);
      }
    } catch(err) {
      console.log(`Failed to get Data for ${etfCode}: ${err}`)
    }
  }
})();