# 🏥 알러지 측정 검사소 통합 가이드

**Phoenix Pet + CareLog 알러지 검사 기능**

---

## 📋 개요

Phoenix Pet 게임에 **AI 기반 개인화 식품 알러지 검사소**를 추가했습니다. 사용자가 자신의 알러지 정보를 등록하고, 식품 이미지 및 원재료 정보를 업로드하면 OpenAI Vision API를 활용하여 알러지 위험도를 판단합니다.

### 주요 기능
- 🔍 **알러지 정보 등록**: 개인화된 알러지 프로필 관리
- 📸 **식품 검사**: 이미지 + OCR 텍스트 기반 AI 분석
- 📊 **분석 결과**: 위험/주의/안전 판정과 상세 분석
- 📋 **검사 기록**: 과거 검사 결과 조회

---

## 🛠️ 설치 및 설정

### 1️⃣ 백엔드 준비

#### 데이터베이스 마이그레이션
```bash
cd backend
psql -U postgres -d phoenix_pet -f database/schema.sql
```

#### 환경 변수 설정
`backend/.env` 파일 생성:
```dotenv
# 기본 설정
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/phoenix_pet
DB_HOST=localhost
DB_PORT=5432
DB_NAME=phoenix_pet
DB_USER=postgres
DB_PASSWORD=your_password

JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
PORT=3000
NODE_ENV=development
CORS_ORIGIN=http://localhost:3001

# 🔑 필수: OpenAI API 키
OPENAI_API_KEY=sk-your-openai-api-key-here
```

#### 패키지 설치 및 실행
```bash
npm install
npm run dev
# 백엔드 실행: http://localhost:3000
```

### 2️⃣ 프론트엔드 준비

```bash
npm install
npm start
# 프론트엔드 실행: http://localhost:3001
```

---

## 📁 새로 추가된 파일

### 백엔드

#### 데이터베이스
- **[database/schema.sql](database/schema.sql)** - 알러지 테이블 추가
  - `user_allergies`: 사용자별 알러지 정보
  - `allergy_check_records`: 검사 기록

#### API
- **[controllers/allergyController.js](controllers/allergyController.js)** - 알러지 로직
  - `setUserAllergies()`: 알러지 정보 등록
  - `getUserAllergies()`: 알러지 정보 조회
  - `checkAllergy()`: AI 기반 검사 (OpenAI Vision API)
  - `getAllergyCheckHistory()`: 검사 기록 조회

- **[routes/allergy.js](routes/allergy.js)** - 알러지 API 라우트
  - `POST /allergy/allergies` - 알러지 등록
  - `GET /allergy/allergies` - 알러지 조회
  - `POST /allergy/check` - 식품 검사
  - `GET /allergy/history` - 검사 기록

#### 설정
- **[.env.example](.env.example)** - `OPENAI_API_KEY` 추가
- **[package.json](package.json)** - `openai` 라이브러리 추가

### 프론트엔드

#### 페이지
- **[src/pages/AllergyCheckPage.js](src/pages/AllergyCheckPage.js)** - 알러지 검사 페이지
  - 3개 탭: 알러지 등록 → 검사하기 → 검사 기록
  - 이미지 업로드 및 OCR 텍스트 입력
  - AI 분석 결과 표시

#### 컴포넌트
- **[src/components/AllergyClinicHouse.js](src/components/AllergyClinicHouse.js)** - 게임 맵에 표시되는 검사소 건물
  - 클릭으로 검사 페이지 이동 가능

#### 서비스
- **[src/services/api.js](src/services/api.js)** - `allergyAPI` 함수 추가
  ```javascript
  allergyAPI.setAllergies(allergies)          // 알러지 등록
  allergyAPI.getAllergies()                   // 알러지 조회
  allergyAPI.checkAllergy(imageBase64, text)  // 검사 실행
  allergyAPI.getCheckHistory(limit)           // 검사 기록
  ```

#### UI 업데이트
- **[src/components/PetWorld.js](src/components/PetWorld.js)** - 검사소 건물 추가
- **[src/pages/HomePage.js](src/pages/HomePage.js)** - 검사소 버튼 추가
- **[src/App.js](src/App.js)** - `/allergy` 라우트 추가

---

## 🔌 API 명세

### 1. 알러지 정보 등록
```http
POST /api/allergy/allergies
Authorization: Bearer {token}
Content-Type: application/json

{
  "allergies": ["계란", "우유", "땅콩"]
}
```

