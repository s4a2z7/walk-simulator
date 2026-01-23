# Phoenix Pet - 프론트엔드와 백엔드 연동 가이드 🔥

이 문서는 Phoenix Pet 프론트엔드가 백엔드 API와 어떻게 연동되는지 설명합니다.

## 📦 프로젝트 구조

```
phoenix-pet/ (부모 폴더)
├── backend/              # Phoenix Pet Backend
│   ├── server.js
│   ├── controllers/
│   ├── routes/
│   ├── middleware/
│   ├── database/
│   ├── package.json
│   └── README.md
└── (frontend)           # Phoenix Pet Frontend (현재 폴더)
    ├── src/
    ├── public/
    ├── package.json
    └── README.md
```

## 🚀 빠른 시작

### 1단계: 백엔드 설정

```bash
cd backend

# 패키지 설치
npm install

# .env 파일 생성
cp .env.example .env

# .env 파일 수정 (PostgreSQL 설정)
# DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD 설정

# 데이터베이스 생성 및 스키마 실행
psql -U postgres
CREATE DATABASE phoenix_pet;
\q

psql -U postgres -d phoenix_pet -f database/schema.sql

# 백엔드 서버 시작
npm run dev
# 서버가 http://localhost:3000 에서 실행됨
```

### 2단계: 프론트엔드 설정

```bash
cd ..  # 부모 폴더로 이동

# 패키지 설치
npm install

# .env 파일 생성
cp .env.example .env

# .env 파일 내용 (기본값은 이미 설정됨)
# REACT_APP_API_URL=http://localhost:3000/api

# 프론트엔드 개발 서버 시작
npm start
# 브라우저에서 http://localhost:3000 으로 접속
```

## 🔗 API 연동 규격

### 인증 (Auth)

#### 회원가입
```
프론트엔드 요청:
POST /api/auth/register
{
  "username": "john",
  "email": "john@example.com",
  "password": "password123",
  "display_name": "John"
}

백엔드 응답 (201 Created):
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "john",
    "display_name": "John",
    "avatar_emoji": "🎮"
  },
  "token": "eyJhbGc..."
}
```

#### 로그인
```
프론트엔드 요청:
POST /api/auth/login
{
  "username": "john",
  "password": "password123"
}

백엔드 응답 (200 OK):
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "john",
    "display_name": "John",
    "avatar_emoji": "🎮"
  },
  "token": "eyJhbGc..."
}

프론트엔드 저장:
localStorage.setItem('token', token)
localStorage.setItem('user', JSON.stringify(user))
```

### 펫 관리 (Pet)

#### 펫 정보 조회
```
프론트엔드 요청:
GET /api/pet
Headers: { Authorization: Bearer {token} }

백엔드 응답 (200 OK):
{
  "pet": {
    "id": 1,
    "user_id": 1,
    "name": "불사조",
    "current_stage": 1,
    "stage_name": "신비한 알",
    "stage_emoji": "🥚",
    "total_exp": 0,
    "current_exp": 0,
    "exp_to_next_stage": 1000,
    "total_steps": 0,
    "today_steps": 0,
    "hunger_level": 50,
    "happiness_level": 50,
    "progress_percentage": 0
  }
}

프론트엔드 처리:
const pet = response.data.pet
setPet({
  stage: pet.current_stage,
  stage_name: pet.stage_name,
  stage_emoji: pet.stage_emoji,
  level: Math.floor(pet.total_exp / 1000) + 1,
  experience: pet.current_exp,
  steps: pet.today_steps,
  hunger: pet.hunger_level,
  ...
})
```

#### 걸음수 추가
```
프론트엔드 요청:
POST /api/pet/steps
Headers: { Authorization: Bearer {token} }
Body: { "steps": 10 }

백엔드 응답 (200 OK):
{
  "pet": {
    "today_steps": 10,
    "total_steps": 10,
    "total_exp": 1,
    "current_exp": 1,
    "current_stage": 1,
    "stage_name": "신비한 알",
    "hunger_level": 49
  },
  "exp_gained": 1,
  "evolved": false,
  "evolution_info": null,
  "hunger_decreased": false,
  "current_hunger": 49
}

프론트엔드 처리:
만약 evolved === true이면 진화 애니메이션 표시
```

