# Phoenix Pet Frontend 완성 ✅

React + Tailwind CSS로 만든 **3D 캐주얼 게임 스타일** 프론트엔드가 완성되었습니다!

## 📁 프로젝트 구조

```
phoenix-pet-frontend/
├── public/
│   └── index.html                 # HTML 진입점
├── src/
│   ├── components/
│   │   ├── PetWorld.js            # 메인 3D 월드 (구름, 나무)
│   │   ├── PetCharacter.js        # 펫 캐릭터 (5단계 진화)
│   │   ├── TopBar.js              # 상단 스탯 바 (걸음수, 경험치, 배고픔)
│   │   ├── FoodTray.js            # 하단 먹이 버튼 (3가지 음식)
│   │   ├── RankingModal.js        # 랭킹 모달 (메달 표시)
│   │   └── EvolutionModal.js      # 진화 애니메이션 (2가지 버전)
│   ├── pages/
│   │   ├── LoginPage.js           # 로그인 페이지
│   │   ├── RegisterPage.js        # 회원가입 페이지
│   │   └── HomePage.js            # 메인 게임 페이지
│   ├── services/
│   │   └── api.js                 # API 통신 (Auth, Pet, Ranking)
│   ├── App.js                     # 라우터 설정
│   ├── index.js                   # React 진입점
│   └── index.css                  # 글로벌 스타일
├── package.json                   # 의존성 설정
├── tailwind.config.js             # Tailwind 설정 (애니메이션 포함)
├── postcss.config.js              # PostCSS 설정
├── .env.example                   # 환경 변수 예시
├── .gitignore                     # Git 무시 파일
└── README.md                      # 상세 문서

## 🎨 주요 기능

### 1️⃣ 펫 진화 시스템 (5단계)
- 🥚 단계 1: 알 (회색)
- 🐤 단계 2: 병아리 (노란색)
- 🐦 단계 3: 날개 새 (주황색, 불꽃 파티클)
- 🔥 단계 4: 불꽃 새 (빨간색, 불꽃 + 날개)
- ✨ 단계 5: 황금 불사조 (금색, 황금 광채 + 왕관)

### 2️⃣ 진화 애니메이션
- **일반 진화** (1-4단계): 불꽃 20개 회전, 3초 지속
- **황금 불사조** (5단계): 황금 광선, 불꽃 50개, 왕관 하강, 7초 지속

### 3️⃣ 게임 시스템
- **걸음수**: 펫 클릭으로 10걸음씩 증가
- **경험치**: 레벨 시스템 (0-100% 진행)
- **배고픔**: 시간에 따라 증가, 먹이로 회복
- **먹이**:
  - 🍓 불꽃 베리: 무료 (항상 가능)
  - 🍖 신성한 고기: 100걸음 필요
  - 🍑 황금 과일: 500걸음 필요

### 4️⃣ 애니메이션 효과
- **cloudFloat**: 구름이 화면 가로질러 이동 (20초)
- **petFloat**: 펫이 부드럽게 떠올랐다 내려옴 (3초 반복)
- **petJump**: 펫 클릭 시 점프 (0.6초)
- **flameRise**: 불꽃 파티클 올라감 (1초)
- **sparkleOrbit**: 황금 스파클 회전 (2초)
- **goldenGlow**: 황금 빛이 맥박치듯 점멸 (2초)

### 5️⃣ UI 특징
- 밝은 초록색 배경 (3D 게임 스타일)
- 떠다니는 구름
- 흔들리는 나무
- 둥글둥글한 버튼 디자인
- 반응형 레이아웃
- 모바일 친화적

## 🚀 설치 및 실행

### 1. 패키지 설치
```bash
cd "c:\Users\LG\Desktop\claude simulator"
npm install
```

### 2. 환경 설정
```bash
# .env 파일 생성 (.env.example 참고)
REACT_APP_API_URL=http://localhost:3000/api
```

### 3. 개발 서버 실행
```bash
npm start
```
브라우저에서 http://localhost:3000 으로 접속하세요.

### 4. 프로덕션 빌드
```bash
npm run build
```

## 📋 API 연동 준비 완료

모든 API 호출이 준비되어 있습니다:

### 인증 (Auth)
- `POST /auth/register` - 회원가입
- `POST /auth/login` - 로그인

### 펫 (Pet)
- `GET /pet` - 펫 정보 조회
- `POST /pet/steps` - 걸음수 추가
- `POST /pet/feed` - 먹이 주기

### 랭킹 (Ranking)
- `GET /ranking` - 전체 사용자 랭킹

## 🎯 기술 스택

- **React 18** - UI 라이브러리
- **React Router v6** - 라우팅
- **Tailwind CSS** - 유틸리티 기반 스타일링
- **Axios** - HTTP 클라이언트

## ✨ 구현된 모든 기능

✅ 완전한 로그인/회원가입 페이지
✅ 메인 게임 페이지 (PetWorld)
✅ 펫 캐릭터 (5단계 진화)
✅ 상단 스탯 바 (걸음수, 경험치, 배고픔, 랭킹)
✅ 하단 먹이 버튼 (3가지 음식)
✅ 랭킹 모달 (메달 표시)
✅ 진화 애니메이션 (2가지 버전)
✅ 6가지 Keyframe 애니메이션
✅ API 서비스 통합
✅ 토큰 기반 인증
✅ 에러 처리
✅ 로딩 상태
✅ 반응형 디자인
✅ README.md (완전한 문서)
✅ 환경 변수 설정

## 📝 특수 구현 사항

### 진화 애니메이션
- **Stage 1-4**: 불꽃 20개 회전 + 3초 지속
- **Stage 5** (황금 불사조): 
  - 불꽃 50개 회전
  - 황금 광선 3개 내려감
  - 왕관 👑 하강 애니메이션
  - "👑 전설 달성! 👑" 메시지
  - 7초 지속

### 반응형 UI
- 모바일: 터치 이벤트 대응
- 태블릿: 레이아웃 조정
- 데스크톱: 최적화된 표시

## 🎮 게임 플레이 흐름

1. 로그인/회원가입
2. 펫 정보 로드
3. 펫 클릭으로 걸음수 증가
4. 걸음수로 경험치 획득
5. 경험치 100% → 레벨 업
6. 일정 경험치 누적 → 진화
7. 랭킹 확인

모든 파일이 완성되고 빌드도 성공했습니다! 🎉

Backend API를 연동하면 즉시 게임이 동작합니다.
