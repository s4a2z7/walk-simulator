# Phoenix Pet Frontend 🔥

걸음수를 세면서 불사조를 키우는 웹앱 - 프론트엔드

## 기술 스택

- **React 18** - UI 라이브러리
- **React Router** - 라우팅
- **Tailwind CSS** - 스타일링
- **Axios** - API 통신

## 디자인

**3D 캐주얼 게임 스타일** (Walkr, Pokémon GO 스타일)
- 밝은 초록색 배경 (잔디)
- 귀여운 펫 캐릭터
- 부드러운 애니메이션
- 직관적인 UI

## 설치 및 실행

### 1. 패키지 설치

```bash
npm install
```

### 2. 환경 변수 설정

`.env` 파일을 생성하세요:

```env
REACT_APP_API_URL=http://localhost:3000/api
```

### 3. 개발 서버 실행

```bash
npm start
```

앱이 `http://localhost:3001`에서 실행됩니다.

### 4. 프로덕션 빌드

```bash
npm run build
```

## 프로젝트 구조

```
src/
├── components/           # 재사용 컴포넌트
│   ├── PetWorld.js      # 메인 3D 월드
│   ├── PetCharacter.js  # 펫 캐릭터 표시
│   ├── TopBar.js        # 상단 스탯 바
│   ├── FoodTray.js      # 하단 먹이 버튼
│   ├── EvolutionModal.js # 진화 애니메이션
│   └── RankingModal.js  # 랭킹 모달
├── pages/               # 페이지
│   ├── LoginPage.js     # 로그인
│   ├── RegisterPage.js  # 회원가입
│   └── HomePage.js      # 메인 게임
├── services/
│   └── api.js          # API 호출 함수
├── App.js              # 메인 앱
├── index.js            # 엔트리 포인트
└── index.css           # 글로벌 스타일
```

## 주요 기능

### 1. 인증
- 회원가입 (자동으로 펫 생성)
- 로그인
- JWT 토큰 기반 인증

### 2. 펫 키우기
- 걸음수 추가 (10걸음 = 1 EXP)
- 5단계 진화 시스템
- 실시간 상태 표시

### 3. 먹이 주기
- 🍓 불꽃 베리 (무료)
- 🍖 신성한 고기 (100 걸음)
- 🍑 황금 과일 (500 걸음)

### 4. 친구 시스템
- 친구 추가
- 랭킹 보기
- 친구 펫 비교

## 컴포넌트 설명

### PetWorld
메인 3D 월드 컴포넌트
- 떠다니는 구름
- 흔들리는 나무
- 중앙의 펫
- 친구 펫들

### PetCharacter
펫 캐릭터 표시
- 단계별 다른 이모지
- 불꽃 효과 (3단계+)
- 황금 반짝임 (5단계)
- 애니메이션 (idle, happy, walking)

### TopBar
상단 스탯 바
- 오늘 걸음수
- 경험치 바
- 배고픔
- 행복도
- 랭킹 버튼

### FoodTray
하단 먹이 버튼
- 3가지 먹이 종류
- 비용 표시
- 호버 툴팁

### EvolutionModal
진화 애니메이션
- 전체 화면 오버레이
- 이전→새 캐릭터 변화
- 폭죽 효과
- 황금 불사조 특별 애니메이션

### RankingModal
랭킹 모달
- 친구 목록
- 친구 추가
- EXP 기준 순위

## API 연동

모든 API 호출은 `src/services/api.js`에서 관리합니다.

```javascript
import { petAPI, authAPI, rankingAPI } from './services/api';

// 인증
await authAPI.login({ username, password });
await authAPI.register(formData);

// 펫
await petAPI.getPet();
await petAPI.addSteps(100);
await petAPI.feedPet('berry');

// 랭킹
await rankingAPI.getRanking();
await rankingAPI.addFriend('username');
```

## 스타일링

### Tailwind 커스텀 색상

```javascript
// tailwind.config.js
colors: {
  grass: {
    DEFAULT: '#7ED321',
    dark: '#5FB304',
  },
  phoenix: {
    red: '#FF6B6B',
    orange: '#FFB74D',
    gold: '#FFD700',
  }
}
```

### 커스텀 애니메이션

```css
@keyframes petFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

@keyframes cloudFloat {
  0% { transform: translateX(-10%); }
  100% { transform: translateX(120vw); }
}
```

## 환경별 설정

### 개발 환경
```env
REACT_APP_API_URL=http://localhost:3000/api
```

### 프로덕션 환경
```env
REACT_APP_API_URL=https://your-backend.com/api
```

## 배포

### Vercel 배포

```bash
# Vercel CLI 설치
npm i -g vercel

# 로그인
vercel login

# 배포
vercel

# 환경 변수 설정
vercel env add REACT_APP_API_URL
```

### Netlify 배포

1. GitHub에 푸시
2. Netlify에서 저장소 연결
3. 빌드 설정:
   - Build command: `npm run build`
   - Publish directory: `build`
4. 환경 변수 추가:
   - `REACT_APP_API_URL`

## 문제 해결

### CORS 오류
백엔드 `.env`에서 `CORS_ORIGIN`을 프론트엔드 주소로 설정:
```
CORS_ORIGIN=http://localhost:3001
```

### API 연결 실패
1. 백엔드가 실행 중인지 확인
2. `.env`의 `REACT_APP_API_URL` 확인
3. 브라우저 콘솔에서 네트워크 탭 확인

### 빌드 오류
```bash
# 캐시 삭제
rm -rf node_modules package-lock.json
npm install

# 다시 빌드
npm run build
```

## 향후 개발 계획

- [ ] 실제 걸음수 센서 연동
- [ ] PWA (프로그레시브 웹 앱)
- [ ] 푸시 알림
- [ ] 다크 모드
- [ ] 펫 커스터마이징
- [ ] 업적 시스템

## 라이센스

MIT

## 기여

이슈와 PR은 언제나 환영합니다! 🎉