#### 진화 시 응답 예시
```
백엔드 응답 (evolved: true):
{
  "pet": {...},
  "evolved": true,
  "evolution_info": {
    "from_stage": 1,
    "to_stage": 2,
    "from_name": "신비한 알",
    "to_name": "작은 병아리",
    "from_emoji": "🥚",
    "to_emoji": "🐤",
    "celebration_message": "축하합니다! 작은 병아리(으)로 진화했습니다!"
  }
}

프론트엔드 처리:
- EvolutionModal 활성화
- stage === 5이면 황금 불사조 애니메이션 (7초)
- stage < 5이면 일반 진화 애니메이션 (3초)
```

#### 먹이 주기
```
프론트엔드 요청:
POST /api/pet/feed
Headers: { Authorization: Bearer {token} }
Body: { "food_type": "berry" | "meat" | "golden_fruit" }

먹이 종류:
- berry: 무료
- meat: 100 걸음 필요
- golden_fruit: 500 걸음 필요

백엔드 응답 (200 OK):
{
  "pet": {
    "hunger_level": 65,
    "happiness_level": 55,
    "today_steps": 100  // 비용만큼 차감
  },
  "food_effect": {
    "name": "불꽃 베리",
    "emoji": "🍓",
    "hunger_restored": 15,
    "happiness_gained": 5
  },
  "message": "불사조가 🍓 불꽃 베리을(를) 맛있게 먹었어요!"
}

에러 응답 (400 Bad Request - 걸음수 부족):
{
  "error": "Not enough steps",
  "required": 100,
  "available": 50
}
```

### 랭킹 (Ranking)

#### 친구 랭킹 조회
```
프론트엔드 요청:
GET /api/ranking?limit=10
Headers: { Authorization: Bearer {token} }

백엔드 응답 (200 OK):
{
  "rankings": [
    {
      "user_id": 1,
      "username": "john",
      "display_name": "John",
      "avatar_emoji": "🎮",
      "pet_name": "Phoenix",
      "pet_stage": 2,
      "pet_stage_name": "작은 병아리",
      "pet_emoji": "🐤",
      "total_exp": 1500,
      "total_steps": 15000,
      "age_days": 5,
      "is_me": true,
      "rank": 1
    },
    {
      "user_id": 2,
      "username": "jane",
      "display_name": "Jane",
      "avatar_emoji": "💎",
      "pet_name": "FireBird",
      "pet_stage": 1,
      "pet_stage_name": "신비한 알",
      "pet_emoji": "🥚",
      "total_exp": 1000,
      "total_steps": 10000,
      "age_days": 3,
      "is_me": false,
      "rank": 2
    }
  ]
}

프론트엔드 처리:
const rankings = response.data.rankings.map((rank) => ({
  id: rank.user_id,
  display_name: rank.display_name,
  level: Math.floor(rank.total_exp / 1000) + 1,
  steps: rank.total_steps,
  stage: rank.pet_stage,
}))
```

## 📊 데이터 변환

### 레벨 계산
```javascript
백엔드: total_exp (누적 경험치)
프론트엔드: level = Math.floor(total_exp / 1000) + 1

예시:
- total_exp: 0 → level: 1
- total_exp: 999 → level: 1
- total_exp: 1000 → level: 2
- total_exp: 5000 → level: 6
```

### 경험치 바 진행률
```javascript
백엔드: current_exp, exp_to_next_stage
프론트엔드: progress = Math.round((current_exp / exp_to_next_stage) * 100)

예시:
- current_exp: 0, exp_to_next_stage: 1000 → progress: 0%
- current_exp: 500, exp_to_next_stage: 1000 → progress: 50%
- current_exp: 1000, exp_to_next_stage: 1000 → progress: 100%
```

### 펫 단계별 진화
```
단계 1: 신비한 알 (🥚) → 0-1,000 EXP
단계 2: 작은 병아리 (🐤) → 1,000-3,000 EXP
단계 3: 날개 돋는 새 (🐦) → 3,000-7,000 EXP
단계 4: 불꽃의 새 (🔥) → 7,000-15,000 EXP
단계 5: 황금 불사조 (✨) → 15,000+ EXP

진화 조건:
- current_exp >= exp_to_next_stage 일 때 자동 진화
- 진화 시 evolved: true 반환
- evolution_info에 진화 상세 정보 포함
```

## 🔐 토큰 관리

### 로그인 후
```javascript
// 응답에서 받은 토큰 저장
localStorage.setItem('token', response.data.token)
localStorage.setItem('user', JSON.stringify(response.data.user))
```