**응답:**
```json
{
  "success": true,
  "message": "알러지 정보가 저장되었습니다.",
  "allergies": ["계란", "우유", "땅콩"]
}
```

### 2. 알러지 정보 조회
```http
GET /api/allergy/allergies
Authorization: Bearer {token}
```

**응답:**
```json
{
  "success": true,
  "allergies": ["계란", "우유", "땅콩"]
}
```

### 3. 식품 알러지 검사
```http
POST /api/allergy/check
Authorization: Bearer {token}
Content-Type: application/json

{
  "imageBase64": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
  "ocrText": "원재료명: 밀, 계란, 우유, 호두\n주의: 견과류 사용 시설에서 제조"
}
```

**응답:**
```json
{
  "success": true,
  "analysis": {
    "verdict": "위험",
    "coreMessage": "계란이 포함되어 있어 위험합니다.",
    "detailedAnalysis": {
      "detectedIngredients": ["계란", "우유"],
      "judgmentReason": "사용자 알러지인 계란이 원재료에 직접 표시되어 있습니다."
    },
    "checkedAt": "2025-01-10T12:34:56.789Z",
    "rawAnalysis": "... AI 분석 전문 ..."
  }
}
```

### 4. 검사 기록 조회
```http
GET /api/allergy/history?limit=10
Authorization: Bearer {token}
```

**응답:**
```json
{
  "success": true,
  "history": [
    {
      "id": "uuid",
      "verdict": "위험",
      "core_message": "계란이 포함되어 있어 위험합니다.",
      "detected_ingredients": ["계란"],
      "judgment_reason": "사용자 알러지인 계란이 포함되어 있습니다.",
      "checked_at": "2025-01-10T12:34:56.789Z"
    }
  ]
}
```

---

## 🤖 AI 분석 로직

### OpenAI Vision API (Claude 3.5 Sonnet)

백엔드의 `allergyController.js`에서 사용자의 알러지 정보와 식품 이미지/텍스트를 함께 분석합니다:

```javascript
const response = await openai.messages.create({
  model: 'claude-3-5-sonnet-20241022',
  max_tokens: 1024,
  messages: [
    {
      role: 'user',
      content: [
        { type: 'text', text: prompt + '\n...' + ocrText },
        { type: 'image', source: { type: 'base64', media_type: 'image/jpeg', data: imageBase64 } }
      ]
    }
  ]
});
```

### 판정 기준

| 판정 | 조건 | 예시 |
|------|------|------|
| 🚨 **위험** | 사용자 알러지 성분이 원재료에 직접 노출됨 | 알러지: 땅콩 → 제품에 "땅콩, 땅콩기름" 포함 |
| ⚠️ **주의** | 혼입 가능성 존재 또는 모호한 성분 | "견과류 사용 시설에서 제조" |
| ✅ **안전** | 알러지 성분 없음 | 알려진 알러지 없음 |

---

## 💡 사용 예시

### 프론트엔드 (React)

```javascript
// 1. 알러지 정보 등록
import { allergyAPI } from '../services/api';

await allergyAPI.setAllergies(['계란', '우유', '땅콩']);

// 2. 알러지 정보 조회
const response = await allergyAPI.getAllergies();
console.log(response.data.allergies); // ['계란', '우유', '땅콩']

// 3. 식품 검사
const imageBase64 = '...'; // 이미지를 Base64로 변환
const ocrText = '원재료명: 밀, 계란, 우유...';

const result = await allergyAPI.checkAllergy(imageBase64, ocrText);
console.log(result.data.analysis);
// {
//   verdict: '위험',
//   coreMessage: '계란이 포함되어 있어 위험합니다.',
//   ...
// }

// 4. 검사 기록 조회
const history = await allergyAPI.getCheckHistory(10);
console.log(history.data.history); // 최근 10개 검사 기록
```

---

## 🎮 게임 내 UX

### 홈페이지
- 우상단에 **"🏥 알러지 검사소"** 버튼 추가
- 게임 맵에 검사소 건물(🏥) 표시
  - 클릭 시 `/allergy` 페이지로 이동

### 알러지 검사 페이지 (`/allergy`)
1. **🔍 알러지 등록 탭**
   - 19개 알러지 옵션 (계란, 우유, 땅콩, 새우, 게 등)
   - 다중 선택 가능
   - "저장" 버튼으로 프로필 등록

