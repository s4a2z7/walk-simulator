# Phoenix Pet Backend 🔥

걸음수를 세면서 불사조를 키우는 웹앱의 백엔드 API 서버

## 기술 스택

- **Node.js** + **Express.js** - 백엔드 프레임워크
- **PostgreSQL** - 데이터베이스
- **JWT** - 인증
- **bcrypt** - 비밀번호 암호화
- **node-cron** - 일일 리셋 스케줄러

## 설치 및 실행

### 1. 패키지 설치

```bash
npm install
```

### 2. 환경 변수 설정

`.env` 파일을 생성하고 다음 내용을 입력하세요:

```env
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=phoenix_pet
DB_USER=postgres
DB_PASSWORD=your_password

# JWT
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
JWT_EXPIRES_IN=30d

# Server
PORT=3000
NODE_ENV=development

# CORS
CORS_ORIGIN=http://localhost:3001
```

### 3. 데이터베이스 설정

PostgreSQL 데이터베이스를 생성하고 스키마를 실행하세요:

```bash
# PostgreSQL 접속
psql -U postgres

# 데이터베이스 생성
CREATE DATABASE phoenix_pet;

# 종료
\q

# 스키마 실행
psql -U postgres -d phoenix_pet -f database/schema.sql
```

### 4. 서버 실행

```bash
# 개발 모드 (nodemon)
npm run dev

# 프로덕션 모드
npm start
```

서버가 `http://localhost:3000`에서 실행됩니다.

## API 엔드포인트

### 인증 (Authentication)

#### 회원가입
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "john",
  "email": "john@example.com",
  "password": "password123",
  "display_name": "John"
}
```

#### 로그인
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "john",
  "password": "password123"
}
```

#### 현재 사용자 정보
```http
GET /api/auth/me
Authorization: Bearer {token}
```

### 펫 관리 (Pet Management)

#### 펫 정보 조회
```http
GET /api/pet
Authorization: Bearer {token}
```

#### 걸음수 추가
```http
POST /api/pet/steps
Authorization: Bearer {token}
Content-Type: application/json

{
  "steps": 100
}
```

#### 먹이 주기
```http
POST /api/pet/feed
Authorization: Bearer {token}
Content-Type: application/json

{
  "food_type": "berry"
}
```
- `berry`: 무료, +15 배고픔
- `meat`: 100 걸음, +40 배고픔
- `golden_fruit`: 500 걸음, +100 배고픔

#### 펫 이름 변경
```http
PATCH /api/pet/name
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "피닉스"
}
```

#### 펫 상태 조회
```http
GET /api/pet/status
Authorization: Bearer {token}
```

### 랭킹 (Ranking)

#### 친구 랭킹 조회
```http
GET /api/ranking?limit=10
Authorization: Bearer {token}
```

#### 글로벌 리더보드
```http
GET /api/ranking/leaderboard?limit=50
Authorization: Bearer {token}
```

#### 친구 추가
```http
POST /api/ranking/friends
Authorization: Bearer {token}
Content-Type: application/json

{
  "username": "jane"
}
```

#### 친구 목록 조회
```http
GET /api/ranking/friends
Authorization: Bearer {token}
```

#### 친구 삭제
```http
DELETE /api/ranking/friends/{friendshipId}
Authorization: Bearer {token}
```

### 통계 (Statistics)

#### 오늘의 통계
```http
GET /api/statistics/today
Authorization: Bearer {token}
```

#### 걸음수 히스토리
```http
GET /api/statistics/history?days=7
Authorization: Bearer {token}
```

#### 진화 기록
```http
GET /api/statistics/evolutions
Authorization: Bearer {token}
```

#### 먹이 기록
```http
GET /api/statistics/feedings?limit=20
Authorization: Bearer {token}
```

## 펫 진화 단계

| 단계 | 이름 | 이모지 | 필요 EXP |
|------|------|--------|----------|
| 1 | 신비한 알 | 🥚 | 0 - 1,000 |
| 2 | 작은 병아리 | 🐤 | 1,000 - 3,000 |
| 3 | 날개 돋는 새 | 🐦 | 3,000 - 7,000 |
| 4 | 불꽃의 새 | 🔥 | 7,000 - 15,000 |
| 5 | 황금 불사조 | ✨ | 15,000+ |

**EXP 계산:** 10걸음 = 1 EXP

## 일일 리셋

매일 자정(00:00)에 자동으로 실행됩니다:
- `today_steps` → 0으로 리셋
- `hunger_level` → -10 감소
- `happiness_level` → -5 감소

## 프로젝트 구조

```
phoenix-pet-backend/
├── config/
│   └── database.js          # PostgreSQL 연결
├── controllers/
│   ├── authController.js    # 인증 로직
│   ├── petController.js     # 펫 관리 로직
│   ├── rankingController.js # 랭킹 로직
│   └── statisticsController.js # 통계 로직
├── middleware/
│   └── auth.js              # JWT 인증 미들웨어
├── routes/
│   ├── auth.js              # 인증 라우트
│   ├── pet.js               # 펫 라우트
│   ├── ranking.js           # 랭킹 라우트
│   └── statistics.js        # 통계 라우트
├── database/
│   └── schema.sql           # DB 스키마
├── .env.example             # 환경변수 예제
├── .gitignore
├── package.json
├── server.js                # 메인 서버
└── README.md
```

## 라이센스

MIT

## 기여

이슈와 PR은 언제나 환영입니다! 🎉