### API 요청 시
```javascript
// axios interceptor가 자동으로 Authorization 헤더 추가
const axiosInstance = axios.create({ baseURL: API_URL })
axiosInstance.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```

### 401 Unauthorized
```javascript
// 토큰 만료 또는 유효하지 않음
try {
  const response = await petAPI.getPet()
} catch (err) {
  if (err.response?.status === 401) {
    // 로그인 페이지로 이동
    navigate('/login')
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }
}
```

## 📱 프론트엔드 API 서비스 구조

```javascript
// src/services/api.js

// 각 API 그룹별 구조:
export const authAPI = {
  register: (data) => axiosInstance.post('/auth/register', data),
  login: (data) => axiosInstance.post('/auth/login', data),
  getCurrentUser: () => axiosInstance.get('/auth/me'),
}

export const petAPI = {
  getPet: () => axiosInstance.get('/pet'),
  getPetStatus: () => axiosInstance.get('/pet/status'),
  addSteps: (steps) => axiosInstance.post('/pet/steps', { steps }),
  feedPet: (food_type) => axiosInstance.post('/pet/feed', { food_type }),
  updatePetName: (name) => axiosInstance.patch('/pet/name', { name }),
}

export const rankingAPI = {
  getRanking: (limit = 10) => axiosInstance.get(`/ranking?limit=${limit}`),
  getLeaderboard: (limit = 50) => axiosInstance.get(`/ranking/leaderboard?limit=${limit}`),
  addFriend: (username) => axiosInstance.post('/ranking/friends', { username }),
  getFriends: () => axiosInstance.get('/ranking/friends'),
  removeFriend: (friendshipId) => axiosInstance.delete(`/ranking/friends/${friendshipId}`),
}

export const statisticsAPI = {
  getTodayStats: () => axiosInstance.get('/statistics/today'),
  getHistory: (days = 7) => axiosInstance.get(`/statistics/history?days=${days}`),
  getEvolutions: () => axiosInstance.get('/statistics/evolutions'),
  getFeedings: (limit = 20) => axiosInstance.get(`/statistics/feedings?limit=${limit}`),
}
```

## 🐛 에러 처리

### 일반적인 에러 응답

```javascript
400 Bad Request:
{
  "error": "Invalid steps amount"
}

401 Unauthorized:
{
  "error": "Invalid credentials"
}

404 Not Found:
{
  "error": "Pet not found"
}

409 Conflict:
{
  "error": "Username or email already exists"
}

500 Internal Server Error:
{
  "error": "Registration failed",
  "details": "..."
}
```

### 프론트엔드 에러 처리 예시
```javascript
try {
  const response = await petAPI.feedPet(foodType)
  // 성공 처리
  setPet(response.data.pet)
} catch (err) {
  // 에러 메시지 표시
  const errorMessage = err.response?.data?.error || '알 수 없는 오류 발생'
  setError(errorMessage)
}
```

## ✅ 검증 체크리스트

프론트엔드와 백엔드가 제대로 연동되는지 확인하려면:

- [ ] 회원가입 성공 (토큰 발급)
- [ ] 로그인 성공 (토큰 발급)
- [ ] 펫 정보 조회 성공
- [ ] 걸음수 추가 성공
- [ ] 배고픔 감소 동작 확인
- [ ] 먹이 주기 성공 (걸음수 차감)
- [ ] 진화 애니메이션 작동
- [ ] 랭킹 조회 성공
- [ ] 토큰 만료 시 로그인 페이지로 이동

## 📞 주요 엔드포인트 요약

| 기능 | 메소드 | 엔드포인트 | 인증 |
|------|--------|-----------|------|
| 회원가입 | POST | /auth/register | ✗ |
| 로그인 | POST | /auth/login | ✗ |
| 현재 사용자 | GET | /auth/me | ✓ |
| 펫 정보 | GET | /pet | ✓ |
| 펫 상태 | GET | /pet/status | ✓ |
| 걸음수 추가 | POST | /pet/steps | ✓ |
| 먹이 주기 | POST | /pet/feed | ✓ |
| 펫 이름 변경 | PATCH | /pet/name | ✓ |
| 친구 랭킹 | GET | /ranking | ✓ |
| 글로벌 리더보드 | GET | /ranking/leaderboard | ✓ |
| 오늘의 통계 | GET | /statistics/today | ✓ |

---

**프로젝트가 완벽하게 준비되었습니다!** 🎉
백엔드를 실행하고 프론트엔드를 실행하면 즉시 게임을 즐길 수 있습니다.
