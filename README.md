# FAO/World Bank → Navicat Schema Transformer  
### Transform External Dataset to Match IFPRI Navicat Table Schema  
**Created by: Minsol Cho**  
**Date: 2025-08-07**

---

## 📌 개요 (Overview)

이 R 스크립트는 **FAO 또는 World Bank에서 다운로드한 Excel 데이터**를  
IFPRI 내부에서 사용하는 **Navicat 테이블 스키마 구조에 자동 변환(standardization)** 하기 위해 개발되었습니다.

원본 데이터는 기관별로 컬럼 구조가 달라 Navicat DB에서 직접 사용할 수 없기 때문에,  
이 스크립트는 다음과 같은 작업을 자동으로 수행합니다:

- 지표 값(value) 컬럼 자동 탐지  
- ISO3, 연도(Time), 값(value) 컬럼 자동 매핑  
- Navicat에서 요구하는 전체 컬럼 생성 & 정렬  
- indicatorTypeID / unit 사용자 입력  
- 최종 결과를 **Navicat 업로드용 Excel 파일(.xlsx)** 로 저장

---

## 📁 기능 요약 (Features)

### ✔️ 1. 자동 컬럼 탐지
- 메타데이터(예: Country Name, Time 등)를 제외하고  
  데이터 값이 포함된 numeric 컬럼을 자동으로 탐지하여 value 컬럼로 설정함.

### ✔️ 2. 사용자 입력 기반 변환
실행 시 아래 2개 값을 입력해야 함:

Enter indicatorTypeID (e.g., 475):
Enter unit (e.g., Percentage):


### ✔️ 3. Navicat 컬럼 생성 & 스키마 구조 맞춤
- Navicat 테이블 스키마에 필요한 **총 23개 컬럼 자동 생성**
- 존재하지 않는 컬럼은 NA로 자동 채워 넣음

### ✔️ 4. 데이터 정제 기능
- ".." 또는 비수치 값 제거  
- value 컬럼 numeric 변환  
- NA 값 필터링  

### ✔️ 5. 안전한 파일명 생성
name_EN 값 기반으로:


<indicator_name>_for_Navicat.xlsx

형태의 Excel 파일 자동 저장

---

## 🧪 사용 방법 (How to Use)

### 1) 패키지 설치
```r
install.packages(c("readxl", "dplyr", "openxlsx"))

2) 스크립트 실행
source("make_navicat_data.R")

3) 파일 선택

실행 후 자동으로 파일 선택 창이 뜹니다:

file_path <- file.choose()

4) 사용자 입력

스크립트가 다음 질문을 표시함:

Enter indicatorTypeID (e.g., 475):
Enter unit (e.g., Percentage):

5) 변환 결과

예시 출력:

GDP_growth_for_Navicat.xlsx

📂 입력 형식 예시 (Input Format)

필수 컬럼:

Country Code

Time

<indicator value column>

예:

Country Code	Country Name	Time	2022	2023
USA	United States	2022	5.1	4.9

value 컬럼은 스크립트가 자동 탐지함.

📤 출력 형식 (Output Format)

최종 파일에는 Navicat 스키마의 전체 컬럼이 포함됨:

phase, id, name_EN, name_ES, name_FR, indicatorTypeID,
commodityID, ISO3Code, subregionID, continentalregionID,
date, year, unit, percentageChangeAlert, referencePeriod,
frequencyID, value, created, lastUpdate, Notes, last_sync,
dataSourceID, percentageChange95Threshold,
percentageChange90Threshold, monthIPC3

🧠 내부 로직 (Main Logic)
1. Value Column Detection
numeric_values <- suppressWarnings(as.numeric(df[[colname]]))


numeric 데이터가 포함된 첫 번째 컬럼을 value로 자동 지정.

2. 컬럼 이름 변환
rename(
  ISO3Code = `Country Code`,
  year = Time,
  value = all_of(value_col)
)

3. 누락된 Navicat 컬럼 자동 생성

없는 컬럼은 모두 NA로 채움.

4. 최종 컬럼 정렬

Navicat 스키마 순서대로 select 수행.

⚠️ 제한사항 (Limitations)

원본 데이터에 Country Code 또는 Time 컬럼이 없으면 에러 발생

하나 이상의 numeric-like value 컬럼이 있는 경우, 첫 번째 컬럼만 사용

복잡한 멀티-지표 파일은 스크립트 범위 밖

🛠️ 개발 도구 (Tools Used)

R

readxl

dplyr

openxlsx

Windows 환경 기준

👩‍💻 작성자 (Author)

Minsol Cho
IFPRI MTI Unit
Data Integration & Shiny Dashboard Development