2. **📸 검사하기 탭**
   - 이미지 드래그 & 드롭 업로드
   - OCR 텍스트 입력 (원재료명, 주의사항 등)
   - "🔬 알러지 위험 분석" 버튼 → AI 분석 실행
   - 즉시 결과 표시:
     - **판정 결과**: 🚨/⚠️/✅ + 판정
     - **핵심 메시지**: 한 문장 요약
     - **상세 분석**: 검출된 성분 + 판단 근거

3. **📋 검사 기록 탭**
   - 과거 검사 기록 목록
   - 각 항목: 판정, 메시지, 검출된 성분, 검사 시간

---

## 🔐 보안 및 주의사항

### 필수 체크리스트

- ✅ **OpenAI API 키 설정** (`.env`에 `OPENAI_API_KEY` 필수)
- ✅ **데이터베이스 마이그레이션** (새 테이블 생성)
- ✅ **CORS 설정** (백엔드 `.env`의 `CORS_ORIGIN` 확인)
- ✅ **JWT 토큰** (모든 알러지 API는 인증 필요)

### 주의사항

1. **이미지 크기**: 5MB 이하 권장 (API 성능)
2. **OCR 텍스트**: 원재료명, 주의사항, 혼입 가능성 문구 포함
3. **API 비용**: OpenAI Vision API 사용료 발생 (약 $0.003/이미지)
4. **분석 결과**: AI 판정이므로 100% 정확도 보장 불가 → 의료 전문가 상담 권장

---

## 📊 데이터베이스 스키마

### user_allergies 테이블
```sql
CREATE TABLE user_allergies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    allergy_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, allergy_name)
);
```

### allergy_check_records 테이블
```sql
CREATE TABLE allergy_check_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    image_url TEXT,
    ocr_text TEXT,
    verdict VARCHAR(20) NOT NULL,
    core_message TEXT,
    detected_ingredients TEXT[],
    judgment_reason TEXT,
    checked_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🧪 테스트 방법

### 1. 로컬 테스트
```bash
# 터미널 1: 백엔드
cd backend && npm run dev

# 터미널 2: 프론트엔드
npm start
```

### 2. 테스트 시나리오
1. 회원가입 및 로그인
2. 홈페이지에서 "알러지 검사소" 버튼 클릭
3. **알러지 등록**: "땅콩, 계란" 선택 후 저장
4. **검사하기**: 
   - 임의의 음식 사진 업로드
   - 텍스트 입력: "원재료명: 밀, 계란, 우유"
   - 분석 실행
5. **결과 확인**: 🚨 위험 (계란 검출)
6. **기록 조회**: 검사 기록 탭에서 방금 검사 결과 확인

### 3. Mock 데이터
```javascript
// 테스트용 알러지
const testAllergies = ['계란', '우유', '땅콩'];

// 테스트용 OCR 텍스트
const testOCR = `
원재료명: 밀, 계란, 우유, 설탕, 버터
주의: 견과류(땅콩) 사용 시설에서 제조
혼입 가능성: 메밀, 새우 포함
`;
```

---

## 🔗 관련 문서

- [백엔드 README](backend/README.md) - 백엔드 설정 및 실행
- [프론트엔드 README](README.md) - 프론트엔드 설정 및 실행
- [OpenAI API 문서](https://platform.openai.com/docs/guides/vision) - Vision API 상세
- [Claude API 문서](https://docs.anthropic.com) - Claude 3.5 모델 명세

---

## ❓ 자주 묻는 질문 (FAQ)

### Q1. OpenAI API 키는 어디서 얻나요?
**A.** [platform.openai.com](https://platform.openai.com)에서 계정 생성 후 API 키 발급

### Q2. 분석 결과가 부정확할 경우?
**A.** OCR 텍스트를 더 명확히 입력하거나, 프롬프트를 개선할 수 있습니다.

### Q3. 이미지 업로드가 안 됩니다.
**A.** 브라우저 콘솔 확인 → CORS 에러 시 백엔드 `.env`의 `CORS_ORIGIN` 확인

### Q4. 검사 기록을 삭제하고 싶습니다.
**A.** 현재 UI에서 삭제 기능 없음 → 직접 DB에서 삭제 필요

---

## 🚀 향후 확장 기능

- [ ] 이미지에서 자동 OCR 텍스트 추출 (Google Vision API)
- [ ] 식품 바코드 스캔 기능
- [ ] 알러지 통계 및 대시보드
- [ ] 친구와 검사 결과 공유
- [ ] 알러지 레벨별 위험 등급 시각화
- [ ] 오프라인 검사 모드 (사전 기반)

---

**제작자**: GitHub Copilot  
**버전**: 1.0.0  
**마지막 업데이트**: 2025-01-10
