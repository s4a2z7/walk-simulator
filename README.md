# Walk Simulator 🔥

React + Tailwind CSS로 만든 **3D 캐주얼 게임 스타일** 불사조 키우기 게임입니다.

🚶 **걸음으로 키워봅시다! Walk Simulator - 불사조를 키우는 신나는 게임입니다!**

✨ **생생한 3D 게임 스타일 UI**
- 밝은 초록색 잔디 배경
- 떠다니는 구름, 흔들리는 나무
- 부드러운 애니메이션 효과

🔥 **펫 진화 시스템**
- 5단계 진화: 🥚 → 🐤 → 🐦 → 🔥 → ✨
- 일반 진화 애니메이션 (불꽃 파티클)
- 황금 불사조 진화 애니메이션 (황금 광선 + 왕관)

👣 **걸음수 기반 성장**
- 펫 클릭으로 걸음수 증가
- 경험치를 통한 레벨 업
- 배고픔 시스템

🍖 **먹이 시스템**
- 불꽃 베리: 무료
- 신성한 고기: 100걸음
- 황금 과일: 500걸음

🏆 **랭킹 시스템**
- 전체 사용자 랭킹
- 레벨 및 걸음수 기반 순위

## 기술 스택

- **React 18** - UI 라이브러리
- **React Router v6** - 라우팅
- **Tailwind CSS** - 스타일링
- **Axios** - HTTP 클라이언트

## 프로젝트 구조

```
src/
├── components/
│   ├── PetCharacter.js      # 펫 캐릭터
│   ├── PetWorld.js          # 메인 게임 월드
│   ├── TopBar.js            # 상단 스탯 바
│   ├── FoodTray.js          # 하단 먹이 버튼
│   ├── RankingModal.js      # 랭킹 모달
│   └── EvolutionModal.js    # 진화 애니메이션
├── pages/
│   ├── LoginPage.js         # 로그인 페이지
│   ├── RegisterPage.js      # 회원가입 페이지
│   └── HomePage.js          # 메인 게임 페이지
├── services/
│   └── api.js               # API 통신
├── App.js                   # 라우터 설정
├── index.js                 # 진입점
└── index.css                # 글로벌 스타일
```

## 설치 및 실행

### 요구사항
- Node.js 14+
- npm 또는 yarn

### 설치

```bash
# 패키지 설치
npm install

# 또는
yarn install
```

### 환경 설정

`.env.example` 파일을 참고하여 `.env` 파일을 생성하세요:

```bash
cp .env.example .env
```

그리고 API URL을 설정하세요:
```
REACT_APP_API_URL=http://localhost:3000/api
```

### 개발 서버 실행

```bash
npm start
```

또는

```bash
yarn start
```

브라우저에서 [http://localhost:3000](http://localhost:3000) 으로 접속하세요.

### 프로덕션 빌드

```bash
npm run build
```

또는

```bash
yarn build
```

`build/` 폴더에 최적화된 빌드가 생성됩니다.

## API 명세

### 인증 (Auth)

**회원가입**
```
POST /api/auth/register
Body: { username, email, password, display_name }
Response: { token, user }
```

**로그인**
```
POST /api/auth/login
Body: { username, password }
Response: { token, user }
```

### 펫 (Pet)

**펫 정보 조회**
```
GET /api/pet
Headers: { Authorization: Bearer <token> }
Response: { id, name, stage, level, experience, steps, hunger }
```

**걸음수 추가**
```
POST /api/pet/steps
Headers: { Authorization: Bearer <token> }
Body: { steps }
Response: { pet, evolved, evolution_info }
```

**먹이 주기**
```
POST /api/pet/feed
Headers: { Authorization: Bearer <token> }
Body: { food_type: 'berry' | 'meat' | 'golden_fruit' }
Response: { pet, evolved, evolution_info }
```

### 랭킹 (Ranking)

**랭킹 조회**
```
GET /api/ranking
Headers: { Authorization: Bearer <token> }
Response: [{ id, display_name, level, steps, stage }]
```

## 색상 팔레트

| 용도 | 색상 | 코드 |
|------|------|------|
| 배경 (하늘) | Light Blue | #B3E5FC |
| 배경 (잔디) | Bright Green | #7ED321 |
| 배경 (어두운 잔디) | Dark Green | #5FB304 |
| 단계 1 (알) | Gray | #E0E0E0 |
| 단계 2 (병아리) | Yellow | #FFD54F |
| 단계 3 (날개 새) | Orange | #FFB74D |
| 단계 4 (불꽃 새) | Red | #FF6B6B |
| 단계 5 (황금 불사조) | Gold | #FFD700 |

## 애니메이션

- **cloudFloat**: 구름이 화면을 가로질러 이동 (20초)
- **petFloat**: 펫이 부드럽게 떠올랐다 내려옴 (3초)
- **petJump**: 펫이 점프하며 커짐 (0.6초)
- **flameRise**: 불꽃 파티클이 위로 올라가며 사라짐 (1초)
- **sparkleOrbit**: 황금 스파클이 회전하며 나타났다 사라짐 (2초)
- **goldenGlow**: 황금 빛이 맥박치듯 점멸 (2초)

## 기능 명세

### 페이지

#### 로그인 페이지
- 사용자명, 비밀번호 입력
- 회원가입 링크
- 토큰 기반 인증

#### 회원가입 페이지
- 사용자명, 이메일, 비밀번호, 표시명 입력
- 자동 로그인

#### 홈 페이지 (게임)
- 펫 표시 및 상호작용
- 실시간 스탯 업데이트 (5초마다)
- 진화 애니메이션
- 랭킹 모달
- 로그아웃 기능

### 컴포넌트

#### PetWorld
- 게임 월드 배경
- 구름 애니메이션
- 나무 장식

#### PetCharacter
- 5단계 펫 표시
- 단계별 이펙트 (불꽃, 날개, 황금 광채)
- 펫 클릭 감지
- 친구 펫 표시

#### TopBar
- 일일 걸음수
- 경험치 바
- 레벨
- 배고픔 상태
- 랭킹 버튼

#### FoodTray
- 3가지 먹이 옵션
- 걸음수 기반 구매 가능 여부
- 비활성화 상태 표시

#### EvolutionModal
- 일반 진화 (1-4단계): 불꽃 파티클, 3초 지속
- 황금 불사조 진화 (5단계): 황금 광선, 왕관, 7초 지속

#### RankingModal
- 상위 사용자 표시
- 메달 표시 (🥇 🥈 🥉)
- 레벨, 걸음수, 단계 표시

## 특수 기능

### 반응형 디자인
- 모바일 친화적 레이아웃
- 터치 이벤트 대응

### 에러 처리
- API 호출 실패 시 에러 메시지
- 401 Unauthorized 시 로그인 페이지로 이동

### 로딩 상태
- 초기 로딩 화면
- 비동기 작업 중 로딩 표시

## 브라우저 지원

- Chrome (최신)
- Firefox (최신)
- Safari (최신)
- Edge (최신)

## 라이센스

MIT

## 문의

문제가 있거나 제안사항이 있으면 이슈를 등록해주세요.

---

**행복한 펫 키우기를 즐기세요!** 🔥✨
